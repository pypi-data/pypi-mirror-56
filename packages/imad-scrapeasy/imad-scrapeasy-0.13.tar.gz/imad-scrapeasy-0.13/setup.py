from distutils.core import setup
setup(
  name = 'imad-scrapeasy',
  packages = ['scrapeasy'],
  version = '0.13',
  license='MIT',
  description = 'Scraping in python made easy - receive the content you like in just one line of code!',
  author = 'Joel Barmettler',
  author_email = 'test@test.com',
  url = 'https://github.com/imadelh/Scrapeasy',
  download_url = 'https://github.com/imadelh/Scrapeasy/archive/pypi-release-imad-0.1.tar.gz',
  keywords = ['scraping', 'easy', 'scraper', 'website', 'download', 'links', 'images', 'videos'],
  install_requires=[
              'pip==18.1',
              'bumpversion==0.5.3',
              'wheel==0.32.1',
              'watchdog==0.9.0',
              'flake8==3.5.0',
              'tox==3.5.2',
              'coverage==4.5.1',
              'Sphinx==1.8.1',
              'twine==1.12.1',
              'pytest==3.8.2',
              'pytest-runner==4.2',
              'tables==3.4.4',
              'tqdm==4.36.2',
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
