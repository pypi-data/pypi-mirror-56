# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_io.core.python.ops import _load_library

_golang_ops = _load_library('libtensorflow_io_golang.so')

io_prometheus_readable_init = _golang_ops.io_prometheus_readable_init
io_prometheus_readable_spec = _golang_ops.io_prometheus_readable_spec
io_prometheus_readable_read = _golang_ops.io_prometheus_readable_read
