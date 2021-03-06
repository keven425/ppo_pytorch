import torch
import numpy as np
from scipy.special import logsumexp


def softmax_p(x):
  e_x = torch.exp(x - torch.max(x, dim=1)[0])
  return e_x / torch.sum(e_x, dim=1)


def softmax_logp(x):
  # log(e^x1 / (e^x1 + e^x2))
  # x1 - log(e^x1 + e^x2)
  # x1 - x1 - log(1 + e^(x2 - x1))
  # -log(1 + e^(x2 - x1))
  x_numerator = x - torch.max(x, dim=1, keepdim=True)[0]
  e_x = torch.exp(x_numerator)
  return x_numerator - torch.log(torch.sum(e_x, dim=1)).view(-1, 1)


def np_softmax_logp(x):
  # log(e^x2 / (e^x1 + e^x2))
  # x2 - log(e^x1 + e^x2)
  # x2 - x1 - log(e^(x1 - x1) + e^(x2 - x1))
  x_numerator = x - np.max(x, axis=1, keepdims=True)
  e_x = np.exp(x_numerator)
  return x_numerator - np.log(np.sum(e_x, axis=1)).reshape([-1, 1])


if __name__ == '__main__':
  x = np.array([[1., 2.], [2., 3.], [3., 4.]])
  logp = np_softmax_logp(x)
  print(str(logp))