Simple filesystem based file tagging.


*Latest release 20191201*:
New "edit" subcommand to rename files and edit tags.

Simple filesystem based file tagging.

Tags are stored in a file `.fstags` in directories
with a line for each entry in the directory
consisting of the directory entry name and the associated tags.

The tags for a file are the union of its direct tags
and all relevant ancestor tags,
with priority given to tags closer to the file.

For example, a media file for a television episode with the pathname
`/path/to/series-name/season-02/episode-name--s02e03--something.mp4`
might obtain the tags:

    series.title="Series Full Name"
    season=2
    sf
    episode=3
    episode.title="Full Episode Title"

from the following `.fstags` files and entries:
* `/path/to/.fstags`:
  `series-name sf series.title="Series Full Name"`
* `/path/to/series-name/.fstags`:
  `season-02 season=2`
* `/path/to/series-name/season-02.fstags`:
  `episode-name--s02e03--something.mp4 episode=3 episode.title="Full Episode Title"`

Tags may be "bare", or have a value.
If there is a value it is expressed with an equals (`'='`)
followed by the JSON encoding of the value.

## Class `FSTagCommand`

MRO: `cs.cmdutils.BaseCommand`  
fstag main command line class.

## Class `FSTags`

A class to examine filesystem tags.

## Function `loadrc(rcfilepath)`

Read rc file, return rules.

## Function `main(argv=None)`

Command line mode.

## Class `PathTags`

Class to manipulate the tags for a specific path.

## Class `RegexpTagRule`

A regular expression based `Tag` rule.

## Function `rfilepaths(path)`

Generator yielding pathnames of files found under `path`.

## Class `Tag`

A Tag has a `.name` (`str`) and a `.value`.

The `name` must be a dotted identifier.

A "bare" `Tag` has a `value` of `None`.

## Class `TagFile`

A reference to a specific file containing tags.



# Release Log

*Release 20191201*:
New "edit" subcommand to rename files and edit tags.

*Release 20191130.1*:
Initial release: fstags, filesystem based tagging utility.
