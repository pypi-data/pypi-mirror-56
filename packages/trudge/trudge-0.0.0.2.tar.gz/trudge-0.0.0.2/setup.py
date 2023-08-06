from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name             = "trudge",
    version          = "0.0.0.2",
    packages         = ["trudge",],
    install_requires = [],
    license          = "MIT",
    url              = "https://github.com/reity/trudge",
    author           = "Andrei Lapets",
    author_email     = "a@lapets.io",
    description      = "Generators that enumerate discrete spaces using various strategies.",
    long_description = long_description,
    long_description_content_type = "text/x-rst",
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
)
