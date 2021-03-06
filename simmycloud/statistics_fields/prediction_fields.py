###############################################################################
# The MIT License (MIT)
#
# Copyright (c) 2013 Cássio Paixão
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###############################################################################

from statistics import mean, stdev

from core.statistics_manager import StatisticsField


class PredictionField(StatisticsField):
    def set_prediction_base(self, prediction_base):
        self.prediction_base = prediction_base

    def set_resource(self, resource):
        self.resource = 0 if resource == 'cpu' else 1


class AverageAbsolutePredictionErrorField(PredictionField):
    def value(self):
        if self.prediction_base:
            return mean(m[0][self.resource] - m[1][self.resource] for m in self.prediction_base)
        else: return 0

class StdevAbsolutePredictionErrorField(PredictionField):
    def value(self):
        if len(self.prediction_base) > 1:
            return stdev(m[0][self.resource] - m[1][self.resource] for m in self.prediction_base)
        else: return 0

class AveragePercentilePredictionErrorField(PredictionField):
    def value(self):
        if self.prediction_base:
            return mean((m[0][self.resource] - m[1][self.resource])/m[1][self.resource] for m in self.prediction_base)
        else: return 0

class StdevPercentilePredictionErrorField(PredictionField):
    def value(self):
        if len(self.prediction_base) > 1:
            return stdev((m[0][self.resource] - m[1][self.resource])/m[1][self.resource] for m in self.prediction_base)
        else: return 0
