from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'easy_spotify',         # How you named your package folder (MyLib)
  packages = ['easy_spotify'],   # Chose the same as "name"
  version = 'v0.3.4-alpha',      # Start with a small number and increase it with every change you make
  description = 'Simple access the Spotify WEB API for general requests about artists, albums or songs',
  author = 'Tilney-Bassett Oktarian',
  author_email = 'ogt@connect.ust.hk',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url = 'https://github.com/OktarianTB/easy_spotify/blob/master/README.md',
  download_url = 'https://github.com/OktarianTB/easy_spotify/archive/v0.3.4-alpha.tar.gz',
  keywords = ['SPOTIFY', 'WEB API'],
  install_requires=[
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)