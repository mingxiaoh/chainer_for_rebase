# iDeep: Intel Deep Learning Extension Package

Intel Deep Learning Extension Package is a module for collection of accelerated deep learning operations like convolution, deconvolution, relu etc. It uses Intel MKL-DNN as acceleration engine.


## Requirements

This preview version of iDeep is tested on Ubuntu 16.04 and OS X.

Minimum requirements:
- Cmake3
- GCC 5.3+
- C++ compiler with C++11 standard support
- MKL-DNN 0.1+
- Python 2.7.6+, 3.5.2+, 3.6.0+
- Numpy 1.13
- Swig 3.0.12
- Doxygen 1.8.5


Requirements for some features:
- Testing utilities
  - Gtest
  - pytest

## Installation

### Install iDeep python package

If you use old ``setuptools``, upgrade it:

```
pip install -U setuptools
```

install iDeep python package(ideep4py) from the source code:

```
git submodule update --init && mkdir build && cmake .. 
python setup.py install
```

### iDeep cpp API

Head file mode to introduce iDeep cpp APIs:

```
#include "ideep.hpp"
```

Pin singleton head file to one cpp file of your project to instance iDeep singletons.

```
@@ main.cc
#include "ideep_pin_singletons.hpp"
```

## More information
- MKL site: https://software.intel.com/en-us/mkl
- MKL-DNN github: https://github.com/01org/mkl-dnn
- iDeep github: https://github.com/intel/ideep.git
- Chainer github: https://github.com/pfnet/chainer

## License
MIT License (see `LICENSE` file).
