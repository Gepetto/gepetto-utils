from skbuild import setup

try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="PACKAGE_NAME",
    version="VERSION",
    description="DESCRIPTION",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GITHUB_ORG/TARGET",
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 2", "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License", "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=2.7',
)
