import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="calcroad_simulation",  # Replace with your own username
    version="0.0.7",
    author="Urbanize",
    author_email="urbanize.contact@gmail.com",
    description="CalcROAD simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/urbanize/simulation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
