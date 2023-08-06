import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='dingdong_sdk',
     version='0.0.1',
     scripts=['dingdong_sdk/'] ,
     author="Centre of Technology and Innovation",
     author_email="cti@apiit.edu.my",
     description="The DingDong SDK",
     long_description="The DingDong SDK allows CTI developers to interact with the endpoints with ease by using simple functions provided.",
   long_description_content_type="text/markdown",
     url="https://bitbucket.org/ctiteam/dingdong-sdk",
     packages=setuptools.find_packages(),
     classifiers=[
        "Intended Audience :: Developers",
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )