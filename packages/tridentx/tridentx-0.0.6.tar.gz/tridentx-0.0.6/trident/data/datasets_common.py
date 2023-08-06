from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
from typing import Iterator, Optional, Sequence, List, TypeVar, Generic, Sized
from backend.common import get_session,get_trident_dir
import threading
import os
import numpy as np
import gzip

from six.moves.urllib.request import urlretrieve
from six.moves.urllib.error import HTTPError
from six.moves.urllib.error import URLError
from six.moves.urllib.request import urlopen


import urllib

import warnings
import time

import threading
import hashlib
import multiprocessing as mp
import os
import random
import shutil
import sys
import tarfile
import threading
import time
import warnings
import zipfile
from abc import abstractmethod
from contextlib import closing
from multiprocessing.pool import ThreadPool
import itertools

import six
from six.moves.urllib.error import HTTPError
from six.moves.urllib.error import URLError
from six.moves.urllib.request import urlopen

try:
    from urllib.request import urlretrieve
except ImportError:
    from six.moves.urllib.request import urlretrieve
from backend.image_common import *


_session =get_session()
_trident_dir=get_trident_dir()




class Sampler(object):
    r"""Base class for all Samplers.

    Every Sampler subclass has to provide an __iter__ method, providing a way
    to iterate over indices of dataset elements, and a __len__ method that
    returns the length of the returned iterators.
    """

    def __init__(self, data_source):
        pass

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class SequentialSampler(Sampler):
    r"""Samples elements sequentially, always in the same order.

    Arguments:
        data_source (Dataset): dataset to sample from
    """

    def __init__(self, data_source):
        super(SequentialSampler, self).__init__(data_source)
        self.data_source = data_source

    def __iter__(self):
        return iter(range(len(self.data_source)))

    def __len__(self):
        return len(self.data_source)

class RandomSampler(Sampler):
    r"""Samples elements randomly. If without replacement, then sample from a shuffled dataset.
    If with replacement, then user can specify ``num_samples`` to draw.

    Arguments:
        data_source (Dataset): dataset to sample from
        num_samples (int): number of samples to draw, default=len(dataset)
        replacement (bool): samples are drawn with replacement if ``True``, default=False
    """

    def __init__(self, data_source, is_bootstrap=False, bootstrap_samples=None):
        super(RandomSampler, self).__init__(data_source)
        self.data_source = data_source
        self.is_bootstrap = is_bootstrap
        self.bootstrap_samples = bootstrap_samples

        if self.bootstrap_samples is not None and is_bootstrap is False:
            raise ValueError("With replacement=False, num_samples should not be specified, "
                             "since a random permute will be performed.")

        if self.bootstrap_samples is None:
            self.bootstrap_samples = len(self.data_source)

        if not isinstance(self.bootstrap_samples, int) or self.bootstrap_samples <= 0:
            raise ValueError("num_samples should be a positive integeral "
                             "value, but got num_samples={}".format(self.bootstrap_samples))
        if not isinstance(self.is_bootstrap, bool):
            raise ValueError("replacement should be a boolean value, but got "
                             "replacement={}".format(self.is_bootstrap))

    def __iter__(self):
        n = len(self.data_source)
        if self.is_bootstrap:
            return iter(np.random.randint(high=n, low=0,size=(self.bootstrap_samples), dtype=np.int64).tolist())
        return iter(np.random.randperm(n).tolist())

    def __len__(self):
        return len(self.data_source)


class BatchSampler(Sampler):
    r"""Wraps another sampler to yield a mini-batch of indices.

    Args:
        sampler (Sampler): Base sampler.
        batch_size (int): Size of mini-batch.
        drop_last (bool): If ``True``, the sampler will drop the last batch if
            its size would be less than ``batch_size``

    Example:
        >>> list(BatchSampler(SequentialSampler(range(10)), batch_size=3, drop_last=False))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
        >>> list(BatchSampler(SequentialSampler(range(10)), batch_size=3, drop_last=True))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    """

    def __init__(self, data_source, batch_size=1, is_shuffle=True,drop_last=False):
        if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size <= 0:
            raise ValueError("batch_size should be a positive integeral value, "
                             "but got batch_size={}".format(batch_size))
        if not isinstance(drop_last, bool):
            raise ValueError("drop_last should be a boolean value, but got "
                             "drop_last={}".format(drop_last))
        self.data_source = data_source
        self.batch_size = batch_size
        self.drop_last = drop_last
        self.is_shuffle=is_shuffle
        self.image_transforms=[]
        self.label_transforms = []

        idxes = np.arange(len(self.data_source))
        if len(self.data_source) % self.batch_size>0:
            idxes=idxes[:-(len(self.data_source) % self.batch_size)]
        if self.is_shuffle==True:
            np.random.shuffle(idxes)
        idxes = list(idxes)

        self.sampler = itertools.cycle(iter(idxes))

    def __iter__(self):
        batch =[]# list(next(self.sampler))
        for idx in self.sampler:
            batch.append(idx)
            if len(batch) == self.batch_size:
                self.data_source.tot_minibatch+=1
                self.data_source.tot_records += len(batch)
                yield self.data_source[batch]
                batch = []
        if len(batch)==0:
            raise StopIteration

    def __len__(self):
        if self.drop_last:
            return len(self.data_source) // self.batch_size
        else:
            return (len(self.data_source)+ self.batch_size - 1) // self.batch_size

    def reset(self):
        idxes = np.arange(len(self.data_source))
        if len(self.data_source) % self.batch_size > 0:
            idxes = idxes[:-(len(self.data_source) % self.batch_size)]
        if self.is_shuffle == True:
            np.random.shuffle(idxes)
        idxes = list(idxes)
        self.sampler = iter(idxes)




class DataProvider(object):
    """An abstract class representing a Dataset.

    All other datasets should subclass it. All subclasses should override
    ``__len__``, that provides the size of the dataset, and ``__getitem__``,
    supporting integer indexing in range from 0 to len(self) exclusive.
    """

    def __init__(self, dataset_name='',data=None,labels=None,masks=None,scenario=None,minibatch_size=8,**kwargs):
        self.__name__=dataset_name
        self.__initialized = False
        self.data = {}
        self.labels = {}
        self.masks = {}

        if scenario is None:
            scenario= 'raw'
        elif scenario not in ['training','testing','validation','train','val','test','raw']:
            raise ValueError('Only training,testing,validation,val,test,raw is valid senario')
        self.current_scenario=scenario
        if data is not None and hasattr(data, '__len__'):
            self.data[self.current_scenario]=np.array(data)

            print('Mapping data  in {0} scenario  success, total {1} record addeds.'.format(scenario,len(data)))
            self.__initialized = True
        if labels is not None and hasattr(labels,'__len__'):
            if len(labels)!=len(data):
                raise ValueError('labels and data count are not match!.')
            else:
                self.labels[self.current_scenario]=np.array(labels)
                print('Mapping label  in {0} scenario  success, total {1} records added.'.format(scenario, len(labels)))
        if masks is not None and hasattr(masks, '__len__'):
            if len(masks)!=len(data):
                raise ValueError('masks and data count are not match!.')
            else:
                self.masks[self.current_scenario]=np.array(masks)
                print('Mapping mask  in {0} scenario  success, total {1} records added.'.format(scenario, len(masks)))


        self.class_names={}
        self.palettes=None
        self.minibatch_size = minibatch_size
        self.is_flatten=bool(kwargs['is_flatten']) if 'is_flatten' in kwargs else False
        self.__default_language__='en-us'
        self.__current_idx2lab__={}
        self.__current_lab2idx__ = {}

        self.batch_sampler=BatchSampler(self ,self.minibatch_size,is_shuffle=True,drop_last=False)
        self._sample_iter =iter(self.batch_sampler)
        self.tot_minibatch=0
        self.tot_records=0
        self.tot_epochs=0
    def _check_data_available(self):
        if len(self.data[self.current_scenario])>0:
            pass
        elif len(self.data['train'])>0:
            self.current_scenario='train'
        elif len(self.data['raw'])>0:
            self.current_scenario='raw'
        elif len(self.data['test'])>0:
            self.current_scenario='test'
    def reset_statistics(self):
        self.tot_minibatch = 0
        self.tot_records = 0
        self.tot_epochs = 0
        self._check_data_available()


    def __getitem__(self, index):
        if self.tot_records == 0:
            self._check_data_available()
        if len(self.data[self.current_scenario])>index and len(self.masks[self.current_scenario])>index and len(self.labels[self.current_scenario])==0:
            return self.data[self.current_scenario][index], self.masks[self.current_scenario][index]
        elif len(self.data[self.current_scenario])>index and len(self.labels[self.current_scenario])>index and len(self.masks[self.current_scenario])==0:
            return self.data[self.current_scenario][index],self.labels[self.current_scenario][index]
        return self.data[self.current_scenario][index]

    def _next_index(self):
        return next(self._sample_iter)

    def __iter__(self):
        return self._sample_iter

    def __len__(self):
        if not isinstance(self.data,dict) or  len(self.data.items())==0 :
            return 0
        if self.current_scenario not in self.data:
            raise ValueError('Current Scenario {0} dont have data.'.format(self.current_scenario))
        elif len(self.data[self.current_scenario])==0:
            self._check_data_available()
            return len(self.data[self.current_scenario])
        else:
            return len(self.data[self.current_scenario])

    def mapping(self,data,labels=None,masks=None,scenario=None):
        if scenario is None:
            scenario= 'train'
        elif scenario not in ['training','testing','validation','train','val','test','raw']:
            raise ValueError('Only training,testing,validation,val,test,raw is valid senario')
        self.current_scenario=scenario
        if data is not None and hasattr(data, '__len__'):
            self.data[scenario]=np.array(data)
            self.__batch_idxes = np.arange(len(self.data[self.current_scenario]))
            print('Mapping data  in {0} scenario  success, total {1} record addeds.'.format(scenario,len(data)))
            self.__initialized = True
        if labels is not None and hasattr(labels,'__len__'):
            if len(labels)!=len(data):
                raise ValueError('labels and data count are not match!.')
            else:
                self.labels[scenario]=np.array(labels)
                print('Mapping label  in {0} scenario  success, total {1} records added.'.format(scenario, len(labels)))
        if masks is not None and hasattr(masks, '__len__'):
            if len(masks)!=len(data):
                raise ValueError('masks and data count are not match!.')
            else:
                self.masks[scenario]=np.array(masks)
                print('Mapping mask  in {0} scenario  success, total {1} records added.'.format(scenario, len(masks)))


    def binding_class_names(self,class_names=None,language=None):
        if class_names is not None and hasattr(class_names, '__len__'):
            if language is None:
                language = 'en-us'
            self.class_names[language] = list(class_names)
            print('Mapping class_names  in {0}   success, total {1} class names added.'.format(language, len(class_names)))
            self.__default_language__=language
            self.__current_lab2idx__= {v: k for k, v in enumerate(self.class_names[language] )}
            self.__current_idx2lab__={k: v for k, v in enumerate(self.class_names[language] )}

            # if len(list(set(self.labels[scenario])))!=len(self.class_names):
            #     warnings.warn('Distinct labels count is not match with class_names', category='mapping', stacklevel=1, source=self.__class__)
            #

    def change_language(self, lang):
        self.__default_language__ = lang
        if self.class_names is None or len(self.class_names.items())==0 or lang not in self.class_names :
            warnings.warn('You dont have {0} language version class names', category='mapping', stacklevel=1, source=self.__class__)
        else:
            self.__current_lab2idx__ = {v: k for k, v in enumerate(self.class_names[lang])}
            self.__current_idx2lab__ = {k: v for k, v in enumerate(self.class_names[lang])}

    def index2label(self, idx:int):
        if self.__current_idx2lab__  is None or len(self.__current_idx2lab__ .items())==0:
            raise ValueError('You dont have proper mapping class names')
        elif  idx not in self.__current_idx2lab__ :
            raise ValueError('Index :{0} is not exist in class names'.format(idx))
        else:
            return self.__current_idx2lab__[idx]

    def label2index(self ,label):
        if self.__current_lab2idx__  is None or len(self.__current_lab2idx__ .items())==0:
            raise ValueError('You dont have proper mapping class names')
        elif  label not in self.__current_lab2idx__ :
            raise ValueError('label :{0} is not exist in class names'.format(label))
        else:
            return self.__current_lab2idx__[label]

    def get_language(self):
        return self.__default_language__


    # def next_bach(self,minibach_size=None):
    #


    def __next__(self):
        next(self._sample_iter)
        # # if minibach_size is not None and minibach_size != self.minibatch_size:
        # #     self.minibatch_size = minibach_size
        # #     self.batch_sampler = BatchSampler(range(len(self.data[self.current_scenario])), self.minibatch_size,
        # #                                       is_shuffle=True, drop_last=False)
        # #     self._sample_iter = iter(self.batch_sampler)
        #
        # if self.batch_sampler is None or len(self.batch_sampler) == 0:
        #     self.batch_sampler = BatchSampler(range(len(self.data[self.current_scenario])), self.minibatch_size,
        #                                       is_shuffle=True, drop_last=False)
        #     self._sample_iter = iter(self.batch_sampler)

        # index = self._next_index()  # may raise StopIteration
        # batch = self.__getitem__(index)  # may raise StopIteration
        # # batch= zip(*batch)
        # self.tot_minibatch += 1
        # self.tot_records += len(batch[0])
        # self.tot_epochs = self.tot_records // self.__len__()
        # yield  batch





# class DataProvider(object):
#     def __init__(self, dataset, batch_size=1, shuffle=True,num_workers=0,  pin_memory=False, drop_last=False,
#                  timeout=0, worker_init_fn=None):
#         self.dataset = dataset
#         self.batch_size = batch_size
#         self.num_workers = num_workers
#         self.shuffle=shuffle
#         self.split_idxs=range(self.__len__())
#         self.batch_idxs=range(self.__len__())
#         self.pin_memory = pin_memory
#         self.drop_last = drop_last
#         self.timeout = timeout
#         self.worker_init_fn = worker_init_fn
#
#         if timeout < 0:
#             raise ValueError('timeout option should be non-negative')
#
#
#         if batch_sampler is not None:
#             if batch_size > 1 or shuffle or sampler is not None or drop_last:
#                 raise ValueError('batch_sampler option is mutually exclusive '
#                                  'with batch_size, shuffle, sampler, and '
#                                  'drop_last')
#             self.batch_size = None
#             self.drop_last = None
#
#         if sampler is not None and shuffle:
#             raise ValueError('sampler option is mutually exclusive with '
#                              'shuffle')
#
#         if self.num_workers < 0:
#             raise ValueError('num_workers option cannot be negative; '
#                              'use num_workers=0 to disable multiprocessing.')
#
#         if batch_sampler is None:
#             if sampler is None:
#                 if shuffle:
#                     sampler = RandomSampler(dataset)
#                 else:
#                     sampler = SequentialSampler(dataset)
#             batch_sampler = BatchSampler(sampler, batch_size, drop_last)
#
#         self.sampler = sampler
#         self.batch_sampler = batch_sampler
#         self.__initialized = True
#     def __setattr__(self, attr, val):
#         if self.__initialized and attr in ('batch_size', 'sampler', 'drop_last'):
#             raise ValueError('{} attribute should not be set after {} is '
#                              'initialized'.format(attr, self.__class__.__name__))
#
#         super(DataLoader, self).__setattr__(attr, val)
#
#     def __iter__(self):
#         return _DataLoaderIter(self)
#
#     def __len__(self):
#         return len(self.batch_sampler)





