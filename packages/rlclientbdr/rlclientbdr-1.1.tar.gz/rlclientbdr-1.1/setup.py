import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='rlclientbdr',
     version='1.1',
     scripts=[],
     author="Robbert van der Gugten",
     author_email="robbert.van.der.gugten@bigdatarepublic.nl",
     description="Client for the reinforcement learning knowledge sharing",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )