from distutils.core import setup
setup(
  name = 'bitk',         # How you named your package folder (MyLib)
  packages = ['bitk'],   # Chose the same as "name"
  version = '0.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Toolkit for Business Intelligence, who wants things simple without hassle',   # Give a short description about your library
  author = 'Loc Nguyen',                   # Type in your name
  author_email = 'your.email@domain.com',      # Type in your E-Mail
  url = 'https://github.com/locnguyen14061996/bitk',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/locnguyen14061996/bitk/archive/0.0.3.tar.gz',    # I explain this later on
  keywords = ['python3', 'simple','business intelligence'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas', 
          'psycopg2'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
  ],
)