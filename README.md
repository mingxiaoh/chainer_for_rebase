# iDeep: Intel Deep Learning Extension Package

Intel Deep Learning Extension Package is a module for collection of accelerated deep learning operations like convolution, deconvolution, relu etc. It uses intel MKL and MKL-DNN as acceleration engine.


## Requirements

This preview version of ideep is tested on Ubuntu 16.04 and OS X, and examples are implemented as a suggestion for its integration of chainer v4.0.0b4.

Minimum requirements:
- Python 2.7.6+, 3.5.2+, 3.6.0+
- Chainer v4.0.0b4
- Numpy 1.13
- Six 1.9+
- MKL 2018 Initial Release 
- MKL-DNN 0.1+
- Swig 3.0.12
- Cmake3
- Doxygen 1.8.5
- C++ compiler with C++11 standard support

Requirements for some features:
- Testing utilities
  - Mock
  - Gtest

## Installation
### Install MKL

Download and install intel MKL at https://software.intel.com/en-us/mkl

### Install MKL-DNN

Refer https://github.com/01org/mkl-dnn for install instruction

### Install python package

If you use old ``setuptools``, upgrade it:

```
pip install -U setuptools
```

install ideep from the source code:

```
git submodule update --init && mkdir build && cmake .. 
python setup.py install
```

### Install cpp package
Install ideep from the source code:

```
git submodule update --init && mkdir build && cmake ..
make && make install
```


## More information
- MKL site: https://software.intel.com/en-us/mkl
- MKL-DNN github: https://github.com/01org/mkl-dnn
- ideep github: https://github.com/intel/ideep.git
- Chainer github: https://github.com/pfnet/chainer

## License
MIT License (see `LICENSE` file).
