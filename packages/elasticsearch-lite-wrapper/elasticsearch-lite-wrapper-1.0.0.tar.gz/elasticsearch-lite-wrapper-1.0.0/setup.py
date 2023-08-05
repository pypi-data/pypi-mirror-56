import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'elasticsearch-lite-wrapper',
    version = '1.0.0',
    author = 'Sanchit Dass',
    author_email = 'sanchitd9@gmail.com',
    description = 'A lightsweight elasticsearch client',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/sanchitd9/es-client',
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.1.2',
)