from distutils.core import setup
setup(
  name = 'ai6',
  packages = ['ai6'],
  version = '0.11',
  license='MIT',
  description = 'Artificial Intelligence Example',
  author = 'ccckmit',
  author_email = 'ccckmit@gmail.com',
  url = 'https://github.com/ccc-py/ai6',
  download_url = 'https://github.com/ccc-py/ai6/archive/v0.11.tar.gz',
  keywords = ['ai', 'nn', 'neural'],
  install_requires=[
          'numpy',
      ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)