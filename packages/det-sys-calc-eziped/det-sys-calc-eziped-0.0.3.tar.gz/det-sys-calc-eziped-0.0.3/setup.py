import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="det-sys-calc-eziped", # Replace with your own username
    version="0.0.3",
    author="Eddie Zhang",
    author_email="obeyfutzipe666@gmail.com",
    description="Calculate systems of equations and determinants to your heart's content",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ezhang7423/determinant-calc/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)