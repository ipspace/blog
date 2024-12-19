#!/usr/bin/env python3
#
import fileinput

maxlen = 0
count = 0
for line in fileinput.input():
  line = line.strip()
  if "\t" in line or maxlen:
    elem = line.split("\t")
    while len(elem) < maxlen:
      elem.append("")
    if len(elem) > maxlen:
      maxlen = len(elem)

    line = ' | '.join(elem)
    line = '| ' + line + ' |'

    count = count + 1
    if count == 2:
      print("|"," | ".join(["---"] * maxlen),"|")

  print(line)
