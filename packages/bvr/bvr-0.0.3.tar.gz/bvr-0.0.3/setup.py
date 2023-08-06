
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='bvr',  
     version='0.0.3',
     scripts=[],
     author="doedotdev",
     author_email="doedotdev@gmail.com",
     description="BVR: Log like a Beaver",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/doedotdev/bvr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )

 # TODO: add keywords
 # TODO: add license type
