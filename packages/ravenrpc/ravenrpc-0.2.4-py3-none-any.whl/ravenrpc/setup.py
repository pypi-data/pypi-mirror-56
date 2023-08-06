import setuptools

with open("ravenrpc/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ravenrpc", # Replace with your own username
    version="0.2.4",
    author="JonPizza",
    author_email="jon@jon.network",
    description="Ravencoin RPC client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JonPizza/ravenrpc",
    packages=['ravenrpc'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
