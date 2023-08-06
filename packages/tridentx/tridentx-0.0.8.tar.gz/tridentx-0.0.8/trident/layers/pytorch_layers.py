from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
from functools import partial
import torch

from torch.nn import Module,BatchNorm2d
from torch.nn import init
from torch.nn.parameter import Parameter
import torch.nn.functional as F  # import torch functions
from torch._six import container_abcs
from torch._jit_internal import List
from itertools import repeat

from ..backend.common import get_session,gcd,get_divisors,isprime,next_prime,prev_prime,nearest_prime
from .pytorch_activations import get_activation
from .pytorch_normalizations import get_normalization
import numpy as np
__all__ = ['Flatten','Conv1d','Conv2d','Conv3d','TransConv1d','TransConv2d','TransConv3d','SeparableConv2d','GcdConv2d','GcdConv2d_1','Lambda','Reshape','CoordConv2d']

_session = get_session()
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_epsilon=_session.epsilon

def _ntuple(n):
    def parse(x):
        if isinstance(x, container_abcs.Iterable):
            if len(x)==n:
                return x
            else:
                return _ntuple(n-len(x))(1)+x
        return tuple(repeat(x, n))

    return parse


_single = _ntuple(1)
_pair = _ntuple(2)
_triple = _ntuple(3)
_quadruple = _ntuple(4)


class Flatten(Module):
    r"""Flatten layer to flatten a tensor after convolution."""

    def forward(self,  # type: ignore
                x: torch.Tensor) -> torch.Tensor:
        return x.view(x.size()[0], -1)

_gcd=gcd
_get_divisors=get_divisors
_isprime=isprime



class _ConvNd(Module):
    __constants__ = ['kernel_size','num_filters','strides','auto_pad','activation', 'padding', 'use_bias', 'dilation', 'groups']

    def __init__(self, kernel_size, num_filters, strides, auto_pad, use_bias, dilation,groups,   transposed, **kwargs):
        super(_ConvNd, self).__init__()

        self.num_filters = kwargs['out_channels'] if 'out_channels' in kwargs else num_filters
        self.input_filters=None
        self.kernel_size = kernel_size
        self.padding = 0  # padding if padding is not None else 0in_channel
        self.strides = kwargs['stride'] if 'stride' in kwargs else strides
        self.auto_pad = auto_pad
        self.dilation = dilation
        self.transposed = transposed
        self.groups = groups
        self.init =kwargs.get('init',None)
        self.init_bias =kwargs.get('init_bias',0)

        self.transposed = transposed
        self.padding_mode =kwargs.get('padding_mode','replicate')
        self._is_built = False
        self.weight = None
        self.use_bias = use_bias
        self.weights_constraint=kwargs.get('weights_constraint',None)




        if 'in_channels' in kwargs:
            self.input_filters = kwargs['in_channels']
            self.build_once(self.input_filters)

        if self.input_filters is not None and self.input_filters % groups != 0:
            raise ValueError('in_channels must be divisible by groups')
        # if self.num_filters % groups != 0:
        #     raise ValueError('out_channels must be divisible by groups')

        self.to(_device)

    def reset_parameters(self):
        if self.init is not None:
            self.init(self.weight)
        else:
            init.kaiming_uniform_(self.weight, mode='fan_in')

        if self.use_bias==True and self.bias is not None:
            if isinstance(self.init_bias,int):
                self.bias.data=np.ones(list(self.bias.size()))*self.init_bias
            else:
                fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
                bound = 1 / math.sqrt(fan_in)
                self.init_bias(self.bias, -bound, bound)

    def build_once(self, input_filters):
        if self._is_built == False:
            if isinstance(input_filters,int) :
                self.input_filters =input_filters
            elif hasattr(input_filters, "__iter__") and  not isinstance(input_filters,str):
                input_filters=list(input_filters)
                if len(input_filters)==1:
                    self.input_filters =input_filters[0]
                else:
                    self.input_filters = input_filters[1]
            if self.transposed:
                self.weight = Parameter(torch.Tensor(self.input_filters, self.num_filters // self.groups, *self.kernel_size))
            else:
                self.weight = Parameter(torch.Tensor(self.num_filters, self.input_filters // self.groups, *self.kernel_size))  #

            if self.use_bias:
                self.bias = Parameter(torch.Tensor(self.num_filters))
            else:
                self.register_parameter('bias', None)
            self.reset_parameters()

            self.to(_device)
            self._is_built = True
    #
    def extra_repr(self):
        s = ( 'kernel_size={kernel_size}, {num_filters}, strides={strides}, activation={activation}, auto_pad={auto_pad} , dilation={dilation}')
    #     if self.groups != 1:
    #         s += ', groups={groups}'
    #     if self.bias is None:
    #         s += ', use_bias=False'
        return s.format(**self.__dict__)

    def __setstate__(self, state):
        super(_ConvNd, self).__setstate__(
            state)  # if not hasattr(self, 'padding_mode'):  #     self.padding_mode = 'zeros'


class Conv1d(_ConvNd):
    def __init__(self, kernel_size, num_filters, strides, auto_pad=True, activation=None,use_bias=False, dilation=1,
                 groups=1,  **kwargs):
        kernel_size = _single(kernel_size)
        strides = _single(strides)
        dilation = _single(dilation)
        super(Conv1d, self).__init__(kernel_size, num_filters, strides, auto_pad, use_bias,
                                     dilation, groups, False, **kwargs)
        self.activation = get_activation(activation)
        if 'padding' in kwargs:
            self.padding = kwargs['padding']
            self.padding = _single(self.padding)
            self.auto_pad = False
        else:
            self.padding = _single(0)

    def conv1d_forward(self, x):
        self.input_filters = x.size(1)
        if self.auto_pad == True:
            iw = x.size()[-1]
            kw = self.weight.size()[-1]
            sw = self.strides[-1]
            dw = self.dilation[-1]
            ow = math.ceil(iw / sw), math.ceil(iw / sw)
            pad_w = max((ow - 1) * sw + (kw - 1) * dw + 1 - iw, 0)
            if pad_w > 0:
                x = F.pad(x, [pad_w // 2, pad_w - pad_w // 2], mode='replicate')
        return F.conv1d(x, self.weight, self.bias, self.strides, self.padding, self.dilation, self.groups)

    def forward(self, x):
        self.build_once(x.shape)
        x = self.conv1d_forward(x)
        if self.activation is not None:
            x = self.activation(x)
        return x

class Conv2d(_ConvNd):
    def __init__(self, kernel_size, num_filters, strides=1, auto_pad=True, activation=None, use_bias=False,  dilation=1, groups=1, **kwargs):
        kernel_size = _pair(kernel_size)
        strides = _pair(strides)
        dilation = _pair(dilation)



        super(Conv2d, self).__init__(kernel_size, num_filters, strides, auto_pad, use_bias,
                                     dilation, groups,  False, **kwargs)
        self.activation=get_activation(activation)

        if 'padding' in kwargs:
            self.padding = kwargs['padding']
            self.padding = _pair(self.padding)
            self.auto_pad = False
        else:
            self.padding = _pair(0)

    def conv2d_forward(self, x):
        self.input_filters = x.size(1)
        if self.auto_pad == True:
            ih, iw = x.size()[-2:]
            kh, kw = self.weight.size()[-2:]
            sh, sw = self.strides[-2:]
            dh, dw = self.dilation[-2:]
            oh, ow = math.ceil(ih / sh), math.ceil(iw / sw)
            pad_h = max((oh - 1) * sh + (kh - 1) * dh + 1 - ih, 0)
            pad_w = max((ow - 1) * sw + (kw - 1) * dw + 1 - iw, 0)
            if pad_h > 0 or pad_w > 0:
                x = F.pad(x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2], mode='replicate')
        return F.conv2d(x, self.weight, self.bias, self.strides, self.padding, self.dilation, self.groups)

    def forward(self, x):
        self.build_once(x.shape)
        x = self.conv2d_forward(x)
        if self.activation is not None:
            x=self.activation(x)
        return x

class Conv3d(_ConvNd):
    def __init__(self, kernel_size, num_filters, strides, auto_pad=True, activation=None,use_bias=False,dilation=1,
                 groups=1,   **kwargs):
        kernel_size = _triple(kernel_size)
        strides = _triple(strides)
        dilation = _triple(dilation)
        super(Conv3d, self).__init__(kernel_size, num_filters, strides, auto_pad, use_bias,
                                     dilation, groups,   False, **kwargs)
        self.activation = get_activation(activation)
        if 'padding' in kwargs:
            self.padding = kwargs['padding']
            self.padding = _triple(self.padding)
            self.auto_pad = False
        else:
            self.padding = _triple(0)

    def conv3d_forward(self, x):
        self.input_filters = x.size(1)
        if self.auto_pad == True:
            iz,ih, iw = x.size()[-3:]
            kz,kh, kw = self.kernel_size[-3:]
            sz,sh, sw = self.strides[-3:]
            dz,dh, dw = self.dilation[-3:]
            oz,oh, ow =math.ceil(iz / sz), math.ceil(ih / sh), math.ceil(iw / sw)
            pad_z = max((oz - 1) * sz + (kz - 1) * dz + 1 - iz, 0)
            pad_h = max((oh - 1) * sh + (kh - 1) * dh + 1 - ih, 0)
            pad_w = max((ow - 1) * sw + (kw - 1) * dw + 1 - iw, 0)
            if  pad_z > 0 or pad_h > 0 or pad_w > 0:
                x = F.pad(x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2,pad_z // 2, pad_z - pad_z // 2], mode='replicate')
        return F.conv3d(x, self.weight, self.bias, self.strides, self.padding, self.dilation, self.groups)

    def forward(self, x):
        self.build_once(x.shape)
        x = self.conv3d_forward(x)
        if self.activation is not None:
            x = self.activation(x)
        return x

class TransConv1d(_ConvNd):
    def __init__(self, kernel_size, num_filters, strides, auto_pad=True, activation=None, use_bias=False,  dilation=1,
                 groups=1,  **kwargs):
        kernel_size = _single(kernel_size)
        strides = _single(strides)
        dilation = _single(dilation)
        super(TransConv1d, self).__init__(kernel_size, num_filters, strides, auto_pad, use_bias, dilation, groups,True, **kwargs)
        self.activation = get_activation(activation)

        if 'padding' in kwargs:
            self.padding = kwargs['padding']
            self.padding = _single(self.padding)
            self.auto_pad = False
        else:
            self.padding = _single(0)

    def conv1d_forward(self, x):
        self.input_filters = x.size(1)
        if self.auto_pad == True:
            iw = x.size()[-1]
            kw = self.kernel_size[-1]
            sw = self.strides[-1]
            dw = self.dilation[-1]
            ow = math.ceil(iw / sw), math.ceil(iw / sw)
            pad_w = max((ow - 1) * sw + (kw - 1) * dw + 1 - iw, 0)
            if pad_w > 0:
                self.padding = [pad_w ]
                self.output_padding = [1]
        return F.conv_transpose1d(x, self.weight, self.bias, self.strides, padding=self.padding, dilation=self.dilation, groups=self.groups)

    def forward(self, x):
        self.build_once(x.shape)
        x = self.conv1d_forward(x)
        if self.activation is not None:
            x = self.activation(x)
        return x

class TransConv2d(_ConvNd):
    def __init__(self, kernel_size, num_filters, strides=1, auto_pad=True, activation=None, use_bias=False,  dilation=1, groups=1, **kwargs):
        kernel_size = _pair(kernel_size)
        strides = _pair(strides)
        dilation = _pair(dilation)

        super(TransConv2d, self).__init__(kernel_size, num_filters, strides, auto_pad, use_bias,
                                     dilation, groups,True, **kwargs)
        self.activation=get_activation(activation)

        if 'padding' in kwargs:
            self.padding = kwargs['padding']
            self.padding = _pair(self.padding)
            self.auto_pad = False
        else:
            self.padding = _pair(0)

    def conv2d_forward(self, x):
        self.input_filters = x.size(1)
        if self.auto_pad == True:
            ih, iw = x.size()[-2:]
            kh, kw = self.kernel_size[-2:]
            sh, sw = self.strides[-2:]
            dh, dw = self.dilation[-2:]
            oh, ow = math.ceil(ih / sh), math.ceil(iw / sw)
            pad_h = max((oh - 1) * sh + (kh - 1) * dh + 1 - ih, 0)
            pad_w = max((ow - 1) * sw + (kw - 1) * dw + 1 - iw, 0)
            if pad_h > 0 or pad_w > 0:
                self.padding = [pad_w , pad_h ]
                self.output_padding = [1, 1]
        return F.conv_transpose2d(x, self.weight, self.bias, self.strides, padding=self.padding, output_padding=self.output_padding,dilation=self.dilation, groups=self.groups)

    def forward(self, x):
        self.build_once(x.shape)
        x = self.conv2d_forward(x)
        if self.activation is not None:
            x=self.activation(x)
        return x

class TransConv3d(_ConvNd):
    def __init__(self, kernel_size, num_filters, strides, auto_pad=True, activation=None,use_bias=False,  dilation=1, groups=1,   **kwargs):
        kernel_size = _triple(kernel_size)
        strides = _triple(strides)
        dilation = _triple(dilation)
        super(TransConv3d, self).__init__(kernel_size, num_filters, strides, auto_pad,use_bias,   dilation, groups,  True, **kwargs)
        if 'padding' in kwargs:
            self.padding = kwargs['padding']
            self.padding = _triple(self.padding)
            self.auto_pad = False
        else:
            self.padding = _triple(0)

    def conv3d_forward(self, x):
        self.input_filters = x.size(1)
        if self.auto_pad == True:
            iz,ih, iw = x.size()[-3:]
            kz,kh, kw = self.kernel_size[-3:]
            sz,sh, sw = self.strides[-3:]
            dz,dh, dw = self.dilation[-3:]
            oz,oh, ow =math.ceil(iz / sz), math.ceil(ih / sh), math.ceil(iw / sw)
            pad_z = max((oz - 1) * sz + (kz - 1) * dz + 1 - iz, 0)
            pad_h = max((oh - 1) * sh + (kh - 1) * dh + 1 - ih, 0)
            pad_w = max((ow - 1) * sw + (kw - 1) * dw + 1 - iw, 0)

            if pad_z > 0 or pad_h > 0 or pad_w > 0:
                self.padding = [pad_z , pad_w , pad_h ]
                self.output_padding = [1, 1,1]
        return F.conv_transpose3d(x, self.weight, self.bias, self.strides, padding=self.padding ,output_padding=self.output_padding, dilation=self.dilation, groups=self.groups)

    def forward(self, x):
        self.build_once(x.shape)
        x = self.conv3d_forward(x)
        if self.activation is not None:
            x = self.activation(x)
        return x

class SeparableConv1d(Module):
    def __init__(self, kernel_size, num_filters, depth_multiplier=1,strides=1, auto_pad=True, activation=None, use_bias=False,  dilation=1, groups=1, **kwargs):
        super(SeparableConv1d, self).__init__()
        self.kernel_size = _single(kernel_size)
        self.num_filters = num_filters
        self.depth_multiplier = 1
        self.dilation = _single(dilation)
        self.strides = _single(strides)
        self.use_bias = use_bias
        self.conv1 = None
        self.pointwise = None

    def forward(self, x):
        if self.conv1 is None:
            input_filters=x.size(1)
            self.conv1 = torch.nn.Conv1d(input_filters, self.num_filters, kernel_size=self.kernel_size, stride=self.strides,padding=0, dilation=self.dilation, groups=x.size(1), bias=self.use_bias)
            self.pointwise = torch.nn.Conv1d(self.num_filters, self.num_filters, 1, 1, 0, 1, 1, bias=self.use_bias)
        x = self.conv1(x)
        x = self.pointwise(x)
        return x
class SeparableConv2d(Module):
    def __init__(self, kernel_size, num_filters, depth_multiplier=1,strides=1, auto_pad=True, activation=None, use_bias=False,  dilation=1, groups=1, **kwargs):
        super(SeparableConv2d, self).__init__()
        self.kernel_size = _pair(kernel_size)
        self.num_filters = num_filters
        self.depth_multiplier = 1
        self.dilation = _pair(dilation)
        self.strides = _pair(strides)
        self.use_bias = use_bias
        self.conv1 = None
        self.pointwise = None

    def forward(self, x):
        if self.conv1 is None:
            self.conv1 = torch.nn.Conv2d(x.size(1), self.num_filters, kernel_size=self.kernel_size, stride=self.strides,padding=0, dilation=self.dilation, groups=x.size(1), bias=self.use_bias)
            self.pointwise = torch.nn.Conv2d(x.size(1), self.num_filters, 1, 1, 0, 1, 1, bias=self.use_bias)
        x = self.conv1(x)
        x = self.pointwise(x)
        return x
class SeparableConv3d(Module):
    def __init__(self, kernel_size, num_filters, depth_multiplier=1,strides=1, auto_pad=True, activation=None, use_bias=False,  dilation=1, groups=1, **kwargs):
        super(SeparableConv3d, self).__init__()
        self.kernel_size = _triple(kernel_size)
        self.num_filters = num_filters
        self.depth_multiplier = 1
        self.dilation = _triple(dilation)
        self.strides = _triple(strides)
        self.use_bias = use_bias
        self.conv1 = None
        self.pointwise = None

    def forward(self, x):
        if self.conv1 is None:
            self.conv1 = torch.nn.Conv2d(x.size(1), self.num_filters, kernel_size=self.kernel_size, stride=self.strides,padding=0, dilation=self.dilation, groups=x.size(1), bias=self.use_bias)
            self.pointwise = torch.nn.Conv2d(x.size(1), self.num_filters, 1, 1, 0, 1, 1, bias=self.use_bias)
        x = self.conv1(x)
        x = self.pointwise(x)
        return x


class GcdConv2d(Module):
    def __init__(self, kernel_size, num_filters, strides, auto_pad=True, activation=None,use_bias=False,
                 dilation=1, divisor_rank=0, self_norm=True, is_shuffle=False,  **kwargs):
        super(GcdConv2d, self).__init__()
        self.kernel_size = kernel_size
        self.num_filters = num_filters
        self.input_filters = None
        self.strides = _pair(strides)
        self.auto_pad = auto_pad

        self.activation = get_activation(activation)
        self.dilation = dilation
        self.self_norm = self_norm
        self.is_shuffle = is_shuffle
        self.use_bias = use_bias
        self.divisor_rank = divisor_rank

        self.groups = 1
        self.gcd_conv3d = None
        self._is_built= False


    def calculate_gcd(self):
        if self.input_filters is None or not isinstance(self.input_filters,int):
            raise ValueError('in_channels must be integer ')
        gcd_list = gcd(self.input_filters, self.num_filters)
        if len(gcd_list) == 0:
            self.groups = self.input_filters
            self.num_filters_1 = self.input_filters
        else:
            self.gcd = gcd_list[0]
            self.groups = gcd_list[min(int(self.divisor_rank), len(gcd_list))]

        if self.input_filters == self.num_filters or self.input_filters == self.gcd or self.num_filters == self.gcd:
            self.groups = gcd_list[min(int(self.divisor_rank + 1), len(gcd_list))]


    def build_once(self, input_filters):
        if self._is_built == False or self.gcd_conv3d is None:
            if isinstance(input_filters, int):
                self.input_filters = input_filters
            elif hasattr(input_filters, "__iter__") and not isinstance(input_filters, str):
                input_filters = list(input_filters)
                if len(input_filters) == 1:
                    self.input_filters = input_filters[0]
                else:
                    self.input_filters = input_filters[1]
            self.calculate_gcd()
            print('input:{0} -> output:{1}   {2}  {3}  gcd:{4} group:{5}   通道縮放倍數:{5} '.format(self.input_filters,
                                                                                               self.num_filters,
                                                                                               self.input_filters //self.groups,
                                                                                               self.num_filters //self.groups,
                                                                                               self.gcd, self.groups,
                                                                                               self.num_filters /
                                                                                               self.num_filters))
            self.channel_kernal=2 if self.groups>3 else 1
            self.channel_dilation=1
            if self.groups>4 :
                self.channel_dilation=2

            self.gcd_conv3d = Conv3d((self.channel_kernal,) + _pair(self.kernel_size), self.num_filters // self.groups,
                                     (1,) + _pair(self.strides), auto_pad=False, activation=None,
                                     use_bias=self.use_bias, dilation=(self.channel_dilation,) + _pair(self.dilation),
                                     groups=1).to(_device)
            self.gcd_conv3d.build_once(self.input_filters // self.groups)
            torch.nn.init.xavier_normal_(self.gcd_conv3d.weight, gain=0.01)
            if self.self_norm == True:
                self.norm = BatchNorm2d(self.num_filters, _epsilon, momentum=0.1, affine=True,track_running_stats=True).to(_device)
                torch.nn.init.ones_(self.norm.weight)
                torch.nn.init.zeros_(self.norm.bias)

            self.to(_device)
            self._is_built = True

    def forward(self, x):
        self.build_once(x.size(1))
        if self.auto_pad:
            ih, iw = x.size()[-2:]
            kh, kw = self.kernel_size[-2:]
            sh, sw = self.strides[-2:]
            dh, dw = _pair(self.dilation)[-2:]
            oh, ow = math.ceil(ih / sh), math.ceil(iw / sw)
            pad_h = max((oh - 1) * sh + (kh - 1) * dh + 1 - ih, 0)
            pad_w = max((ow - 1) * sw + (kw - 1) * dw + 1 - iw, 0)
            if pad_h > 0 or pad_w > 0:
                x = F.pad(x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2], mode='replicate')


        x = x.view(x.size(0), x.size(1) // self.groups, self.groups, x.size(2), x.size(3))
        pad_g = max((self.groups - 1) * 1 + (self.channel_kernal - 1) * self.channel_dilation + 1 - self.groups, 0)
        x = F.pad(x, [0,0,0,0,pad_g // 2, pad_g - pad_g // 2], mode='replicate')

        x = self.gcd_conv3d(x)
        if self.is_shuffle == True:
            x = x.transpose([2,1])
        x = x.view(x.size(0), x.size(1) * x.size(2), x.size(3), x.size(4))
        if self.self_norm == True:
            x = self.norm(x)
        if self.activation is not None:
            x = self.activation(x)
        if torch.isnan(x).any():
            print(self._get_name() + '  nan detected!!')
            raise  ValueError('')
        return x
    def extra_repr(self):
        s = ( 'kernel_size={kernel_size}, {num_filters}, strides={strides}, activation={activation}, auto_pad={auto_pad} , dilation={dilation}')
    #     if self.groups != 1:
    #         s += ', groups={groups}'
    #     if self.bias is None:
    #         s += ', use_bias=False'
        return s.format(**self.__dict__)


class GcdConv2d_1(Module):
    def __init__(self, kernel_size, num_filters, strides, auto_pad=True, activation=None,use_bias=False,
                 divisor_rank=0, dilation=1, self_norm=True, is_shuffle=False,  **kwargs):
        super(GcdConv2d_1, self).__init__()
        self.kernel_size = kernel_size
        self.num_filters = num_filters
        self.input_filters = 3
        self.strides = _pair(strides)
        self.auto_pad = auto_pad

        self.activation = get_activation(activation)
        self.dilation = dilation
        self.self_norm = self_norm
        self.is_shuffle = is_shuffle

        self.use_bias = use_bias

        self.gcd_conv3d = None

        self.divisor_rank = divisor_rank

        self.groups = 1
        self.pointwise = None
        self.input_shape = None
        self.is_shape_inferred = False

    def calculate_gcd(self):
        gcd_list = _gcd(self.input_filters, self.num_filters)
        if len(gcd_list) == 0:
            self.groups = self.input_filters
            self.num_filters_1 = self.input_filters
        else:
            self.gcd = gcd_list[0]
            self.groups = gcd_list[min(int(self.divisor_rank), len(gcd_list))]

            self.num_filters_1 = self.gcd
            self.num_filters_2 = self.num_filters
            factors = _get_divisors(self.num_filters // self.gcd)

        if self.input_filters == self.num_filters or self.input_filters == self.gcd or self.num_filters == self.gcd:
            self.groups = gcd_list[min(int(self.divisor_rank + 1), len(gcd_list))]

    def forward(self, x):
        input_shape = x.size()
        if self.is_shape_inferred == True and self.input_shape[1] != input_shape[1]:
            raise ValueError(
                'You have do dynamic shape inferred once. Current shape {0} channel is not the same with the shape {1} channel'.format(
                    input_shape, self.input_shape))
        elif self.is_shape_inferred == False:
            self.input_filters = x.size(1)
            self.input_shape = input_shape
            self.calculate_gcd()
            print('input:{0}   output:{1}->{2}  gcd:{3} group:{4}   放大因子:{5} '.format(self.input_filters,
                                                                                      self.num_filters_1,
                                                                                      self.num_filters_2, self.gcd,
                                                                                      self.groups,
                                                                                      self.num_filters_1 // self.groups))

            # if _pair(self.kernel_size)==(1,1):
            #     self.gcd_conv3d = nn.Conv3d(self.input_filters // self.groups, self.num_filters // self.groups,
            #                                 (1,) + _pair(self.kernel_size), (1,) + _pair(self.strides), padding=0,
            #                                 dilation=(2, 1, 1), groups=1, bias=False).to(
            #         torch.device("cuda" if torch.cuda.is_available() else "cpu"))
            #
            #     # self.gcd_conv3d = nn.Conv2d(self.input_filters , self.num_filters,
            #     #                              _pair(self.kernel_size), _pair(self.strides), padding=0,
            #     #                             dilation=( 1, 1), groups=1, bias=False).to(
            #     #     torch.device("cuda" if torch.cuda.is_available() else "cpu"))
            # else:
            self.gcd_conv3d = torch.nn.Conv3d(self.input_filters // self.groups, self.num_filters // self.groups,
                                        (2,) + _pair(self.kernel_size), (1,) + _pair(self.strides), padding=(1, 0, 0),
                                        dilation=(2,) + _pair(self.dilation), groups=1, bias=False).to(
                torch.device("cuda" if torch.cuda.is_available() else "cpu"))
            self.add_module('gcd_conv3d', self.gcd_conv3d)
            torch.nn.init.xavier_normal_(self.gcd_conv3d.weight, gain=0.01)
            if self.self_norm == True:
                self.norm = BatchNorm2d(self.num_filters, _session.epsilon, momentum=0.1, affine=True,
                                           track_running_stats=True).to(_device)

                torch.nn.init.ones_(self.norm.weight)
                torch.nn.init.zeros_(self.norm.bias)

            #
            # self.pointwise_conv = nn.Conv2d(self.num_filters, self.num_filters,1,1).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
            # self.add_module('pointwise_conv', self.pointwise_conv)
            # torch.nn.init.xavier_normal_(self.pointwise_conv.weight,gain=0.01)

            self.is_shape_inferred = True

        if self.auto_pad:
            # test_shape=self.group_conv.forward(x).size()
            ih, iw = x.size()[-2:]
            # oh,ow=self.group_conv.forward(x).size()[-2:]
            kh, kw = self.gcd_conv3d.weight.size()[-2:]
            sh, sw = self.strides[-2:]
            dh, dw = _pair(self.dilation)[-2:]
            oh, ow = math.ceil(ih / sh), math.ceil(iw / sw)
            pad_h = max((oh - 1) * sh + (kh - 1) * dh + 1 - ih, 0)
            pad_w = max((ow - 1) * sw + (kw - 1) * dw + 1 - iw, 0)
            if pad_h > 0 or pad_w > 0:
                x = F.pad(x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2], mode='replicate')

        x = x.view(x.size(0), x.size(1) // self.groups, self.groups, x.size(2), x.size(3))
        if torch.isnan(x).any():
            print(self._get_name() + '  nan detected!!')

        if torch.isnan(self.gcd_conv3d.weight).any():
            result = x.cpu().detach().numpy()
            p = self.gcd_conv3d.weight.data.cpu().detach().numpy()
            print('x   mean: {0} max:{1} min:n {2}'.format(result.mean(), result.max(), result.min()))
            print('parameters mean: {0} max:{1} min:n {2}'.format(p.mean(), p.max(), p.min()))
            item = torch.isnan(self.gcd_conv3d.weight).float()
            data = self.gcd_conv3d.weight.data
            data[item == 1] = 1e-8
            self.gcd_conv3d.weight.data = data
            print(self._get_name() + '  nan fix!!')
        x = self.gcd_conv3d(x)
        if torch.isnan(self.gcd_conv3d.weight).any():
            print(self._get_name() + '  nan detected!!')
        x = torch.transpose(x, 1, 2).contiguous()  # N, G,C, H, W

        # x= torch.transpose(x, 1, 2).contiguous()

        # if self.self_norm:
        #     reshape_x=x.view(x.size(0),x.size(1),-1) #N, G,C*H,W
        #     mean =reshape_x.mean(dim=-1, keepdim=True).unsqueeze(-1).unsqueeze(-1).detach() #N, G,1,1,1
        #     std = reshape_x.std(dim=-1, keepdim=True).unsqueeze(-1).unsqueeze(-1).detach()#N, G,1,1,1
        #     x=(x - mean) / (std +_session.epsilon)  #N, G,C, H, W

        if self.is_shuffle == False:
            x = torch.transpose(x, 1, 2).contiguous()  # N, C,G, H, W

        x = x.view(x.size(0), x.size(1) * x.size(2), x.size(3), x.size(4))
        if self.self_norm == True:
            x = self.norm(x)

        if self.activation is not None:
            x = self.activation(x)
        return x


def gcdconv2d(x, kernel_size=(1, 1), num_filters=None, strides=1, padding=0, activation=None, init=None, use_bias=False,
              init_bias=0, divisor_rank=0, dilation=1, weights_constraint=None):
    conv = GcdConv2d(kernel_size=kernel_size, num_filters=num_filters, strides=strides, padding=padding,
                     activation=activation, init=init, use_bias=False, init_bias=0, divisor_rank=divisor_rank,
                     dilation=dilation, weights_constraint=None, padding_mode='zeros', transposed=False)
    return conv(x)


class Lambda(Module):
    """
    Applies a lambda function on forward()
    Args:
        lamb (fn): the lambda function
    """

    def __init__(self, lam):
        super(Lambda, self).__init__()
        self.lam = lam

    def forward(self, x):
        return self.lam(x)


class Reshape(Module):
    """
    Reshape the input volume
    Args:
        *shape (ints): new shape, WITHOUT specifying batch size as first
        dimension, as it will remain unchanged.
    """

    def __init__(self, *shape):
        super(Reshape, self).__init__()
        self.shape = shape

    def forward(self, x):
        return x.view(x.shape[0], *self.shape)



"""
Implementation of the CoordConv modules from https://arxiv.org/abs/1807.03247
"""
def _append_coords(input_tensor, with_r=False):
    batch_size, _, x_dim, y_dim = input_tensor.size()

    xx_channel = torch.arange(x_dim).repeat(1, y_dim, 1)
    yy_channel = torch.arange(y_dim).repeat(1, x_dim, 1).transpose(1, 2)

    xx_channel = xx_channel.float() / (x_dim - 1)
    yy_channel = yy_channel.float() / (y_dim - 1)

    xx_channel = xx_channel * 2 - 1
    yy_channel = yy_channel * 2 - 1

    xx_channel = xx_channel.repeat(batch_size, 1, 1, 1).transpose(2, 3)
    yy_channel = yy_channel.repeat(batch_size, 1, 1, 1).transpose(2, 3)

    ret = torch.cat(
        [
            input_tensor,
            xx_channel.type_as(input_tensor),
            yy_channel.type_as(input_tensor),
        ],
        dim=1,
    )

    if with_r:
        rr = torch.sqrt(
            torch.pow(xx_channel.type_as(input_tensor) - 0.5, 2)
            + torch.pow(yy_channel.type_as(input_tensor) - 0.5, 2)
        )
        ret = torch.cat([ret, rr], dim=1)

    return ret


"""
An alternative implementation for PyTorch with auto-infering the x-y dimensions.
https://github.com/mkocabas/CoordConv-pytorch/blob/master/CoordConv.py
"""



class CoordConv2d(Module):
    def __init__(self,kernel_size, num_filters, strides, auto_pad=True, activation=None, use_bias=False,
                group=1, dilation=1,  with_r=False, **kwargs):
        super().__init__()
        self.addcoords = partial(_append_coords,with_r=with_r)
        self.conv = Conv2d(kernel_size, num_filters, strides, auto_pad=True, activation=None, init=None, use_bias=False,
                 init_bias=0, group=1,dilation=1,   **kwargs)

    def forward(self, x):
        ret = self.addcoords(x)
        ret = self.conv(ret)
        return ret