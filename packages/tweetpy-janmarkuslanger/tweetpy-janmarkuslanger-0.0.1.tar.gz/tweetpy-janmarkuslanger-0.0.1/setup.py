import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tweetpy-janmarkuslanger",
    version="0.0.1",
    author="Jan-Markus Langer",
    author_email="janmarkuslanger10121994@gmail.com",
    description="Create your own twitter bot without the api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/janmarkuslanger/tweetpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
