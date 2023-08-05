from setuptools import setup



def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="multipleinputs",
    version="0.0.4",
    description="A Python package to get multiple inputs from console as array in required datatype",
    author="Himank Jain",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author_email="himank369123@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["multipleinputs"],
    install_requires=["numpy"],
    include_package_data=True
)
