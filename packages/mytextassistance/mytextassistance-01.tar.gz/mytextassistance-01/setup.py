from distutils.core import setup
setup(
  name = 'mytextassistance',         # How you named your package folder (MyLib)
  packages = ['mytextassistance'],   # Chose the same as "name"
  version = '01',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package aims to provide users with some of the features they may need when working with texts.',   # Give a short description about your library
  author = 'AliReza Alemi',                   # Type in your name
  author_email = 'alireza.alemi76@icloud.com',      # Type in your E-Mail
  url = 'https://github.com/aalemi76/mytextassistance',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/aalemi76/mytextassistance/archive/01.tar.gz',    # I explain this later on
  keywords = ['Supervised', 'Text', 'Featueres'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'python version 3 would be preferred'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
