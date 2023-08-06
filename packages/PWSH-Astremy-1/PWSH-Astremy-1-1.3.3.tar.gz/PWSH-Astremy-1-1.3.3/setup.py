import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PWSH-Astremy-1", # Replace with your own username
    version="1.3.3",
    author="Astremy",
    author_email="",
    description="A framework to help for backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Astremy/Python-Web-Site-Helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)