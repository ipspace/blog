#!/usr/local/bin/python3

from __future__ import print_function
import sys
import os
import re
import io
import xml.etree.ElementTree as ET
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup,Comment
import yaml
from datetime import date, datetime, timezone
import dateutil.parser
import argparse

POST_PATH="content/posts/"
IMAGE_PATH="static/"
COMMENT_PATH="comments/"

IMAGE_SERVER="bp.blogspot.com"
IMAGE_URL="/"
URL_LIMIT=""
LOGGING=""
LOGFILE=""

def getElementText(parent,tag):
  elem = parent.find(tag)
  if elem is not None:
    return elem.text
  return None

def getElementAttr(parent,tag,attr):
  elem = parent.find(tag)
  if elem is not None:
    return elem.attrib[attr]
  return None

def printElementText(parent,key,tag,**options):
  elem = parent.find(tag)
  if elem is not None:
    if elem.text is not None:
      txt = elem.text.strip()
      if options.get('multiline'):
        print(u'%s: |\n  %s' % (key,txt))
      else:
        print(u'%s: "%s"' % (key,txt.replace('"','\\"')))

def printCategories(entry,key,tag):
  cnt = 0
  for elem in entry.findall(tag):
    term = elem.attrib['term']
    if term and term.find("#") < 0:
      if (not cnt):
        print(u"%s: [ %s" % (key,term),end="")
      else:
        print(u",%s" % term,end="")
      cnt = cnt + 1
  if cnt:
    print(" ]")

def multiline(text):
  for tag in ('p','li','ul','ol','div','blockquote'):
    text= re.sub("</"+tag+"><","</"+tag+">\n<",text)
  return text

def fetchAndSaveImage(obj,attr,path):
  href = obj.get(attr)

  prefix = ""
  imgres = re.search("/s(\d+)/",href)
  if imgres:
    w = imgres.group(1)
    if w:
      prefix = "s"+w+"-"

  imgname = os.path.dirname(path) + "/" + prefix + urllib.parse.unquote(os.path.basename(href))
  imgpath = IMAGE_PATH+imgname
  with urllib.request.urlopen(href) as url:
    if url.status == 200:
      dir = os.path.dirname(imgpath)
      if not os.path.exists(dir):
        os.makedirs(dir)
      with open(imgpath,"wb") as f:
        f.write(url.read())
        f.close()
      obj[attr] = IMAGE_URL+imgname
      if LOGGING:
        LOGFILE.write("Fetched image: "+imgpath+"\n")
        LOGFILE.flush
      return 1
    else:
      sys.stderr.write("Error fetching "+href+": "+str(url.status)+" "+url.reason+"\n")
      sys.stderr.flush
      return 0

def fetchImages(tree,path):
  cnt = 0
  for img in tree("img"):
    href = img.get('src')
    if href.find(IMAGE_SERVER) >= 0:
      cnt = cnt + fetchAndSaveImage(img,'src',path)

  for a in tree("a"):
    href = a.get('href')
    if href and href.find(IMAGE_SERVER) >= 0:
      cnt = cnt + fetchAndSaveImage(a,'href',path)

  return cnt

def fixScriptHide(tree,path):
  cnt = 0
  for s in tree("script"):
    jscode = s.string
    if jscode and jscode.find('startHide') >= 0:
      if LOGGING:
        LOGFILE.write('... found old startHide')
        LOGFILE.flush()
      s.replace_with(Comment("more"))
      cnt = cnt + 1
    if jscode and jscode.find('endHide') >= 0:
      if LOGGING:
        LOGFILE.write('... found old endHide')
        LOGFILE.flush()
      s.extract()
      cnt = cnt + 1
  return cnt

def printHTMLContent(entry,tag,**options):
  elem = entry.find(tag)
  text = elem.text

  path = options.get('path')
  text = text.replace("<a name='more'></a>","<!--more-->")
  tree = BeautifulSoup(text,features='html.parser')
  imgcnt = fetchImages(tree,path)
  morefix = fixScriptHide(tree,path)

  for tag in ('p','li','ul','ol','div','blockquote'):
    for e in tree(tag):
      e.insert_after("\n")

  tree.smooth()
  html = str(tree)+"\n"
  html = re.sub("\n(\s+|\n+)*","\n",html)
  print(html,end='')
  return False

def findLink(entry,tag,rel,type):
  for link in entry.findall(tag):
    if link.attrib['rel'] == rel and (link.attrib['type'] == type or type is None):
      return link.attrib['href']

def dumpEntryElements(entry):
  for elem in entry:
    print(elem.tag)
    print(elem.attrib)
    print("  ",elem.text)

def getURLPath(url):
  m = re.search("//[a-zA-Z.]+/(.*)\\Z",url)
  if m is not None:
    return m.group(1)
  raise Exception("Cannot find URL path in %s" % url)

def createOutputFile(url):
  urlPath = getURLPath(url)
  path = POST_PATH + urlPath

  dir = os.path.dirname(path)
  if not os.path.exists(dir):
    os.makedirs(dir)
  print("Writing:",path)
  sys.stdout = io.open(path,mode="w")
  return urlPath

def getEntryType(entry):
  for elem in entry.findall("{http://www.w3.org/2005/Atom}category"):
    if elem.attrib["scheme"] == "http://schemas.google.com/g/2005#kind":
      term = elem.attrib["term"]
      term = term.replace('http://schemas.google.com/blogger/2008/kind#',"")
      return term

def extractPostId(id):
  match = re.search(r"post-(\d+)$",id)
  if match:
    return match.group(1)
  return id

def findId(entry):
  id = getElementText(entry,"{http://www.w3.org/2005/Atom}id")
  if not id:
    raise Exception("Cannot find entry ID")
  return extractPostId(id)

idLookup = {}

def dumpPost(entry):
  stdout = sys.stdout
  url = findLink(entry,"{http://www.w3.org/2005/Atom}link","alternate","text/html")
  if not(url):
    url = findLink(entry,"{http://www.w3.org/2005/Atom}link","replies","text/html")
    url = url.split("#")[0]
    LOGFILE.write("Blog post without primary URL link, found %s\n" % url)

  id = findId(entry)
  idLookup[id] = {
    'type': 'post',
    'id':   id,
    'url':  getURLPath(url),
    'count':0
  }

  if URL_LIMIT and url.find(URL_LIMIT) < 0:
    return 0

  filepath = createOutputFile(url)
  if filepath:
    print("---")
    # print(u"url: %s" % url)
    print("url: /%s" % filepath)
    printElementText(entry,u"title","{http://www.w3.org/2005/Atom}title")
    printElementText(entry,u"date","{http://www.w3.org/2005/Atom}published")
    printCategories(entry,u"tags","{http://www.w3.org/2005/Atom}category")

    media = findLink(entry,"{http://www.w3.org/2005/Atom}link","enclosure",None)
    if media:
      print(u"media: %s" % media)

    print("---")
    print()
    done = printHTMLContent(entry,"{http://www.w3.org/2005/Atom}content",path=filepath)
    print()
    sys.stdout.close()
    sys.stdout = stdout
    if done:
      sys.exit()
    return 1
  else:
    sys.stderr.write("Cannot find file path in "+url)

def parseComment(entry):
  pubstr  = getElementText(entry,"{http://www.w3.org/2005/Atom}published")
  pubdate = dateutil.parser.parse(pubstr)
  content = getElementText(entry,"{http://www.w3.org/2005/Atom}content")
  id =      findId(entry)
  ref =     extractPostId(getElementAttr(entry,"{http://purl.org/syndication/thread/1.0}in-reply-to","ref"))
  related = findLink(entry,"{http://www.w3.org/2005/Atom}link","related","application/atom+xml")
  author  = entry.find("{http://www.w3.org/2005/Atom}author")

  if not id:
    raise Exception("No ID in comment")
  if not ref:
    raise Exception("No Ref in comment ID %s" % id)
  if not content:
    raise Exception("No content in comment ID %s" % id)
  if not pubdate:
    raise Exception("No pubdate in comment ID %s" % id)
  if not author:
    raise Exception("No author in comment ID %s" % id)

  if related:
    related = related.split('/')[-1]
  image = getElementAttr(author,"{http://schemas.google.com/g/2005}image","src")
  if image and not 'http' in image:
    image = 'https:' + image

  comment = {
    'type':   'comment',
    'id':     id,
    'pub':    pubstr,
    'date':   pubdate.strftime('%d %B %Y %H:%M'),
    'html':   content,
    'name':   getElementText(author,"{http://www.w3.org/2005/Atom}name"),
    'profile':getElementText(author,"{http://www.w3.org/2005/Atom}uri"),
    'image':  image
  }
  idLookup[id] = comment

  parent = idLookup.get(related) if related else idLookup.get(ref)

  if parent:
    comment['ref'] = parent['id']
    parent.setdefault('comments',[])
    parent['comments'].append(comment)

    while parent['type'] == 'comment':
      parent = idLookup[parent['ref']]
    parent['count'] = parent['count']+1
    return 1
  else:
    return 0

def dumpBlog(root):
  cnt = 0
  comments = 0
  for entry in root:
    if entry.tag == "{http://www.w3.org/2005/Atom}entry":

      id = entry.find("{http://www.w3.org/2005/Atom}id")
      if id is not None:
        id_text = id.text
        if (id_text.find(".post") > 0):
          entryType = getEntryType(entry)
          if entryType == "post":
            cnt = cnt + dumpPost(entry)
          elif entryType == "comment":
            comments = comments + parseComment(entry)
          else:
            print("Unknown entry type: %s" % entryType)

  print("Total: ",cnt,"blog posts and ",comments,"comments")

def dumpComments(data):
  cnt = 0
  for item in data.values():
    if item.get('type') != 'post':
      continue
    if not 'comments' in item:
      continue

    url = item.get('url')
    if not url:
      continue

    path = COMMENT_PATH + url.replace('.html','.yaml')
    if LOGGING:
      LOGFILE.write('Writing comments %s\n' % path)
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
      os.makedirs(dir)

    with open(path,"w") as output:
      output.write(yaml.dump(item))
      output.close

#
# Main code
#
def parseCLI():
  parser = argparse.ArgumentParser(description='Import Blogger XML dump')
  parser.add_argument('input', action='store', help='Input file')
  parser.add_argument('--limit',dest='limit', action='store', help='Limit post URL')
  parser.add_argument('--comments', dest='comments', action='store_true',help='Import comments')
  parser.add_argument('--log', dest='logging', action='store_true',
                  help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',
                  help='Enable more verbose logging')
  return parser.parse_args()


args = parseCLI()

LOGFILE=sys.stdout
LOGGING=args.logging
URL_LIMIT=args.limit

print("Reading from ",args.input)

xml = ET.parse(args.input)
root = xml.getroot()

dumpBlog(root)
if args.comments:
  dumpComments(idLookup)
