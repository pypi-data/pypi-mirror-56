import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zmq_ses_communications",  # Replace with your own username
    version="0.0.1",
    author="Vinu",
    author_email="vinuvnair@outlook.com",
    description="communication backend for creating a distributed system for integrating devices in a smart factory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/specospec/zmq_ses_communications",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
