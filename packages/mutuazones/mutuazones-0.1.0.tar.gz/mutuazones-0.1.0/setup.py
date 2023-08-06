import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mutuazones",
    version="0.1.0",
    author="Carlos López Pérez",
    author_email="carlos.lopez@mutuatfe.com",
    description="Se corrige el acceso a los esquemas cuando el usuario tiene más privilegios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mutuatfe/smartflow/mutuazones.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)