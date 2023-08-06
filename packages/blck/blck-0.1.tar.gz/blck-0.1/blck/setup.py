from distutils.core import setup
setup(
  name = 'blck',         # How you named your package folder (MyLib)
  packages = ['blck'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='GNU',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'raukoras',                   # Type in your name
  author_email = 'raukoras@live.fr',      # Type in your E-Mail
  url = 'https://github.com/raukoras/blck',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/raukoras/blck/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['blockchain'],   # Keywords that define your package best
  install_requires=[
        'PostgreSQL',
        'flask', 
        'flask-cors', 
        'psycopg2' ,
        'libgcc_mutex',
        'asn1crypto','ca-certificates','certifi','cffi','chardet','click','cryptography','idna','itsdangerous','jinja2','krb5','libedit','libffi','libgcc-ng','libpq','libstdcxx-ng','markupsafe','ncurses','openssl','pip','pycparser','pycrypto','pyopenssl','pysocks','python','readline','requests','setuptools','six','sqlite','tk','urllib3','werkzeug','wheel','xz','zlib' 
    ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)