#!/usr/bin/env python3
#

import re
import os
import argparse
import common
import typing
import bs4

def parseCLI():
  parser = argparse.ArgumentParser(description='Fix old HTML markup')
  parser.add_argument('files', nargs='+',action='store',help='Files to check/fix')
  parser.add_argument('-v',dest='verbose',action='store_true')
  return parser.parse_args()

def dom_get_tag(de: typing.Union[bs4.element.PageElement,bs4.element.Tag]) -> str:
  if isinstance(de,bs4.element.Tag):
    return de.name
  if isinstance(de,bs4.element.Comment):
    return 'comment'
  if isinstance(de,bs4.element.NavigableString):
    return 'string'
  
  return ''  

def fix_html_markup(oh: str) -> str:
  dom = bs4.BeautifulSoup(oh.strip(),'html.parser')
  result = ''
  for de in dom.contents:
    dtag = dom_get_tag(de)
    if dtag == 'comment':                               # Recreate the comments
      result += f'<!--{str(de)}-->'
      continue

    if dtag != 'p':                                     # All other tags but P are passed through
      result += str(de)
      continue

    pct = de.contents
    if len(pct) != 1:
      result += str(de)
      continue

    if str(pct[0]).strip():
      result += str(de)

  return result

def fix_html_file(fname: str) -> typing.Optional[str]:
  if not(os.path.isfile(fname)):
    raise RuntimeError(f'File does not exist: {fname}')

  (file,ext) = os.path.splitext(fname)
  if ext != ".html":
    return None

  with open(fname, 'r') as stream:
    content = re.split(common.YAML_DELIMITER,stream.read())
    if len(content) < 3:
      return None
    fm = content[1]
    old_html = common.YAML_DELIMITER.join(content[2:]).strip()

  if not(old_html):
    raise RuntimeError(f'Cannot get HTML text from {fname}')

  fix_html = fix_html_markup(old_html)

  if fix_html == old_html:
    return None

  with open(fname,"wt") as output:
    output.write('---\n')
    output.write(fm)
    output.write('---\n')
    output.write(fix_html)
    output.close()
    return fname

def main() -> None:
  global VERBOSE
  args = parseCLI()
  VERBOSE = bool(args.verbose)
  for fname in args.files:
    if fix_html_file(fname):
      print(f"... fixed {fname}")

main()