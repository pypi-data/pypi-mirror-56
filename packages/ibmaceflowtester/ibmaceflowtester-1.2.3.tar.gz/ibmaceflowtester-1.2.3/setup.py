import setuptools
from ibmaceflowtester.util import io

long_description = io.read_file_string("README.md")

setuptools.setup(
    name="ibmaceflowtester",
    version="1.2.3",
    author="Jasper Landa",
    author_email="jasperlanda91@gmail.com",
    description="Package to perform tests for IBM ACE interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JLanda91/ibm-ace-flow-tester",
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)