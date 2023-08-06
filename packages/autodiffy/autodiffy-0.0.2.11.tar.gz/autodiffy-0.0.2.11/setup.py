import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autodiffy",
    version="0.0.2.11",
    author="Will Fried, Andrew Chia, Ankith Harathi, Wei-Hung Hsu",
    author_email=" ",
    description="Automatic Differentiation package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CS207-Feiyu-Group8/cs207-FinalProject",
    packages=setuptools.find_packages(),
    install_requires=['numpy>=1.17',
                      'pythonds>=1.2.1',
                      'pytest>=5.2', 
                      'pytest-cov>=2.8',
                      'pytest-dependency>=0.4'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)