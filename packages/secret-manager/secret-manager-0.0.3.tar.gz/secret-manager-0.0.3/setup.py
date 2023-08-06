from setuptools import setup, find_packages

setup(name='secret-manager',
      version='0.0.3',
      license='MIT',
      author='Praveen Kumar',
      author_email='praveen.k@blackbuck.com',
      description='Secret Manager AWS',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False)
