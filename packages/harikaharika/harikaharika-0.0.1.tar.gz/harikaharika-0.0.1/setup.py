import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="harikaharika", # Replace with your own username
    version="0.0.1",
    author="harika",
    author_email="harikamanu260997@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/venkatadri123/codesignals.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)