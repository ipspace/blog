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

BLOCK_TAG: list = ['p','div','blockquote','pre','h1','h2','h3','h4','table','ul','ol']
VERBOSE: bool = False

def dom_get_tag(de: typing.Union[bs4.element.PageElement,bs4.element.Tag]) -> str:
  if isinstance(de,bs4.element.Tag):
    return de.name
  if isinstance(de,bs4.element.Comment):
    return 'comment'
  if isinstance(de,bs4.element.NavigableString):
    return 'string'
  
  return ''  

def dom_get_class(de: bs4.element.Tag) -> str:
  c_val = de.attrs.get('class')
  if not c_val:
    return ''
  return c_val[0]

def starts_with_markup(oh: str) -> bool:
  for kw in BLOCK_TAG:
    if oh.startswith('<'+kw):
      return True

  return False

def fix_dom_contents(dom: bs4.element.Tag) -> str:
  result = ''
  in_para = False
  in_br = False
  for de in dom.contents:
    dtag = dom_get_tag(de)
    if VERBOSE:
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

def fix_html_markup(oh: str) -> str:
  dom = bs4.BeautifulSoup(oh.strip(),'html.parser')
  return fix_dom_contents(dom)

def div_to_p(oh: str) -> str:
  dom = bs4.BeautifulSoup(oh.strip(),'html.parser')
  result = ''
  for de in dom.contents:
    dtag = dom_get_tag(de)
    if dtag != 'div' or not isinstance(de,bs4.element.Tag):
      result += str(de)
      continue

    c_val = dom_get_class(de)
    if VERBOSE:
      print(f'div class: {c_val}')
    if c_val < 'a':
      de.name = 'p'
    elif c_val == 'bloggerBody':
      result += fix_dom_contents(de)
      continue

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

  if starts_with_markup(old_html):
    if '<!--more' in old_html and 'bloggerBody' not in old_html:
      return None
    fix_html = div_to_p(old_html)
  else:
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