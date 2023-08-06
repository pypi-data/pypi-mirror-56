from setuptools import setup, find_packages
 

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='partial_web_file',
      version='1.0.1',
      url='https://github.com/alexappsnet/pypartialwebfile',
      license='MIT',
      author='Alex Malko',
      author_email='alex@alexapps.net',
      description='Utility methods to get the partial content of the web file or to unarchive a single file from a huge remote web zip.',
      packages=find_packages(exclude=['tests']),
      long_description=long_description,
      long_description_content_type="text/markdown"
)