import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="calcroad_simulation",
    version="0.1.1",
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
    install_requires=[
        'Dijkstar==2.5.0'
    ],
    python_requires='>=3.6'
)
