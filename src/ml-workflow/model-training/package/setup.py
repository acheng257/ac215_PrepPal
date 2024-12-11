from setuptools import find_packages
from setuptools import setup


REQUIRED_PACKAGES = ["pythonjsonlogger"]

setup(
    name="preppal-trainer",
    version="0.0.1",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description="PrepPal Trainer Application",
)
