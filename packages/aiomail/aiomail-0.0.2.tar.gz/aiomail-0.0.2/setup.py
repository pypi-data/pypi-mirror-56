import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiomail",
    version="0.0.2",
    author="fxdmhtt",
    author_email="yuanjunkang@gmail.com",
    description="easy and async e-mail package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fxdmhtt/aiomail.git",
    packages=list(filter(lambda x: x.startswith('aiomail'), setuptools.find_packages())),
    install_requires=[
        'aiosmtplib',
        'drymail',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
