import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pisi", # Replace with your own username
    version="999.999",
    author="Pale Dega",
    author_email="hebele@hubele.org",
    description="my example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/pisi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=999.999',
)
