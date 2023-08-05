from distutils.core import setup
setup(
  name = 'fspathdict',
  packages = ['fspathdict'],
  version = '0.1',
  license='MIT',
  description = 'A small dict that allows filesystem-like path access, including walking up with "../".',
  author = 'CD Clark III',
  author_email = 'clifton.clark@gmail.com',
  url = 'https://github.com/CD3/fspathdict',
  download_url = 'https://github.com/CD3/fspathdict/archive/0.1.tar.gz',
  keywords = ['dict', 'tree', 'filesystem path'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
