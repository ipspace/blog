#!/usr/bin/env python3
#

import re
import os
import argparse
import yaml
import common
import typing
import textwrap
import bs4

def parseCLI():
  parser = argparse.ArgumentParser(description='Fix old HTML markup')
  parser.add_argument('files', nargs='+',action='store',help='Files to check/fix')
  parser.add_argument('-v',dest='verbose',action='store_true')
  return parser.parse_args()

BLOCK_TAG: list = ['p','div','blockquote','pre','h1','h2','h3','h4','table','ul','ol']

def dom_get_tag(de: bs4.element.PageElement) -> str:
  if isinstance(de,bs4.element.Comment):
    return 'comment'
  if isinstance(de,bs4.element.NavigableString):
    return 'string'
  
  return de.name

def starts_with_markup(oh: str) -> bool:
  for kw in BLOCK_TAG:
    if oh.startswith('<'+kw):
      return True

  return False

def fix_html_markup(oh: str, verbose: bool = False) -> str:
  dom = bs4.BeautifulSoup(oh.strip(),'html.parser')
  result = ''
  in_para = False
  in_br = False
  for de in dom.contents:
    dtag = dom_get_tag(de)
    if verbose:
      print(f'{dtag}: {str(de)}')
    if dtag == 'comment':
      if str(de) == 'more' and in_para:
        in_para = False
        result += "</p>\n"
      result += f'<!--{str(de)}-->'
      continue
    if dtag == 'br':
      if in_br:
        continue
      if in_para:
        result += "</p>\n"
        in_para = False
      in_br = True
      continue

    in_br = False
    if dtag in BLOCK_TAG:
      if in_para:
        result += '</p>\n'
        in_para = False
    else:
      if not in_para:
        result += '<p>'
        in_para = True

    result += str(de)

  if in_para:
    result += '</p>\n'
  return result

def div_to_p(oh: str) -> str:
  dom = bs4.BeautifulSoup(oh.strip(),'html.parser')
  result = ''
  for de in dom.contents:
    dtag = dom_get_tag(de)
    if dtag != 'div':
      result += str(de)
      continue

    c_val = de.attrs.get('class')
    if not c_val or c_val[0] < 'a':
      de.name = 'p'
    result += str(de)

  return result

def fix_html_file(fname: str, verbose: bool = False) -> typing.Optional[str]:
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

  if starts_with_markup(old_html):
    if '<!--more' in old_html:
      return None
    fix_html = div_to_p(old_html)
  else:
    fix_html = fix_html_markup(old_html,verbose)

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
  args = parseCLI()
  for fname in args.files:
    if fix_html_file(fname,bool(args.verbose)):
      print(f"... fixed {fname}")

main()