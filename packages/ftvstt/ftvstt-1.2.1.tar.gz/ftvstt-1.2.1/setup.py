import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='ftvstt',
     version='1.2.1',
     packages=setuptools.find_packages() ,
     author="France Télévisions innovations et développement",
     author_email="pierre-andre.long@francetv.fr",
     description="Transcription APIs encapsulation",
     long_description=long_description,
   long_description_content_type="text/markdown",
     install_requires=['boto3==1.10.4', 'google-cloud-speech==1.2.0', 'requests==2.22.0'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
