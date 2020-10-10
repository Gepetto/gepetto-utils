from skbuild import setup

try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="pinocchio",
    version="VERSION",
    description="A fast and flexible implementation of Rigid Body Dynamics algorithms and their analytical derivatives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stack-of-tasks/pinocchio",
    install_requires=['hpp-fcl'],
    cmake_minimum_required_version='3.1',
    classifiers=[
        "Programming Language :: Python :: 2", "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License", "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=2.7',
)
