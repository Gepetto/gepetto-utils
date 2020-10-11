from skbuild import setup

try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="example-robot-data",
    version="VERSION",
    description="Set of robot URDFs for benchmarking and developed examples.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gepetto/example-robot-data",
    install_requires=['pinocchio'],
    cmake_minimum_required_version='3.1',
    classifiers=[
        "Programming Language :: Python :: 2", "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License", "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=2.7',
)
