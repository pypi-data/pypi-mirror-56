import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='example-pkg-avishek',  
     version='0.1',
     author="Avishek Das",
     author_email="avishek.das.ayan@gmail.com",
     description="A simple function",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/silenthunter007/test_pip",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )