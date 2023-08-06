"""mv_regex
  Rename files using regular expressions. The program will prompt the user for
  confirmation before renaming (unless the "--force" options is used).

Usage:
  mv_regex [options] <search> <replace> <files>...

Arguments:
  <search>        Regular expression to search.
  <replace>       Regular expression to use as replace.
  <files>         List of files on which to do the replacement.

Options:
  -f, --force     Force move, don't prompt for user interaction.
  -d, --dirname   Rename directory name (not the file-name).
  -h, --help      Show help.
      --version   Show version.


Example:
  mv_regex "(.*)(_raw.svg)" "\1.svg" *.svg

Copyright:
  T.W.J. de Geus
  tom@geus.me
  www.geus.me
"""

import sys
import os
import re
import docopt
import click
import pkg_resources

__version__ = pkg_resources.require("mv_regex")[0].version

# --------------------------------------------------------------------------------------------------

def main():

  args = docopt.docopt(__doc__, version=__version__)

  # check if all input files actually exist
  for file in args['<files>']:
    if not os.path.isfile(file) and not os.path.isdir(file):
      print('Input {1:s} does not exist'.format(file))
      sys.exit(1)

  # select directory name
  if args['--dirname']: args['<files>'] = [os.path.split(file)[0] for file in args['<files>']]

  # only keep input files that match the input regular-expression
  args['<files>'] = [file for file in args['<files>'] if re.match(args['<search>'],file)]

  # rename the remaining files
  args['renamed'] = [re.sub(args['<search>'],args['<replace>'],file) for file in args['<files>']]

  # only keep files that will be renamed
  idx = [i for i,(old,new) in enumerate(zip(args['<files>'], args['renamed'])) if old != new]
  args['<files>'] = [args['<files>'][i] for i in idx]
  args['renamed'] = [args['renamed'][i] for i in idx]

  # no files remaining -> quit
  if len(args['renamed']) == 0:
    sys.exit(0)

  # prompt the user for confirmation
  if not args['--force']:

    # - construct print-format to align output
    w   = max([len(file) for file in args['<files>']])
    fmt = 'mv {file:'+str(w)+'s} {new:s}'

    # - print all files
    for file,new in zip(args['<files>'],args['renamed']):
      print(fmt.format(file=file,new=new))

    # - prompt user
    if not click.confirm('Proceed?'):
      sys.exit(1)

  # proceed with the renaming of all files
  for file,new in zip(args['<files>'],args['renamed']):
    os.rename(file,new)

