import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cs2py",
    version="0.0.1",
    author="Ethosa",
    author_email="social.ethosa@gmail.com",
    description="C# to Python language translator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ethosa/cs2py",
    packages=setuptools.find_packages(),
    license="LGPLv3",
    keywords="c# to python language translator ethosa konard",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Github" : "https://github.com/Ethosa/cs2py",
        "Documentation" : "https://github.com/Ethosa/cs2py",
    },
    python_requires=">=3",
    install_requires=["retranslator"]
)