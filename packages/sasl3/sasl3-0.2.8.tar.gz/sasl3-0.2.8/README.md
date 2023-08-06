# python-sasl

Python wrapper for Cyrus SASL

# why `sasl3`? 

This is a fork from original work from Cloudera's https://github.com/cloudera/python-sasl package `sasl` package. 
Original package wasn't maintained and had issue wth latest Python 3 releases, and also had runtime issues running 
on RHEL6. Python `sasl` solves those issues. 


### to generate sasl/saslwrapper.cpp from the pyx file:

run `./recython.sh`
