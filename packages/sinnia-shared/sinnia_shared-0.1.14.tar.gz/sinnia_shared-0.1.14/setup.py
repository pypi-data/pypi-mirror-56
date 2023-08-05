from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

    # my utils: version='0.1.12',
    # old: version='0.1.13',
    # old + file check: version='0.1.14',

setup(name='sinnia_shared',
      version='0.1.14',
      description='Sinnia Utilities',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/sinnia/scripts/tree/develop/shared',
      author='Sinnia',
      author_email='sonia.segura@sinnia.com',
      packages=find_packages(),
      install_requires=[
        'pymysql',
        'pyyaml'
      ],
      zip_safe=False)
