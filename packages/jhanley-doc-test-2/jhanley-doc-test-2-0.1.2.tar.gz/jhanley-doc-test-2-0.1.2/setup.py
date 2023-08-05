import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jhanley-doc-test-2",
    version="0.1.2",
    author="John J. Hanley",
    author_email="blog@jhanley.com",
    description="This is a test package for deploying to PyPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhanley-com/doc-test-2",
    packages=setuptools.find_packages(),
    platforms=['any'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
