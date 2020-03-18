#!/usr/bin/env python3
#
# Scan the blog posts and create metadata and template files
#
# - blog archive data files
# - tag cloud (TBD)
#

import sys
import os
import argparse
import yaml
import json
import re
from datetime import date, datetime, timezone
import dateutil.parser
from types import SimpleNamespace
from jinja2 import Environment, FileSystemLoader, Undefined, StrictUndefined, make_logging_undefined

LOGGING=False
VERBOSE=False
FAILED=False
WEIGHT=0.97

def parseCLI():
  parser = argparse.ArgumentParser(description='Create blog metadata and templates')
  parser.add_argument('--posts', dest='path', action='store', default='content/posts/',
                  help='Path to blog content')
  parser.add_argument('--data', dest='data', action='store', default='data/',
                  help='Data directory')
  parser.add_argument('--template', dest='template', action='store', default='templates/',
                  help='Template directory')
  parser.add_argument('--output', dest='output', action='store', default='snippets/',
                  help='Snippet directory')
  parser.add_argument('--content', dest='content', action='store', default='content/',
                  help='Content directory')
  parser.add_argument('--log', dest='logging', action='store_true',
                  help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',
                  help='Enable more verbose logging')
  return parser.parse_args()

def failure(s):
  print(s)
  FAILED=True

def scanFile(path,archive,tags):
  if VERBOSE:
    print("Reading file %s" % path)

  with open(path, 'r') as stream:
    content = re.split("---\n",stream.read())
    frontmatter = content[1]

    try:
      doc = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
      return failure("Error parsing YAML header in %s: %s" % (path,exc))

    date = doc.get('date')
    if not date:
      return failure("Date header missing in %s" % path)

    try:
      pubdate = dateutil.parser.parse(date)
    except:
      return failure("Date parsing error %s in %s" % (sys.exc_info()[0],path))

    year = pubdate.year
    month = pubdate.month

    archive.setdefault(year,{})
    archive[year].setdefault(month,SimpleNamespace(count=0))
    archive[year][month].count = archive[year][month].count + 1

    age = datetime.now(timezone.utc) - pubdate
    weight = WEIGHT ** age.days

    for t in doc.get('tags',[]):
      tags.setdefault(t,SimpleNamespace(count=0,weight=0))
      tags[t].count = tags[t].count + 1
      tags[t].weight = tags[t].weight + weight
  return

def template(j2,data,dest):
  ENV = Environment(loader=FileSystemLoader('.'),trim_blocks=True,lstrip_blocks=True)
  template = ENV.get_template(j2)

  with open(dest,'w') as output:
    output.write(template.render(**data))
    output.close()

def shuffleArchive(a):
  data = []
  for year in sorted(a.keys(),reverse=True):
    record = { 'year':year, 'rows':[], 'count':0 }
    for month in sorted(a[year].keys(),reverse=True):
      item  = a[year][month]
      mdate = date(year,month,1)
      record['rows'].append({
        'month': month,
        'count': item.count,
        'text':  mdate.strftime('%B %Y'),
        'url':   mdate.strftime('/%Y/%m')
        })
      record['count'] = record['count']+item.count
    data.append(record)
  return data

def createArchiveStubs(path,archive):
  for year in archive.keys():
    with open('{}archy/{}.md'.format(path,year),'w') as output:
      output.write('{"date": "%i-01-01 00:00:00"}\n' % year)
      output.close()
    for month in archive[year].keys():
      with open('{}archm/{}-{:02d}.md'.format(path,year,month),'w') as output:
        output.write('{"date": "%i-%02i-01 00:00:00"}\n' % (year,month))
        output.close()

def writeArchiveData(args,archive):
  sbArchive = shuffleArchive(archive)

  with open(args.data+'archive.json','w') as output:
    output.write(json.dumps(sbArchive))
    output.close()

  template(args.template+'archive.j2',{ 'data': sbArchive },args.output+'archive-sidebar.html')
  createArchiveStubs(args.content,archive)

def scanPosts(path,archive,tags):
  if LOGGING:
    print("Scanning %s" % path)

#  for dir,subdirs,files in os.walk(path):
#    for f in files:
#      scanFile(os.path.join(dir,f),archive,tags)
#    for f in subdirs:
#      scanPosts(os.path.join(dir,f),archive,tags)
  with os.scandir(path) as dir:
    for entry in dir:
      if entry.is_dir():
        if not entry.name.startswith('.'):
          scanPosts(os.path.join(path,entry.name),archive,tags)
      elif entry.is_file():
        scanFile(os.path.join(path,entry.name),archive,tags)

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

archive = {}
tags = {}
scanPosts(args.path,archive,tags)

writeArchiveData(args,archive)

#for t in sorted(tags.keys(), key=lambda x: tags[x].weight, reverse=True):
#  print("%-20s %f %i" % (t,tags[t].weight,tags[t].count))