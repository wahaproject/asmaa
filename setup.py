#!/usr/bin/python

from distutils.core import setup
from glob import glob


doc_files  = ['LICENSE-ar', 'LICENSE-en', 'AUTHORS', 'ChangeLog', 'README', 'TODO']
data_files = [('share/applications/', ['asmaa.desktop']),
              ('share/icons/hicolor/scalable/apps', ['asmaa.svg']),
              ('share/doc/asmaa', doc_files),
	      	  ('share/asmaa/asmaa-librery/data', glob('asmaa-librery/data/*.*')),
	      	  ('share/asmaa/asmaa-librery/books/', glob('asmaa-librery/books/*')),
	      	  ('share/asmaa/asmaa-librery/index', glob('asmaa-librery/index/*')),
	      	  ('share/asmaa/asmaa-librery/fields-search', glob('asmaa-librery/fields-search/*')), 
	      	  ('share/asmaa/asmaa-librery/waraka-search', glob('asmaa-librery/waraka-search/*')),
	      	  ('share/asmaa/asmaa-data/icons', glob('asmaa-data/icons/*.png')),
              ('share/asmaa/asmaa-data/moshaf', glob('asmaa-data/moshaf/*.*')),
              ('share/asmaa/asmaa-data/db', glob('asmaa-data/db/*.db')),
              ('share/asmaa/modules', glob('modules/*.py')),
	          ('share/fonts/asmaa', glob('fonts/*.*')),
              ]

setup(
      name="Asmaa",
      description='library',
      long_description='library',
      version="2.6.0",
      author='Ahmed Raghdi',
      author_email='asmaaarab@gmail.com',
      url="http://linuxac.org",
      license='Waqf License',
      platforms='Linux',
      scripts=['asmaa'],
      keywords=['book', 'arab'],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: POSIX :: Linux',
          'Development Status :: 4 - Beta',
          'Environment :: X11 Applications :: Gtk',
          'Natural Language :: Arabic',
          'Intended Audience :: End Users/Desktop',
          'Topic :: Desktop Environment :: Gnome',
			],
      data_files=data_files
      )
