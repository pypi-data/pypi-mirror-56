import os.path

from setuptools import find_packages, setup

version = None
with open(os.path.join("src", "resolvref", "version.py")) as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split('"')[1]

if not version:
    raise ValueError("did not detect version correctly")

setup(
    name="resolvref",
    version=version,
    description="Resolve JSON and YAML references (e.g. in OpenAPI specs)",
    long_description=open("README.rst").read(),
    entry_points={"console_scripts": ["resolvref = resolvref.main:main"]},
    author="Stpehen Rosen",
    author_email="sirosen@uchicago.edu",
    url="https://github.com/sirosen/resolvref",
    packages=find_packages("src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
    extras_require={
        "yaml": ["pyyaml>=5,<6"],
        "development": [
            # testing
            "pytest>=5.2.2,<6",
            "pytest-cov>=2.5.1,<3.0",
            "pytest-xdist>=1.22.5,<2.0",
            # mock on py2, py3.4 and py3.5
            # not just py2: py3 versions of mock don't all have the same
            # interface!
            'mock==2.0.0;python_version<"3.6"',
        ],
    },
    include_package_data=True,
    keywords=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
