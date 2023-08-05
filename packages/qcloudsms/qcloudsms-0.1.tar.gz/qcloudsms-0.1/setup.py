import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qcloudsms", # Replace with your own username
    version="0.1",
    author="SamuelWu",
    author_email="samuel.yh.wu@gmail.com",
    description="Qcloud(Tecent Cloud) Python3 SMS SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wyh/qcloudsms",
    packages=setuptools.find_packages(),
    install_requires = ['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
