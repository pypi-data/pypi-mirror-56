from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pybackupper',
      version='1.2',
      url='https://github.com/SavelevMatthew/backupper',
      license='MIT',
      author='Matthew Savelev',
      author_email='savelevmatthew@gmail.com',
      description='Realise files copy on your Cloud Services',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(exclude=['tests']),
      zip_safe=False)
