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
import dateutil.tz
from types import SimpleNamespace
from jinja2 import Environment, FileSystemLoader, Undefined, StrictUndefined, make_logging_undefined
import common

LOGGING=False
VERBOSE=False
FAILED=False
WEIGHT=0.97
RECENT_TAGS=10
MIN_TAG_COUNT=10
RECENT_PERIOD=180

CONFIG={}
BLOCK_TAGS=[]
NOW=datetime.now(timezone.utc)

def parseCLI():
  parser = argparse.ArgumentParser(description='Create blog metadata and templates')
  parser.add_argument('--config', dest='config', action='store', default='config.yaml',
                  help='Hugo configuration file')
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
  parser.add_argument('--quiet', dest='quiet', action='store_true',
                  help='Report only major errors')
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

    # Parsing the publication date is weird
    #
    # * YAML might already have generated the datetime timestamp, so we have to go to string first
    # * We have to use dateutil.parser so we can parse 'meaningful' and ISO timestamps
    # * The result might or might not have a timezone, so we have to adjust that as well
    #
    try:
      pubdate = dateutil.parser.parse(str(date))
    except:
      return failure("Date %s parsing error %s in %s" % (date,sys.exc_info()[0],path))

    if pubdate.tzinfo is None:
      pubdate = pubdate.replace(tzinfo=timezone.utc)

    if pubdate > NOW:
      if not args.quiet:
        print("Blog post %s is not published yet, skipping" % path)
      return

    # Now we should know what the publish datetime is, and it's not in the future,
    # so let's move forward and get some work done
    #
    year = pubdate.year
    month = pubdate.month

    archive.setdefault(year,{})
    archive[year].setdefault(month,SimpleNamespace(count=0))
    archive[year][month].count = archive[year][month].count + 1

    age = datetime.now(timezone.utc).date() - pubdate.date()
    weight = WEIGHT ** age.days

    if doc.get('tags'):
      for t in doc.get('tags'):
        if t in BLOCK_TAGS:
          continue
        tags.setdefault(t,SimpleNamespace(count=0,weight=0,recent=9999))
        tags[t].count = tags[t].count + 1
        tags[t].weight = tags[t].weight + weight
        tags[t].recent = min(tags[t].recent,age.days)
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

def createTagList(names,data):
  tagList = []
  for t in names:
    tagList.append({
      'name':  t,
      'url':   "/tag/"+t.lower().replace(' ','-')+"/",
      'count': data[t].count })
  return tagList

def shuffleTags(tags):
  recent = []
  all = []

  for t in sorted(tags.keys(), key=lambda x: tags[x].weight, reverse=True):
    if len(recent) < RECENT_TAGS:
      recent.append(t)

  for t in sorted(tags.keys(), key=lambda x: tags[x].count, reverse=True):
    if not t in recent and (tags[t].count > MIN_TAG_COUNT or tags[t].recent < RECENT_PERIOD):
      all.append(t)

  return {
    'recent': createTagList(recent,tags),
    'other' : createTagList(all,tags)
  }

def writeTagData(args,tags):
  sbTags = shuffleTags(tags)

  with open(args.data+'tags.json','w') as output:
    output.write(json.dumps(sbTags))
    output.close()

  tagList = sorted(tags.keys(), key=lambda x: str(x).lower())
  with open(args.data+'tags.yaml','w') as output:
    output.write(yaml.safe_dump({ 'tags': tagList }))
    output.close()

  template(args.template+'tags.j2',sbTags,args.output+'tags-sidebar.html')

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
      elif entry.is_file() and entry.name.find('.') > 0:
        scanFile(os.path.join(path,entry.name),archive,tags)

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

CONFIG = common.findRootConfig(".",args.config)

if 'params' in CONFIG:
  if 'notags' in CONFIG['params']:
    BLOCK_TAGS = CONFIG['params']['notags']

archive = {}
tags = {}
scanPosts(args.path,archive,tags)

writeArchiveData(args,archive)
writeTagData(args,tags)

#for t in sorted(tags.keys(), key=lambda x: tags[x].weight, reverse=True):
#  print("%-20s %f %i" % (t,tags[t].weight,tags[t].count))