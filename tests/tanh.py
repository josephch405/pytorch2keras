import keras  # work around segfault
import sys
import numpy as np

import torch
import torch.nn as nn
from torch.autograd import Variable

sys.path.append('../pytorch2keras')
from converter import pytorch_to_keras


class TestTanh(nn.Module):
    """Module for Tanh activation conversion testing
    """

    def __init__(self, inp=10, out=16, bias=True):
        super(TestTanh, self).__init__()
        self.linear = nn.Linear(inp, out, bias=True)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.linear(x)
        x = self.tanh(x)
        return x


if __name__ == '__main__':
    max_error = 0
    for i in range(100):
        inp = np.random.randint(1, 100)
        out = np.random.randint(1, 100)
        model = TestTanh(inp, out, inp % 2)

        input_np = np.random.uniform(-1.0, 1.0, (1, inp))
        input_var = Variable(torch.FloatTensor(input_np))
        output = model(input_var)

        k_model = pytorch_to_keras(model, input_var, (inp,), verbose=True)

        pytorch_output = output.data.numpy()
        keras_output = k_model.predict(input_np)

        error = np.max(pytorch_output - keras_output)
        print(error)
        if max_error < error:
            max_error = error

    print('Max error: {0}'.format(max_error))
