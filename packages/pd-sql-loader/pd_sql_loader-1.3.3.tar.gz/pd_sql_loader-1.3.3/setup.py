from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='pd_sql_loader',
      version='1.3.3',
      license='MIT',
      author='Karev Vitaliy',
      author_email='Vitaliy.Karev@mvideo.ru',
      description='To optimization load DataFrame from databases',
      packages=find_packages(exclude=['tests', 'debug']),
      #packages=['pd_sql_loader'],
      include_package_data=True,
      long_description=open('README.md').read(),
      setup_requires=requirements,
      test_suite='tests')
