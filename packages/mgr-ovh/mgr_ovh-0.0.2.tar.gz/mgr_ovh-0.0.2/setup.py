import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mgr_ovh", # Replace with your own username
    version="0.0.2",
    author="1V14713",
    author_email="mathieu.gravil@gmail.com",
    description="an ovh sdk to consume api" ,
    long_description="ovh sdk python",
    long_description_content_type="text/markdown",
    url="https://framagit.org/mathieugravil/myOvh",
    packages=setuptools.find_packages(),
      install_requires=[            # I get to this in a second
          'ovh',
          ],
    classifiers=[
        "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
