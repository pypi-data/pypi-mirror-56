import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yapg",
    version="0.0.4",
    author="Alexandre Janvrin",
    author_email="alexandre.janvrin@dnconsulting.com",
    description="A simple password generator checking password complexity with zxcvbn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        'zxcvbn',
    ],
    python_requires='>=3.6',
)
