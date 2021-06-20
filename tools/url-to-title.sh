#!/bin/bash
if [ -z "$1" ]; then
  echo "Need URL parameter" >&2
  exit
fi
URL=$1
echo $(wget -qO- $URL|hxnormalize -x|hxselect -c head title|perl -0777 -pe 's/(\s+&#171;.*| - www.ipSpace.net)$//igs')
