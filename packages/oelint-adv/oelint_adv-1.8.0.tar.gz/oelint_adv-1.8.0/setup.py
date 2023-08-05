import setuptools

import subprocess
_long_description = "See https://github.com/priv-kweihmann/oelint-adv for documentation"
_long_description_content_type = "text/plain"
try:
    _long_description = subprocess.check_output(
        ["pandoc", "--from", "markdown", "--to", "rst", "README.md"]).decode("utf-8")
    _long_description_content_type = "text/x-rst"
except (subprocess.CalledProcessError, FileNotFoundError):
    pass

setuptools.setup(
    name="oelint_adv",
    version="1.8.0",
    author="Konrad Weihmann",
    author_email="kweihmann@outlook.com",
    description="Advanced bitbake-recipe linter",
    long_description=_long_description,
    long_description_content_type=_long_description_content_type,
    url="https://github.com/priv-kweihmann/oelint-adv",
    packages=setuptools.find_packages(),
    scripts=['bin/oelint-adv'],
    install_requires=[
        'urllib3>=1.21.1',
        'anytree>=2.7.0'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
