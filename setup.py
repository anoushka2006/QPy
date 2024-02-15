import setuptools

setuptools.setup(
    name="qpy",
        version = "0.0.0",
    author="Anoushka Chaudhury",
    author_email="anoushkachaudhury5@gmail.com",
    description="Simulator for Quantum Circuits",
    license="MIT",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "numpy"
    ],
)