# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TensorFlow Quantitative Finance."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# We need to put some imports inside a function call below, and the function
# call needs to come before the *actual* imports that populate the
# tf_quant_finance namespace. Hence, we disable this lint check throughout
# the file.
#
# pylint: disable=g-import-not-at-top

# Update this whenever we need to depend on a newer TensorFlow release.
_REQUIRED_TENSORFLOW_VERSION = "1.15"  # pylint: disable=g-statement-before-imports


# Ensure TensorFlow is importable and its version is sufficiently recent. This
# needs to happen before anything else, since the imports below will try to
# import tensorflow, too.
def _ensure_tf_install():  # pylint: disable=g-statement-before-imports
  """Attempt to import tensorflow, and ensure its version is sufficient.

  Raises:
    ImportError: if either tensorflow is not importable or its version is
    inadequate.
  """
  try:
    import tensorflow as tf
  except ImportError:
    # Print more informative error message, then reraise.
    print("\n\nFailed to import TensorFlow. Please note that TensorFlow is not "
          "installed by default when you install TF Quant Finance library. "
          "This is so that users can decide whether to install the GPU-enabled "
          "TensorFlow package. To use TF Quant Finance library, please install "
          "the most recent version of TensorFlow, by following instructions at "
          "https://tensorflow.org/install.\n\n")
    raise

  import distutils.version

  if (distutils.version.LooseVersion(tf.__version__) <
      distutils.version.LooseVersion(_REQUIRED_TENSORFLOW_VERSION)):
    raise ImportError(
        "This version of TF Quant Finance library requires TensorFlow "
        "version >= {required}; Detected an installation of version {present}. "
        "Please upgrade TensorFlow to proceed.".format(
            required=_REQUIRED_TENSORFLOW_VERSION, present=tf.__version__))


_ensure_tf_install()

from tf_quant_finance import black_scholes
from tf_quant_finance import math
from tf_quant_finance import models
from tf_quant_finance import rates
from tensorflow.python.util.all_util import remove_undocumented  # pylint: disable=g-direct-tensorflow-import

_allowed_symbols = [
    "math",
    "models",
    "rates",
    "black_scholes",
]

remove_undocumented(__name__, _allowed_symbols)
