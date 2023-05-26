#!/usr/bin/env python3
#
# Scan the blog posts and create a list of URLs used in those blog posts
#

import os
import sys
import argparse
import glob
import re
import yaml
import common

LOGGING=False
VERBOSE=False

def parseCLI():
  parser = argparse.ArgumentParser(description='List URLs used by blog psots in a directory(tree)')
  parser.add_argument('dir', nargs='*',action='store',help='Directory to process')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  parser.add_argument('--no-section', dest='no_section', action='store_true',help='Pages are not groups into a section')

  return parser.parse_args()

def find_pre_start(lines: list, cnt: int) -> int:
  for i in range(cnt-1,0,-1):
    if lines[i].find('```') == 0:
      return i
  return -1

def replace_markup_tag(line: str, tag: str = '') -> str:
  if tag:
    return re.sub(r'[A-Z]+:\s+(.*)',"{{<"+tag+">}}\\1{{</"+tag+">}}" ,line)
  else:
    chunks = re.split(r'\A([A-Z-]+):\s+',line,1)
    tag = chunks[1].lower()
    if 'caption' in tag:
      print(f"WARNING: leftover caption tag: {line}")
      return "{{<cc>}}"+chunks[2]+"{{</cc>}}"
    else:
      return "{{<note "+tag+">}}"+chunks[2]+"{{</note>}}"

def fix_blockquote(m):
  text = m.group(1)
  lines = text.split('\n')
  for i in range(len(lines)):
    lines[i] = "> " + lines[i]

  return '\n'.join(lines)

def fix_figure(m):
  text = m.group(1)
  img_match = re.search(r'<img src=.([^\'"]+)',text)
  src = img_match.group(1) if img_match else ''
  if not src:
    print(f"WARNING: cannot find image in figure: {m.group(0)}")
    return m.group(0)
  
  cap_match = re.search(r'<figcaption>(.*?)</figcaption>',text)
  markup = '{{<figure src="'+src+'"'
  if cap_match:
    caption = cap_match.group(1)
    caption = re.sub('<br\s*/>','. ',caption)
    markup = markup + ' caption="'+caption+'"'
  markup = markup + '>}}'
  return markup

def process_markup(text: str,fname: str) -> str:
  lines = text.split('\n')
  for i in range(len(lines)):
    if lines[i].find('CAPTION:') != 0 or i == 0:
      continue

    if lines[i-1] != '```':
      print(f"WARNING: {fname}:{i} - CAPTION: must be preceded by a code block")
      continue

    j = find_pre_start(lines,i-1)
    if j < 0:
      print(f"WARNING: {fname}:{i} - cannot find start of code block preceding CAPTION")
      continue

    lines = lines[:j] + [replace_markup_tag(lines[i],'cc')] + lines[j:i] + lines[i+1:]

  for i in range(len(lines)):
    if not re.search(r"\A[A-Z-]+:\s+",lines[i]):
      continue
    lines[i] = replace_markup_tag(lines[i])

  for i in range(len(lines)):
    m = re.search(r"\A!\[(.*?)\]\((.*?)\)",lines[i])
    if m:
      lines[i] = "{{<figure src=\""+m.group(2)+"\" caption=\""+m.group(1)+"\">}}"

  text = '\n'.join(lines)
  text = re.sub(r'<blockquote class=.cite..*?>(.*?)</blockquote>',fix_blockquote,text)
  text = re.sub(
            r'<figure markdown.*?>(.*?)</figure>',fix_figure,text,
            count=0,
            flags=re.DOTALL+re.MULTILINE+re.IGNORECASE)
  return text

def migrate_post(path: str,args: argparse.Namespace) -> None:
  if VERBOSE:
    print("Reading file %s" % path)

  with open(path, 'r') as stream:
    content = stream.read()
    stream.close()

  if content.find('---') == 0:
    print("Skipping %s, already migrated" % path)
    return
  
  chunks = content.split('\n\n')
  frontmatter = chunks[0]
  text = '\n\n'.join(chunks[1:])

  try:
    if frontmatter.find('#') == 0:
      doc = { 'title': frontmatter[1:].strip() }
    else:
      doc = yaml.safe_load(frontmatter)
  except Exception as exc:
    print(f"Error parsing YAML header {path}: {exc}")
    return

  if not doc:
    print(f"Unable to parse frontmatter, skipping {path}")
    print(frontmatter)
    print('---')
    return

  cfg_yaml = os.path.dirname(path) + '/config.yaml'
  config = {}
  if os.path.isfile(cfg_yaml):
    with open(cfg_yaml, 'r') as stream:
      config = yaml.safe_load(stream)
      stream.close()

  doc['minimal_sidebar'] = True
  doc.pop('publish',None)

  path_chunks = os.path.abspath(path).split('content')
  if 'index' in doc:
    doc['url'] = os.path.dirname(path_chunks[1])+"/"
  else:
    doc['url'] = path_chunks[1].replace('.md','.html')

  if not args.no_section:
    try:
      kb_section = path_chunks[1].split('/')[-2]
      if kb_section:
        doc['kb_section'] = kb_section
    except:
      pass

  text = process_markup(text,path)
  if 'cc>' in text or 'caption>' in text or '```' in text:
    doc['pre_scroll'] = True
  
  with open(path, 'w') as stream:
    stream.write('---\n')
    yaml.dump(doc,stream)
    stream.write('---\n')
    stream.write(text)
    stream.close()

  print(f"Migrated {path}")

def scan_posts(path,args) -> None:
  if LOGGING:
    print("Scanning %s" % path)

  if os.path.isfile(path):
    migrate_post(path,args)
    return

  for entry in glob.glob(path + "/*"):
    if VERBOSE:
      print("Inspecting %s " % entry)
    if os.path.isdir(entry):
      scan_posts(entry,args)
    elif os.path.isfile(entry) and '.md' in entry:
      migrate_post(entry,args)

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose
if not args.dir:              # Iterate over all posts when nothing is specified
  scan_posts('.',args)
else:
  for entry in args.dir:
    scan_posts(entry,args)
