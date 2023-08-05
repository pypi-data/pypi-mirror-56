import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s2s",
    version="0.0.0",
    author="HQ",
    author_email="idorce@outlook.com",
    description="Sequence to Sequence Learning with PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idorce/s2s",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="pytorch machine learning seq2seq",
    install_requires=["torch"],
)
