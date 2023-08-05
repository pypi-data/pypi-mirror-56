import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xlsfile-shaw1236", # Replace with your own username
    version="0.0.2",
    author="Simon Li",
    author_email="shaw1236@gmail.com",
    description="Utility for read/write of Excel or csv files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shaw1236/ExcelFiles",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
