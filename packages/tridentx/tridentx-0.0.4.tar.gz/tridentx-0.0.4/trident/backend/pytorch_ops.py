import os
import sys
import torch
import torch.nn as nn

import torch.nn.functional as F
from torch.autograd import Variable
from functools import partial
import numpy as np
from backend.common import get_session,addindent,get_time_prefix,get_class
from backend.pytorch_backend import *



def argmax(t:torch.Tensor,axis=1):
    _, idx = t.max(axis)
    return idx

def expand_dims(t:torch.Tensor,axis=0):
    return t.unsqueeze(axis)