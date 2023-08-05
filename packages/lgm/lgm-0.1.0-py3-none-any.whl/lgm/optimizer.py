import torch
from functools import partial
from .utils import listify, compose

def maybe_update(sources, destination, func):
    """
    Updates defaults (values) in destination with values from func
    applied to sources, only if defaults (values) not already specified.
    """
    for source in sources:
        for key, value in func(source).items():
            if key not in destination:
                destination[key] = value

def get_defaults(default):
    return getattr(default, '_defaults', {})

class Optimizer():
    """
    param_groups is assumed to be a list of lists for discriminative learning rates.
    hypers are hyperparams for each param group (each list in the list of lists).
    """
    def __init__(self, param_groups, steppers, **defaults):
        self.steppers = listify(steppers)
        maybe_update(self.steppers, defaults, get_defaults)
        # might be a generator
        self.param_groups = list(param_groups)
        # ensure param_groups is a list of lists
        if not isinstance(self.param_groups[0], list):
            self.param_groups = [self.param_groups]
        # list of dicts of hyperparams, one dict per param group;
        # each dict clones the provided **defaults
        self.hypers = [{**defaults} for param_group in self.param_groups]

    def grad_params(self):
        "Return list of (param, hyper) tuples if param has gradient."
        param_hyper_list = []
        for param_group, hyper in zip(self.param_groups, self.hypers):
            for param in param_group:
                if param.grad is not None:
                    param_hyper_list.append((param, hyper))
        return param_hyper_list

    def zero_grad(self):
        for param, hyper in self.grad_params():
            param.grad.detach_()
            param.grad.zero_()

    def step(self):
        for param, hyper in self.grad_params():
            compose(param, self.steppers, **hyper)

def sgd_step(param, lr, **kwargs):
    "Example stepper for use with Optimizer."
    param.data.add_(-lr, param.grad.data)
    return param
# sgd_step._defaults = dict(lr=1e-1)

def weight_decay(param, lr, weight_decay_param, **kwargs):
    "Update with gradient of L2 regularizer with weight_decay_param."
    param.data.mul_(1 - lr * weight_decay_param)
    return param
weight_decay._defaults = dict(weight_decay_param=0.)

# alternatively
# def l2_reg(param, lr, weight_decay_param, **kwargs):
    # param.grad.data.add_(weight_decay_param, param.data)
    # return param
# l2_reg._defaults = dict(weight_decay_param=0.)

# SGD optimizer with weight decay
sgd_opt = partial(Optimizer, steppers=[weight_decay, sgd_step])

# To inspect the hyperparams of the optimizer:
# opt = sgd_opt(learn.model.parameters(), lr=1e-1, weight_decay_param=1e-4)
# print(opt.hypers)

class StatefulOptimizer(Optimizer):
    """
    Optimizer with state for momentum.
    We assemble the relevant state with the stats argument.
    """
    def __init__(self, param_groups, steppers, stats=None, **defaults):
        self.stats = listify(stats)
        maybe_update(self.stats, defaults, get_defaults)
        super().__init__(param_groups, steppers, **defaults)
        self.state = {}

    def step(self):
        for param, hyper in self.grad_params():
            if param not in self.state:
                #Create a state for param and call all the statistics to initialize it.
                self.state[param] = {}
                maybe_update(self.stats, self.state[param],
                             lambda grad_stat: grad_stat.init_state(param))
            state = self.state[param]
            for stat in self.stats:
                state = stat.update(param, state, **hyper)
            compose(param, self.steppers, **state, **hyper)
            self.state[param] = state

class Stat():
    "Base class used to assemble state for StatefulOptimizer."
    _defaults = {}
    def init_state(self, param):
        raise NotImplementedError
    def update(self, param, state, **kwargs):
        raise NotImplementedError

class AverageGrad(Stat):
    "Assembles state for momentum."
    _defaults = dict(mom=0.9)
    def __init__(self, dampening=True):
        self.dampening = dampening

    def init_state(self, param):
        return {'grad_avg': torch.zeros_like(param.grad.data)}

    def update(self, param, state, mom, **kwargs):
        state['mom_damp'] = 1 - mom if self.dampening else 1.
        # the update below is just the definition of momentum
        state['grad_avg'].mul_(mom).add_(state['mom_damp'],
                                         param.grad.data)
        return state

def momentum_step(param, lr, grad_avg, **kwargs):
    param.data.add_(-lr, grad_avg)
    return param

sgd_mom_opt = partial(StatefulOptimizer,
                      steppers=[momentum_step, weight_decay],
                      stats=AverageGrad(dampening=False),
                      weight_decay_param=1e-2)

class AverageSqrGrad(Stat):
    _defaults = dict(sqr_mom=0.99)
    def __init__(self, dampening=True):
        self.dampening = dampening

    def init_state(self, param):
        return {'sqr_avg': torch.zeros_like(param.grad.data)}

    def update(self, param, state, sqr_mom, **kwargs):
        state['sqr_damp'] = 1 - sqr_mom if self.dampening else 1.
        state['sqr_avg'].mul_(sqr_mom).addcmul_(state['sqr_damp'],
                                                param.grad.data,
                                                param.grad.data)
        return state

class StepCount(Stat):
    def init_state(self, param):
        return {'step': 0}

    def update(self, param, state, **kwargs):
        state['step'] += 1
        return state

def debias(mom, damp, step):
    return damp * (1 - mom**step) / (1 - mom)

def adam_step(param, lr, mom, mom_damp, step, sqr_mom, sqr_damp,
              grad_avg, sqr_avg, eps, **kwargs):
    debias_mom = debias(mom, mom_damp, step)
    debias_sqr_mom = debias(sqr_mom, sqr_damp, step)
    param.data.addcdiv_(-lr / debias_mom, grad_avg,
                        (sqr_avg/debias_sqr_mom).sqrt() + eps)
    return param
adam_step._defaults = dict(eps=1e-5)

def adam_opt(extra_step=None, **kwargs):
    return partial(StatefulOptimizer,
                   steppers = [adam_step, weight_decay] + listify(extra_step),
                   stats = [AverageGrad(), AverageSqrGrad(), StepCount()],
                   **kwargs)
