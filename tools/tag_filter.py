from __future__ import print_function
import re

def parse_tags(tags):
  or_list = []
  for t_and in tags.split(','):
    or_list.append(t_and.split('+'))
  return or_list

def match_tags(taglist,matchlist):
  if taglist is None:
    return False

  for t_and in matchlist:
    match = True
    for t in t_and:
      match = match and t in taglist
    if match:
      return True
  return False
