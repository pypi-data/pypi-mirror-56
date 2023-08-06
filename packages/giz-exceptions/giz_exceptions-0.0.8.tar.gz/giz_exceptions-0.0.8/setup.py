import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="giz_exceptions",
    version="0.0.8",
    author="Matthew Pang",
    author_email="mpang@gizwits.com",
    description="Exceptions for Gizwits PaaS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=None,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'djangorestframework',
    ]
)
