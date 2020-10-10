from skbuild import setup

try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="hpp-fcl",
    version="1.6.0",
    description="HPP fork of FCL -- The Flexible Collision Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/humanoid-path-planner/hpp-fcl",
    install_requires=['eigenpy'],
    cmake_minimum_required_version='3.1',
    classifiers=[
        "Programming Language :: Python :: 2", "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License", "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=2.7',
)
