from __future__ import print_function
import sys
import os
import yaml
import re
from datetime import date, datetime, timezone
import dateutil.parser
import dateutil.tz

YAML_DELIMITER="---\n"

def findRootConfig(dir='.',config='config.yaml'):
  while True:
    try:
      cfile = open(config)
    except:
      print("Cannot file config file in %s, retrying..." % os.getcwd())
      os.chdir("../")
      continue

    cdata = yaml.safe_load(cfile)
    cfile.close()
    return cdata

def read_blog_post(path):
  with open(path, 'r') as stream:
    content = re.split(YAML_DELIMITER,stream.read())
    if len(content) < 2:
      return (None,None)
    frontmatter = content[1]
    text = YAML_DELIMITER.join(content[2:])
    stream.close()

  try:
    doc = yaml.safe_load(frontmatter)
  except yaml.YAMLError as exc:
    raise Exception("Error parsing YAML header in %s: %s" % (path,exc))

  # Parsing the publication date is weird
  #
  # * YAML might already have generated the datetime timestamp, so we have to go to string first
  # * We have to use dateutil.parser so we can parse 'meaningful' and ISO timestamps
  # * The result might or might not have a timezone, so we have to adjust that as well
  #
  date = doc.get('date')
  if date:
    try:
      pubdate = dateutil.parser.parse(str(date))
    except:
      raise Exception("Date %s parsing error %s in %s" % (date,sys.exc_info()[0],path))

    if pubdate.tzinfo is None:
      pubdate = pubdate.replace(tzinfo=timezone.utc)
    doc['date'] = pubdate

  return(doc,text)

def set_series_tag(post,series=None,s_tag=None):
  if not series:
    series = os.environ.get('BLOG_SERIES') or os.environ.get('BLOG_CATEGORY')

  if not series:
    print("Cannot tag a post without series/category value")
    return

  modified = False

  if series and not series in post.get('tags',[]):
    c_value = post.get('series',None)
    if c_value and isinstance(c_value,str):
      post['series'] = [ c_value ]
      modified = True
    elif c_value is None:
      post['series'] = []

    if not series in post['series']:
      post['series'].append(series)
      modified = True

  if not s_tag:
    s_tag = os.environ.get('BLOG_SERIES_TAG')
  if s_tag and series:
    series = series.lower().replace(' ','-')
    post[series+"_tag"] = s_tag
    modified = True
    if os.environ.get('BLOG_SERIES_WEIGHT'):
      if not post.get("series_weight"):
        post["series_weight"] = int(os.environ.get('BLOG_SERIES_WEIGHT'))

  if modified and not 'series_title' in post and ': ' in post.get('title',''):
    post['series_title'] = post.get('title').split(': ')[-1]
