
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='chameleone_status',
    version='0.2.3',
    scripts=['chameleone_status.py'],
    author="avinash",
    author_email="avinashn686@gmail.com",
    description="chameleone status sender",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
