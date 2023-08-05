import torch
import warnings
import torch.nn.functional as F
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

def dropout_mask(x, size, prob):
    """
    We pass size in so that we get broadcasting along the sequence dimension
    in RNNDropout.
    """
    return x.new(*size).bernoulli_(1-prob).div_(1-prob)

class RNNDropout(nn.Module):
    """
    Note the way size is passed in the forward function: we insert a 3rd
    dimension in between the width and height of the minibatch:
    (x.size(0), 1, x.size(2)).
    The middle dimension is the sequence dimension, so the zeroed-out positions
    will stay the same along the sequence, i.e., througout the bptt sequence.
    """
    def __init__(self, prob=0.5):
        super().__init__()
        self.prob = prob

    def forward(self, x):
        if not self.training or self.prob == 0.:
            return x
        mask = dropout_mask(x.data, (x.size(0), 1, x.size(2)), self.prob)
        return x * mask

class WeightDropout(nn.Module):
    """
    Dropout to the weights (not activations!) of the inner LSTM hidden to
    hidden matrix. We want to preserve the CuDNN speed and not reimplement
    the cell from scratch, so in __init__, we add a parameter that will
    contain the raw weights f'{layer}_raw'. We then replace the weight matrix
    in the LSTM in forward when we call self._setweights()
    """
    def __init__(self, inner_module, weight_prob=[0.], layer_names=['weight_hh_l0']):
        super().__init__()
        self.inner_module = inner_module
        self.weight_prob = weight_prob
        self.layer_names = layer_names
        for layer in self.layer_names:
            # we make a copy of the weights of the selected layers
            weights = getattr(self.inner_module, layer)
            self.register_parameter(f'{layer}_raw', nn.Parameter(weights.data))
            # we apply dropout to the actual weights since we are doing dropout
            # after all, but the forward method will use raw_weights
            self.inner_module._parameters[layer] = F.dropout(weights,
                                                             p=self.weight_prob,
                                                             training=False)

    def _setweights(self):
        "Apply dropout to raw_weights and set them as the layer weights."
        for layer in self.layer_names:
            raw_weights = getattr(self, f'{layer}_raw')
            self.inner_module._parameters[layer] = F.dropout(raw_weights,
                                                             p=self.weight_prob,
                                                             training=self.training)

    def forward(self, *args):
        self._setweights()
        with warnings.catch_warnings():
            # To avoid the warning that comes because the weights aren't flattened.
            warnings.simplefilter("ignore")
            return self.inner_module.forward(*args)

class EmbeddingDropout(nn.Module):
    """
    Applies dropout in the embedding layer by zeroing out some elements of
    the embedding vector. Dropout is applied to full rows of the embedding
    matrix: we drop out entire words and not components of a word's dense
    embedding.
    """
    def __init__(self, emb, embed_prob):
        super().__init__()
        self.emb = emb
        self.embed_prob = embed_prob
        self.pad_idx = self.emb.padding_idx
        if self.pad_idx is None:
            self.pad_idx = -1

    def forward(self, words, scale=None):
        if self.training and self.embed_prob != 0:
            size = (self.emb.weight.size(0), 1)
            mask = dropout_mask(self.emb.weight.data, size, self.embed_prob)
            masked_embed = self.emb.weight * mask
        else:
            masked_embed = self.emb.weight
        if scale:
            masked_embed.mul_(scale)
        return F.embedding(words, masked_embed, self.pad_idx, self.emb.max_norm,
                           self.emb.norm_type, self.emb.scale_grad_by_freq,
                           self.emb.sparse)

def to_detach(h):
    "Detaches h from its gradient history."
    return h.detach() if type(h) == torch.Tensor else tuple(to_detach(v) for v in h)

class AWD_LSTM(nn.Module):
    "AWD-LSTM inspired by https://arxiv.org/abs/1708.02182."
    initrange=0.1

    def __init__(self, vocab_size, emb_dim, hidden_dim, n_layers, pad_token,
                 hidden_prob=0.2, input_prob=0.6, embed_prob=0.1, weight_prob=0.5):
        super().__init__()
        self.batch_size = 1
        self.emb_dim = emb_dim
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.emb = nn.Embedding(vocab_size, emb_dim, padding_idx=pad_token)
        self.emb_dropout = EmbeddingDropout(self.emb, embed_prob)
        # we create n_layers of LSTMs
        self.rnns = [nn.LSTM(emb_dim if l == 0 else hidden_dim,
                             (hidden_dim if l != n_layers-1 else emb_dim),
                             1, batch_first=True)
                     for l in range(n_layers)]
        # we add dropout to the LSTM layers
        self.rnns = nn.ModuleList([WeightDropout(rnn, weight_prob)
                                   for rnn in self.rnns])
        self.emb.weight.data.uniform_(-self.initrange, self.initrange)
        self.input_dropout = RNNDropout(input_prob)
        self.hidden_dropouts = nn.ModuleList([RNNDropout(hidden_prob)
                                              for l in range(n_layers)])

    def forward(self, input):
        batch_size, seq_len = input.size()
        if batch_size != self.batch_size:
            self.batch_size = batch_size
            self.reset()
        raw_output = self.input_dropout(self.emb_dropout(input))
        new_hidden, raw_outputs, outputs = [], [], []
        # we loop through the LSTM layers (plus the hidden dropout layers)
        for l, (rnn, hid_dropout) in enumerate(zip(self.rnns, self.hidden_dropouts)):
            raw_output, new_h = rnn(raw_output, self.hidden[l])
            new_hidden.append(new_h)
            raw_outputs.append(raw_output)
            # we do hidden dropout for all layers but the last one
            if l != self.n_layers - 1: raw_output = hid_dropout(raw_output)
            outputs.append(raw_output)
        self.hidden = to_detach(new_hidden)
        return raw_outputs, outputs

    def _one_hidden(self, l):
        "Return one hidden state."
        nh = self.hidden_dim if l != self.n_layers - 1 else self.emb_dim
        return next(self.parameters()).new(1, self.batch_size, nh).zero_()

    def reset(self):
        "Reset (zero out) the hidden states."
        self.hidden = [(self._one_hidden(l), self._one_hidden(l))
                       for l in range(self.n_layers)]

class LinearDecoder(nn.Module):
    """
    We add a top layer to the AWD LSTM. This is a linear model with dropout.
    """
    def __init__(self, n_out, hidden_dim, output_prob, tie_encoder=None, bias=True):
        super().__init__()
        self.output_dropout = RNNDropout(output_prob)
        self.decoder = nn.Linear(hidden_dim, n_out, bias=bias)
        if bias:
            self.decoder.bias.data.zero_()
        if tie_encoder:
            self.decoder.weight = tie_encoder.weight
        else:
            init.kaiming_uniform_(self.decoder.weight)

    def forward(self, input):
        raw_outputs, outputs = input
        # we call dropout first
        output = self.output_dropout(outputs[-1]).contiguous()
        # we call the linear model
        decoded = self.decoder(output.view(output.size(0)*output.size(1),
                                           output.size(2)))
        return decoded, raw_outputs, outputs

class SequentialRNN(nn.Sequential):
    "A sequential module that passes the reset call to its children."
    def reset(self):
        for child in self.children():
            if hasattr(child, 'reset'): child.reset()

def get_language_model(vocab_size, emb_dim, hidden_dim, n_layers, pad_token,
                       output_prob=0.4, hidden_prob=0.2, input_prob=0.6,
                       embed_prob=0.1, weight_prob=0.5, tie_weights=True, bias=True):
    rnn_enc = AWD_LSTM(vocab_size, emb_dim, hidden_dim=hidden_dim, n_layers=n_layers,
                       pad_token=pad_token, hidden_prob=hidden_prob,
                       input_prob=input_prob, embed_prob=embed_prob,
                       weight_prob=weight_prob)
    enc = rnn_enc.emb if tie_weights else None
    # the rnn_enc is the AWD LSTM
    # its output is passed to the top linear layer (with dropout)
    return SequentialRNN(rnn_enc,
                         LinearDecoder(vocab_size, emb_dim, output_prob,
                                       tie_encoder=enc, bias=bias))

def lm_splitter(model):
    """
    Splits the language model provided by the get_language_model into multiple
    param groups to do transfer learning (e.g., from Wikipedia to IMDB):
    -- we have one group for each rnn + corresponding dropout, for a
    total of 2 if we had n_layers = 2 in the get_language_model call;
    -- we have one final group that contains the embeddings/decoder.
    The final group needs to be trained the most (new embedding vectors).
    """
    groups = []
    for i in range(len(model[0].rnns)):
        groups.append(nn.Sequential(model[0].rnns[i], model[0].hidden_dropouts[i]))
    groups += [nn.Sequential(model[0].emb, model[0].emb_dropout, model[0].input_dropout, model[1])]
    return [list(group.parameters()) for group in groups]

class AWD_LSTM1(nn.Module):
    """
    AWD-LSTM inspired by https://arxiv.org/abs/1708.02182,
    updated to deal with pad_packed_sequence and pack_padded_sequence.
    """
    initrange=0.1

    def __init__(self, vocab_size, emb_dim, hidden_dim, n_layers, pad_token,
                 hidden_prob=0.2, input_prob=0.6, embed_prob=0.1, weight_prob=0.5):
        super().__init__()
        self.batch_size = 1
        self.emb_dim = emb_dim
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.pad_token = pad_token
        self.emb = nn.Embedding(vocab_size, emb_dim, padding_idx=pad_token)
        self.emb_dropout = EmbeddingDropout(self.emb, embed_prob)
        # we create n_layers of LSTMs
        self.rnns = [nn.LSTM(emb_dim if l == 0 else hidden_dim,
                             (hidden_dim if l != n_layers - 1 else emb_dim),
                             1, batch_first=True)
                     for l in range(n_layers)]
        self.rnns = nn.ModuleList([WeightDropout(rnn, weight_prob)
                                   for rnn in self.rnns])
        self.emb.weight.data.uniform_(-self.initrange, self.initrange)
        self.input_dropout = RNNDropout(input_prob)
        self.hidden_dropouts = nn.ModuleList([RNNDropout(hidden_prob)
                                              for l in range(n_layers)])

    def forward(self, input):
        batch_size, seq_len = input.size()
        if batch_size != self.batch_size:
            self.batch_size = batch_size
            self.reset()
        mask = (input == self.pad_token)
        lengths = seq_len - mask.long().sum(1)
        n_empty = (lengths == 0).sum()
        if n_empty > 0:
            input = input[:-n_empty]
            lengths = lengths[:-n_empty]
            self.hidden = [(h[0][:, :input.size(0)], h[1][:, :input.size(0)])
                           for h in self.hidden]
        raw_output = self.input_dropout(self.emb_dropout(input))
        new_hidden, raw_outputs, outputs = [], [], []
        for l, (rnn, hid_dropout) in enumerate(zip(self.rnns, self.hidden_dropouts)):
            # take data of different lengths and shape it to pass to RNN
            raw_output = pack_padded_sequence(raw_output, lengths, batch_first=True)
            raw_output, new_h = rnn(raw_output, self.hidden[l])
            # this is where the padding actually happens
            raw_output = pad_packed_sequence(raw_output, batch_first=True)[0]
            raw_outputs.append(raw_output)
            # we do hidden dropout for all layers but the last one
            if l != self.n_layers - 1: raw_output = hid_dropout(raw_output)
            outputs.append(raw_output)
            new_hidden.append(new_h)
        self.hidden = to_detach(new_hidden)
        return raw_outputs, outputs, mask

    def _one_hidden(self, l):
        "Return one hidden state."
        nh = self.hidden_dim if l != self.n_layers - 1 else self.emb_dim
        return next(self.parameters()).new(1, self.batch_size, nh).zero_()

    def reset(self):
        "Reset (zero out) the hidden states."
        self.hidden = [(self._one_hidden(l), self._one_hidden(l)) for l in range(self.n_layers)]

class Pooling(nn.Module):
    """
    This is just a pedagogically useful model. The actual pooling classifier is
    provided in PoolingLinearClassifier below.
    The LSTMs create hidden states for bptt time steps. We decide what to pass
    to the classifier here. Following concat pooling from vision, we use three
    things for the classification head of the model. We concatenate:
    -- the last hidden state
    -- the average (mean) pool of all the bptt hidden states
    -- the max pool of all the bptt hidden states
    We pass the resulting concatenated tensor to the classifier.
    """
    def forward(self, input):
        raw_outputs, outputs, mask = input
        # last hidden state
        output = outputs[-1]
        # once again, we need to ignore the padding in the last hidden state,
        # as well as the average pool and max pool tensors
        lengths = output.size(1) - mask.long().sum(dim=1)
        # average pool
        avg_pool = output.masked_fill(mask[:, :, None], 0).sum(dim=1)
        avg_pool.div_(lengths.type(avg_pool.dtype)[:, None])
        # max pool
        max_pool = output.masked_fill(mask[:, :, None], -float('inf')).max(dim=1)[0]
        # Concat pooling
        x = torch.cat([output[torch.arange(0, output.size(0)), lengths-1],
                       max_pool, avg_pool], 1)
        return output, x

def batchnorm_dropout_linear(n_in, n_out, batch_norm=True, dropout_prob=0.,
                             activation=None):
    "Creates a list of layers: batchnorm, dropout, linear, activation."
    layers = [nn.BatchNorm1d(n_in)] if batch_norm else []
    if dropout_prob != 0:
        layers.append(nn.Dropout(dropout_prob))
    layers.append(nn.Linear(n_in, n_out))
    if activation is not None:
        layers.append(activation)
    return layers

class PoolingLinearClassifier(nn.Module):
    """
    Create a linear classifier with pooling:
    -- the concat pooling layer, followed by
    -- a list of batchnorm + dropout + linear + activation layers
    """
    def __init__(self, layers, dropout_probs):
        super().__init__()
        modified_layers = []
        activations = [nn.ReLU(inplace=True)] * (len(layers) - 2) + [None]
        # list of batchnorm + dropout + linear layers
        for n_in, n_out, dropout_prob, activation in zip(layers[:-1], layers[1:],
                                                         dropout_probs, activations):
            modified_layers += batchnorm_dropout_linear(n_in, n_out,
                                                        dropout_prob=dropout_prob,
                                                        activation=activation)
        self.layers = nn.Sequential(*modified_layers)

    def forward(self, input):
        """
        The LSTMs create hidden states for bptt time steps. We decide what to pass
        to the classifier here. Following concat pooling from vision, we use three
        things for the classification head of the model. We concatenate:
        -- the last hidden state
        -- the average (mean) pool of all the bptt hidden states
        -- the max pool of all the bptt hidden states
        We pass the resulting concatenated tensor to the linear classifier.
        """
        raw_outputs, outputs, mask = input
        # last hidden state
        output = outputs[-1]
        # we need to ignore the padding in the last hidden state,
        # as well as the average pool and max pool tensors
        lengths = output.size(1) - mask.long().sum(dim=1)
        # average pool
        avg_pool = output.masked_fill(mask[:, :, None], 0).sum(dim=1)
        avg_pool.div_(lengths.type(avg_pool.dtype)[:, None])
        # max pool
        max_pool = output.masked_fill(mask[:, :, None], -float('inf')).max(dim=1)[0]
        # Concat pooling
        x = torch.cat([output[torch.arange(0, output.size(0)), lengths-1],
                       max_pool, avg_pool], 1)
        # pass the concat-pooled tensor through the linear layers
        x = self.layers(x)
        return x

def pad_tensor(t, batch_size, val=0.):
    if t.size(0) < batch_size:
        return torch.cat([t, val + t.new_zeros(batch_size-t.size(0), *t.shape[1:])])
    return t

class SentenceEncoder(nn.Module):
    """
    The encoder is the AWD LSTM model that gets called on the input text.
    We call it on chunks of text of bptt length instead of on the full text.
    """
    def __init__(self, encoder, bptt, pad_idx=1):
        super().__init__()
        self.encoder = encoder
        self.bptt = bptt
        self.pad_idx = pad_idx

    def concat(self, arrs, batch_size):
        return [torch.cat([pad_tensor(l[si],batch_size) for l in arrs], dim=1)
                for si in range(len(arrs[0]))]

    def forward(self, input):
        batch_size, seq_len = input.size()
        self.encoder.batch_size = batch_size
        self.encoder.reset()
        raw_outputs, outputs, masks = [], [], []
        # We go through the input one bptt at a time
        for i in range(0, seq_len, self.bptt):
            # we call the RNN model on it
            r, o, m = self.encoder(input[:,i: min(i+self.bptt, seq_len)])
            # we keep appending the results
            masks.append(pad_tensor(m, batch_size, 1))
            raw_outputs.append(r)
            outputs.append(o)
        return self.concat(raw_outputs, batch_size), self.concat(outputs, batch_size), torch.cat(masks,dim=1)

def get_text_classifier(vocab_size, emb_dim, hidden_dim, n_layers, n_out, pad_token,
                        bptt, output_prob=0.4, hidden_prob=0.2, input_prob=0.6,
                        embed_prob=0.1, weight_prob=0.5, layers=None, dropout_probs=None):
    "To create a full AWD-LSTM"
    rnn_enc = AWD_LSTM1(vocab_size, emb_dim, hidden_dim=hidden_dim, n_layers=n_layers,
                        pad_token=pad_token, hidden_prob=hidden_prob,
                        input_prob=input_prob, embed_prob=embed_prob,
                        weight_prob=weight_prob)
    enc = SentenceEncoder(rnn_enc, bptt)
    if layers is None:
        # we set the dimension(s) of the hidden layers in the decoder,
        # which is a fully connected (multilayer perceptron) network
        layers = [50]
    if dropout_probs is None:
        dropout_probs = [0.1] * len(layers)
    # the decoder takes the concat pool as input (3 * emb_dim) and feeds it
    # through one or more hidden layers; output layer has n_out neurons/units
    layers = [3 * emb_dim] + layers + [n_out]
    dropout_probs = [output_prob] + dropout_probs
    return SequentialRNN(enc, PoolingLinearClassifier(layers, dropout_probs))

def class_splitter(model):
    enc = model[0].encoder
    groups = [nn.Sequential(enc.emb, enc.emb_dropout, enc.input_dropout)]
    for i in range(len(enc.rnns)):
        groups.append(nn.Sequential(enc.rnns[i], enc.hidden_dropouts[i]))
    groups.append(model[1])
    return [list(group.parameters()) for group in groups]
