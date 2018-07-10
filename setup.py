from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
    name="dellemc_unity_sdk",
    version="0.4.1",
    packages=find_packages(),
    author="Dmitry Mityushin",
    author_email="mityushin.dmitry@gmail.com",
    description="Package used to create requests to DellEMC Unity.",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ansible-dellemc-unity/dellemc-unity-sdk",
    install_requires=find_packages(),
    # install_requires=['requests', 'ansible']
    classifiers=(
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
)
