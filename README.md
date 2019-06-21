# Purpose
Example Robot Framework project that demontrates common testing
instruments using serial communication.

# Requirements
* Python 3+
* Robot Framework
* Pyserial (if using _real_ serial communication)
* Docutils (if using ReStructured Text Format)

_Note: See `requirements.txt` for all requirements. Requirements can be 
installed with `pip install -r requirements.txt`_

# Usage
From the root of the repository -
`robot --variable PORT:/dev/ttyUSB0 --pythonpath libs/ tests/`

# Developing

## Requirements
* Virtualenv (for development)
* Black (for development)

Strongly suggest using a "python virtual environment" via virtualenv (or equivalent) - 

* `pip install virtualenv`
* `python -m virtualenv venv`
* `venv/bin/pip install -r requirements.txt`

## Structure
Many instruments require abstractions in Python to make use from Robot 
Framework easier. Abstractions are in `./libs`.

Folders containing `.robot` files are test suites. `.robot` files are test suites
containing 1...n test cases.

# Known Issues
None

# Resources
* [Robot Framework User Manual](https://robotframework.org/)
* [Robot Framework Built-in Libraries](http://robotframework.org/robotframework/#standard-libraries)
