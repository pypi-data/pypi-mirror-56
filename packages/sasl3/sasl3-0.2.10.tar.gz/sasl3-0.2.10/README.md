# python-sasl

Python wrapper for Cyrus SASL

## how `sasl3` is different from `sasl` package? 

This is a fork from original work from Cloudera's https://github.com/cloudera/python-sasl package `sasl` package. 

Original package wasn't maintained and had issue wth latest Python 3 releases, and also had runtime issues running 
on RHEL6. Python `sasl` solves those issues.

## External dependencies

You need following external packages installed on the system to pip-install `sasl3` :
- C compiler (e.g. `gcc`)
- `cyrus-sasl-devel` packahe for Cyrus header files.

Both can be installed with OS' package manager, e.g. 
```bash
yum install gcc cyrus-sasl-devel.x86_64

```

## to generate sasl/saslwrapper.cpp from the pyx file:

run `./recython.sh`
