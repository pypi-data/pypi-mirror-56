from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Packages required for this module to be executed
def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()

def list_test_reqs(fname='test_requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()

        
setup(name='feature_engine',
      version='0.3.1',
      description='Feature engineering package that follows sklearn functionality',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/solegalli/feature_engine',
      author='Soledad Galli',
      author_email='solegalli1@gmail.com',
      packages=['feature_engine'],
      license= 'BSD 3 clause',
      install_requires=list_reqs(),
      tests_require=list_test_reqs(),
      classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: 'BSD 3 clause'",
        "Operating System :: OS Independent",
        ],
      zip_safe=False)

