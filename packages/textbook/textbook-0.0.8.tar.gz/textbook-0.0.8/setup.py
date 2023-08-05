import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="textbook",
    version="0.0.8",
    author="Chenghao",
    python_requires='>3.7.0',
    author_email="mouchenghao@gmail.com",
    description="Text classification datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChenghaoMou/textbook",
    packages=setuptools.find_packages(),
    install_requires=[
        'jsonnet',
        'torch',
        'transformers',
        'torchvision',
        'opencv_python',
        'av',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
)
