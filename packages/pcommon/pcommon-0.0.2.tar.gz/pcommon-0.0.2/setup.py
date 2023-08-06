import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name = "pcommon",
    version = "0.0.2",
    author = "shijianliangs",
    author_email = "shijianliangs@gmail.com",
    description = "A python tool package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/shijianliangs/utils-1019",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
)
