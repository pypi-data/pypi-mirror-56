from setuptools import setup, find_packages

version = '0.0.12'

setup(name='6D657461666C6F77',
      version=version,
      description='6D657461666C6F77 is a microframework for Data Science projects',
      author='Machine Learning Infrastructure team',
      author_email='mli@netflix.com',
      license='Apache License 2.0',
      packages=find_packages(exclude=['metaflow_test']),
      py_modules=['metaflow', ],
      package_data={'metaflow' : ['tutorials/*/*']},
      entry_points='''
        [console_scripts]
        metaflow=metaflow.main_cli:main
      ''',
      install_requires = [
        'click',
        'requests',
        'boto3'
      ],
      tests_require = [
        'coverage'
      ])
