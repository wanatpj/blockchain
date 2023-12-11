from distutils.core import setup

from setuptools import find_namespace_packages

with open("VERSION", "r") as f:
    version = f.read().strip()

with open("requirements/requirements.txt", "r") as f:
    required_packages = f.read().split()

setup(
    name="blockchain",
    version=version,
    description="Sample implementation of blockchain in Python.",
    author="Paweł Wanat",
    author_email="wanatpj+blockchain@gmail.com",
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    install_requires=required_packages,
    setup_requires=["wheel", "bdist_wheel"],
)
