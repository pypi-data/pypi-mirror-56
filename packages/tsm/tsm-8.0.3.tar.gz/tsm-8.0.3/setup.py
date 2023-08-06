from setuptools import setup
setup(
  name = 'tsm',
  packages = ['tsm'], # this must be the same as the name above
  version = '8.0.3',
  description = 'Twitter Subgraph Manipulator (TSM)',
  author = 'Deen Freelon',
  author_email = 'dfreelon@gmail.com',
  url = 'https://github.com/dfreelon/tsm/', # use the URL to the github repo
  download_url = 'https://github.com/dfreelon/tsm/tarball/8.0', 
  install_requires = ['python-louvain','networkx'],
  keywords = ['twitter', 'network analysis', 'data science','big data'], # arbitrary keywords
  classifiers = [],
)