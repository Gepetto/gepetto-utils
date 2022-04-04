from setuptools import setup
import os


def read_text(path):
    with open(path) as f:
        return f.read().decode("utf-8").strip()


def data_files(*paths):
    return [
        (root, [os.path.join(root, f) for f in files])
        for path in paths
        for root, _, files in os.walk(path)
    ]


setup(
    name="example-robot-data",
    packages=["example_robot_data"],
    description="Set of robot URDFs for benchmarking and developed examples.",
    url="https://github.com/gepetto/example-robot-data",
    install_requires=["pinocchio"],
    data_files=data_files("include", "lib", "share"),
    version=read_text(".version"),
    long_description=read_text("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=2.7",
)
