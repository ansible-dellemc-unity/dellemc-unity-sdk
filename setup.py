from setuptools import setup, find_packages

setup(
    name='dellemc-unity-sdk',
    version='0.4.1',
    packages=find_packages(),
    author='Dmitry Mityushin',
    author_email='mityushin.dmitry@gmail.com',
    url='https://github.com/SPBSTUandDELLEMC-unity-ansible/dellemc-unity-sdk',
    install_requires=['requests', 'ansible']
)
