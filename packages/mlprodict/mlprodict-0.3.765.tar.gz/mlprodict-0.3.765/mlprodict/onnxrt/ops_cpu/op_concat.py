# -*- encoding: utf-8 -*-
# pylint: disable=E0203,E1101,C0111
"""
@file
@brief Runtime operator.
"""
import numpy
from ._op import OpRun
from ..shape_object import ShapeObject


class Concat(OpRun):

    atts = {'axis': 0}

    def __init__(self, onnx_node, desc=None, **options):
        OpRun.__init__(self, onnx_node, desc=desc,
                       expected_attributes=Concat.atts,
                       **options)

    def _preprocess(self, a):
        if self.axis >= len(a.shape):
            new_shape = a.shape + (1, ) * (self.axis + 1 - len(a.shape))
            return a.reshape(new_shape)
        return a

    def _run(self, *args):  # pylint: disable=W0221
        args = [self._preprocess(a) for a in args]
        return (numpy.concatenate(args, self.axis), )

    def _infer_shapes(self, *args):  # pylint: disable=W0221
        return (args[0].concat_columns(self.axis, *(args[1:])), )

    def _infer_type(self, *args):
        return ShapeObject._infer_merged_type(*args)
