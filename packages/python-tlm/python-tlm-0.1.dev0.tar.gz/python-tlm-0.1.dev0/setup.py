import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-tlm",
    use_scm_version={
        "relative_to": __file__,
        "write_to": "tlm/version.py",
    },
    author="Stefan Wallentowitz",
    author_email="stefan@wallentowitz.de",
    description="Python Transaction Level Modeling",
    long_description=long_description,
    url="https://github.com/wallento/python-tlm",
    packages=["tlm"],
    install_requires=[],
    setup_requires=[
        'setuptools_scm',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
)
