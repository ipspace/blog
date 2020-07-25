#!/bin/bash
if [ -z "$1" ]; then
  echo "Need URL parameter" >&2
  exit
fi
URL=$1
open https://blog.ipspace.net/$(echo $URL|perl -pe 's/\.md/.html/')