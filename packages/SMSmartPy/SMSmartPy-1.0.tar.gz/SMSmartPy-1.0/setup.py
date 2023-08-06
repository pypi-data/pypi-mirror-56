from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="SMSmartPy",
    version="1.0",
    description="A Python package.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/SmartManoj/SmartPy",
    author="Mehul Gupta",
    author_email="mehularnavi28@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Smart"],
    include_package_data=True,
    install_requires=["requests"],
    
)