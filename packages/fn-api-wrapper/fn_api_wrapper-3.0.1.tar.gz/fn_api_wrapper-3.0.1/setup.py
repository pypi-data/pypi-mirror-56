import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fn_api_wrapper",
    version="3.0.1",
    author="LupusLeaks",
    author_email="LupusLeaks@gmail.com",
    description="API wrapper for https://fortnite-api.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LupusLeaks/fortnite-api-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
)