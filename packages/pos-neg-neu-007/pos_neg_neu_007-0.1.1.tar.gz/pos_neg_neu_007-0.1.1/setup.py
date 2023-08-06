
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
   name="pos_neg_neu_007",
   version="0.1.1",
   author="Ankit Srivastava 007",
   author_email="ankits.7733@gmail.com",
   description="Get positive,negative response for given sentence",
   long_description=README,
   long_description_content_type="text/markdown",
   #url="https://github.com/pypa/sampleproject",
   packages=find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
)

install_requires = [
    'textblob',
    'nltk'
]
if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
