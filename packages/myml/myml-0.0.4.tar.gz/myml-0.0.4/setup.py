import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
  name = 'myml',
  packages = setuptools.find_packages(),
  version = '0.0.4',
  description = 'Implementations of machine learning algorithms',
  long_description = long_description,
  author = 'Brett Clark',
  author_email = 'clarkbab@gmail.com',
  url = 'https://github.com/clarkbab/myml',
  keywords = ['machine learning'],
  classifiers = []
)
