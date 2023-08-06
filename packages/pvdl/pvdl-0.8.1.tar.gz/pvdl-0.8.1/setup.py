from distutils.core import setup
setup(
  name = 'pvdl',         # How you named your package folder (MyLib)
  packages = ['pvdl'],   # Chose the same as "name"
  version = '0.8.1',      # Start with a small number and increase it with every change you make
  license='GPL-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'PacktPub Video Downloader, The Easiest way to download any Packt video tutorial using subscription',   # Give a short description about your library
  author = 'TheWeirdDev',                   # Type in your name
  author_email = 'alireza6677@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/TheWeirdDev/PacktPub-Video-Downloader',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/TheWeirdDev/PacktPub-Video-Downloader/archive/0.8.1.tar.gz',    # I explain this later on
  keywords = ['packt','packtpub','packtpub-downloader','packtpub-video-downloader','video-downloader', 'subscription','free-trial'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'tqdm',
          'requests',
          'pycurl'
      ],
  entry_points = {
        'console_scripts': ['pvdl=pvdl.pvdl:main'],
    },
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: End Users/Desktop',      # Define that your audience are developers
    'Topic :: Multimedia :: Video',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
  ],
)
