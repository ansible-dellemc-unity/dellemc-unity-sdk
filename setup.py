from setuptools import setup, find_packages

setup(
    name='dellemc_unity_sdk',
    version='0.2',
    packages=find_packages(),
    author='Dmitry Mityushin',
    author_email='mityushin.dmitry@gmail.com',
    url='https://github.com/SPBSTUandDELLEMC-unity-ansible/dellemc_unity_sdk',
    install_requires=['requests']
)
