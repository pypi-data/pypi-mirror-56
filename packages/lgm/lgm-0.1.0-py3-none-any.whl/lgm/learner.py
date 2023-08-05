import numpy as np
import pandas as pd
import torch
from functools import partial
from torch import tensor
from torch.utils.data import DataLoader
from .optimizer import adam_opt
from .utils import ALL_CALLBACKS, param_getter, listify, CancelTrainException, CancelEpochException, CancelBatchException, CancelPredsException
from .callbacks import TrainEvalCallback, ProgressCallback, Plotter, SendToDeviceCallback, AvgStatsCallback, SaveModelCallback, GetPredictionsCallback

class Learner():
    """
    Main train-eval class that packages together a model, the data,
    the loss function and the optimizer.
    In addition, it keeps track of a learning rate and a splitter function that
    can split the model layers into mutiple groups so that they can be trained
    with different learning rates.
    Default splitter does nothing, but this is where splitter functions for
    discriminative learning rates should be passed.
    Finally, the learner is passed a list of callbacks and can be called (like
    a function) with attrs inherited from the callbacks.
    Callbacks added by default: TrainEvalCallback, ProgressCallback, Plotter,
    SendToDeviceCallback (send to cuda if available), AvgStatsCallback for loss_func
    and metrics.
    """
    def __init__(self, model, data, loss_func, opt_func=adam_opt(), lr=1e-2,
                 splitter=param_getter, metrics=None, callbacks=None,
                 callback_funcs=None, device=None, reset_opt=False,
                 model_name=None, path_str=None):
        self.model = model
        self.data = data
        self.loss_func = loss_func
        self.opt_func = opt_func
        self.lr = lr
        self.splitter = splitter
        self.metrics = metrics
        if device == None:
            # by default, we select the first GPU or the CPU if there are no GPUs
            self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        else:
            # use the device argument of the Learner to select a specific GPU
            # for example, 'cuda:0' will select the first GPU, 'cuda:1' the second etc.
            self.device = torch.device(device)
        self.reset_opt = reset_opt # whether to reset the optimizer or not; resets after LRFinder
        # this is where we will save the metric_dicts contributed by AvgStatsCallback or GetPredictionsCallback
        self.train_metrics_dict = None
        self.valid_metrics_dict = None
        self.pred_metrics_dict = None
        self.pred_avg_stats = None
        self.pred_df = pd.DataFrame(columns=[#'X',
                                             'Y', 'Y_hat'])
        self.in_train = False
        self.logger = print
        self.opt = None
        self.ALL_CALLBACKS = ALL_CALLBACKS # inventory of all possible callback functions
        self.callbacks = [] # the list of callbacks that are actually run

        # self.callback_list stores default callbacks to be added to self.callbacks below
        self.callback_list = [ProgressCallback(), Plotter(), SendToDeviceCallback()]
        if model_name and isinstance(model_name, str):
            self.callback_list.append(SaveModelCallback(model_name=model_name, path_str=path_str))
        # add the callbacks called with the Learner instance to the self.callback_list
        self.callback_list.extend(listify(callbacks))
        # add the callback_funcs called with the Learner instance to the self.callback_list
        self.callback_list.extend(callback_func() for callback_func in listify(callback_funcs))

        # add the self.callback_list to self.callbacks
        self.add_callbacks(self.callback_list)

    def add_callbacks(self, callbacks):
        for callback in listify(callbacks):
            self.add_callback(callback)

    def add_callback(self, callback):
        "grab callback and set it as an attr under its name"
        callback.set_learner(self)
        setattr(self, callback.name, callback)
        self.callbacks.append(callback)

    def remove_callbacks(self, callbacks):
        for callback in listify(callbacks):
            self.callbacks.remove(callback)

    def one_batch(self, i, xb, yb):
        try:
            self.iter = i
            self.xb, self.yb = xb, yb;                      self('begin_batch')
            self.pred = self.model(self.xb);                self('after_pred')
            self.loss = self.loss_func(self.pred, self.yb); self('after_loss')
            if not self.in_train:
                return
            self.loss.backward();                           self('after_backward')
            self.opt.step();                                self('after_step')
            self.opt.zero_grad()
        except CancelBatchException:                        self('after_cancel_batch')
        finally:                                            self('after_batch')

    def all_batches(self):
        self.iters = len(self.dl)
        try:
            for i, (xb, yb) in enumerate(self.dl):
                self.one_batch(i, xb, yb)
        except CancelEpochException: self('after_cancel_epoch')

    def do_begin_fit(self, epochs):
        self.epochs = epochs
        self.loss = tensor(0.)
        self('begin_fit')

    def do_begin_epoch(self, epoch):
        self.epoch = epoch
        self.dl = self.data.train_dl
        return self('begin_epoch')

    def fit(self, epochs, callbacks=None):
        # add TrainEvalCallback and AvgStatsCallback to the fit_callbacks
        fit_callbacks = [TrainEvalCallback(),
                         AvgStatsCallback(listify(self.metrics))]
        # add the callbacks passed to fit() to callbacks
        fit_callbacks.extend(listify(callbacks))
        self.add_callbacks(fit_callbacks)
        # create optimizer on fit(), optionally replacing existing optimizer (e.g., after LRFinder)
        if self.reset_opt or not self.opt:
            self.opt = self.opt_func(self.splitter(self.model), lr=self.lr)
            self.reset_opt = False
        try:
            self.do_begin_fit(epochs)
            for epoch in range(epochs):
                self.do_begin_epoch(epoch)
                if not self('begin_epoch'): self.all_batches()

                with torch.no_grad():
                    self.dl = self.data.valid_dl
                    if not self('begin_validate'): self.all_batches()
                self('after_epoch')
        except CancelTrainException:
            self('after_cancel_train')
        finally:
            self('after_fit')
            # remove callbacks passed with fit,
            # as well as TrainEvalCallback and AvgStatsCallback
            self.remove_callbacks(fit_callbacks)

    def _get_preds(self, valid_preds=True, new_dl=None, record_preds=False):
        """
        The record_preds part still needs work. Ideally, the post-processing of
        the predictions would be done by a callback, and all post-processing
        would be done in the after_batch method of the callback rather than
        hardcoding different cases here (current_Y_hat for regression,
        current_Y_hat for classification etc.).
        """
        # add GetPredictionsCallback
        get_preds_callbacks = [GetPredictionsCallback(listify(self.metrics))]
        self.add_callbacks(get_preds_callbacks)
        # (re)set various Learner attributes, including correct dataloader
        self.loss = tensor(0.)
        self.pred_df = pd.DataFrame(columns=[#'X',
                                             'Y', 'Y_hat'])
        if new_dl == None and valid_preds:
            self.dl = self.data.valid_dl
        elif new_dl == None and not valid_preds:
            self.dl = self.data.train_dl
        elif isinstance(new_dl, DataLoader):
            self.dl = new_dl
        else:
            raise CancelPredsException("No new dataloader: `new_dl` is not the right type.")

        self('begin_get_preds')
        self.iters = len(self.dl)
        with torch.no_grad():
            for i, (xb, yb) in enumerate(self.dl):
                self.iter = i
                self.xb, self.yb = xb, yb;                      self('begin_batch')
                self.pred = self.model(self.xb);                self('after_pred')
                self.loss = self.loss_func(self.pred, self.yb); self('after_loss')
                # record actual predictions if record_preds is True
                if record_preds:
                    current_Y = self.yb.cpu().numpy().squeeze()
                    current_Y_hat = self.pred.cpu().numpy().squeeze()
                    # we need this for classification: Y_hat is a tensor of logits
                    current_Y_hat = current_Y_hat if len(current_Y_hat.shape)<=1 else \
                                    np.argmax(current_Y_hat, axis=1)
                    current_preds_df = pd.DataFrame({#'X':self.xb.cpu().numpy(),
                                                    'Y':current_Y,
                                                    'Y_hat':current_Y_hat},
                                                    index=range(len(current_Y)))
                    self.pred_df = pd.concat([self.pred_df, current_preds_df],
                                            ignore_index=True)
                self('after_batch')
        self('end_get_preds')
        self('after_get_preds')

        self.remove_callbacks(get_preds_callbacks)

    def get_valid_preds(self, record_preds=False):
        return self._get_preds(valid_preds=True, record_preds=record_preds)

    def get_train_preds(self, record_preds=False):
        return self._get_preds(valid_preds=False, record_preds=record_preds)

    def get_new_preds(self, new_dl, record_preds=False):
        return self._get_preds(new_dl=new_dl, record_preds=record_preds)

    def __call__(self, callback_name):
        results = False
        assert callback_name in self.ALL_CALLBACKS
        for callback in sorted(self.callbacks, key=lambda x: x._order):
            results = callback(callback_name) and results
        return results
