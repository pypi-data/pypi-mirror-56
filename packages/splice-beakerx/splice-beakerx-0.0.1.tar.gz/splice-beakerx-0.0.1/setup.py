import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="splice-beakerx", # Replace with your own username
    version="0.0.1",
    author="Two Sigma",
    author_email="author@example.com",
    description="Splice Modification for TwoSigma Beakerx",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.65',
)
