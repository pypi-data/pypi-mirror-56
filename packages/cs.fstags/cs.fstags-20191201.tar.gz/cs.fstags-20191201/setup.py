#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.fstags',
  description = 'Simple filesystem based file tagging.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20191201',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  entry_points = {'console_scripts': ['fstags = cs.fstags:main']},
  include_package_data = True,
  install_requires = ['cs.cmdutils', 'cs.edit', 'cs.lex', 'cs.logutils', 'cs.pfx', 'cs.threads', 'icontract'],
  keywords = ['python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description = '*Latest release 20191201*:\nNew "edit" subcommand to rename files and edit tags.\n\nSimple filesystem based file tagging.\n\nTags are stored in a file `.fstags` in directories\nwith a line for each entry in the directory\nconsisting of the directory entry name and the associated tags.\n\nThe tags for a file are the union of its direct tags\nand all relevant ancestor tags,\nwith priority given to tags closer to the file.\n\nFor example, a media file for a television episode with the pathname\n`/path/to/series-name/season-02/episode-name--s02e03--something.mp4`\nmight obtain the tags:\n\n    series.title="Series Full Name"\n    season=2\n    sf\n    episode=3\n    episode.title="Full Episode Title"\n\nfrom the following `.fstags` files and entries:\n* `/path/to/.fstags`:\n  `series-name sf series.title="Series Full Name"`\n* `/path/to/series-name/.fstags`:\n  `season-02 season=2`\n* `/path/to/series-name/season-02.fstags`:\n  `episode-name--s02e03--something.mp4 episode=3 episode.title="Full Episode Title"`\n\nTags may be "bare", or have a value.\nIf there is a value it is expressed with an equals (`\'=\'`)\nfollowed by the JSON encoding of the value.\n\n## Class `FSTagCommand`\n\nMRO: `cs.cmdutils.BaseCommand`  \nfstag main command line class.\n\n## Class `FSTags`\n\nA class to examine filesystem tags.\n\n## Function `loadrc(rcfilepath)`\n\nRead rc file, return rules.\n\n## Function `main(argv=None)`\n\nCommand line mode.\n\n## Class `PathTags`\n\nClass to manipulate the tags for a specific path.\n\n## Class `RegexpTagRule`\n\nA regular expression based `Tag` rule.\n\n## Function `rfilepaths(path)`\n\nGenerator yielding pathnames of files found under `path`.\n\n## Class `Tag`\n\nA Tag has a `.name` (`str`) and a `.value`.\n\nThe `name` must be a dotted identifier.\n\nA "bare" `Tag` has a `value` of `None`.\n\n## Class `TagFile`\n\nA reference to a specific file containing tags.\n\n\n\n# Release Log\n\n*Release 20191201*:\nNew "edit" subcommand to rename files and edit tags.\n\n*Release 20191130.1*:\nInitial release: fstags, filesystem based tagging utility.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.fstags'],
)
