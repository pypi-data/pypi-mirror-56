import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SealLogging", # Replace with your own username
    version="1.0.0",
    author="Darwin Subramaniam",
    author_email="darwin.subramaniam@wdc.com",
    description="A Logging Library for Seal Softwares",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.wdc.com/projects/HDDRDSDSMML/repos/inspection-false-call-detector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)