from setuptools import find_packages, setup
setup(
    name='acft_evaluators',
    packages=find_packages(),
    version='1.0.0',
    description='Simplified aircraft performance model',
    author='Carlos Schwabe | João Vitor Lima | Luis Guilherme Burato',
    license='MIT',
    install_requires=['pandas','numpy','math','fluids'],
)