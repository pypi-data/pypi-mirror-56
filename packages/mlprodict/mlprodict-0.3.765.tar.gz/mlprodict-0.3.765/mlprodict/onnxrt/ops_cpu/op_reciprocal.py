# -*- encoding: utf-8 -*-
# pylint: disable=E0203,E1101,C0111
"""
@file
@brief Runtime operator.
"""
import numpy
from ._op import OpRunUnaryNum


class Reciprocal(OpRunUnaryNum):

    def __init__(self, onnx_node, desc=None, **options):
        OpRunUnaryNum.__init__(self, onnx_node, desc=desc,
                               **options)

    def _run(self, x):  # pylint: disable=W0221
        with numpy.errstate(divide='ignore'):
            if self.inplaces.get(0, False):
                return (numpy.reciprocal(x, out=x), )
            else:
                return (numpy.reciprocal(x), )
