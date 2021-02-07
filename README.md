# SECUNIT
Mobile Security Robot

# Installation

## Install From Source

Obtain the source from git.
```bash
git clone https://github.com/DustinMoriarty/secunit.git
cd secunit
```

### Install With Pip 
For non-development use, install using pip.
```bash
pip install .
```
Note that `pip install -e .` is not supported.

## Robot Pinout
Review resources/production.json for the pinout that is expected.

## Run On Target
To run the application on target, use the following.
```bash
gunicorn -b 0.0.0.0:8080 secunit.wsgi
```
Modify the IP and path as necessary depending on your web server configuration.

A basic web-ui is available at http://0.0.0.0:8080/controller.



