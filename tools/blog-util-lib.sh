#!/bin/bash
#
# OSX hugo utilities - library
#

# Change the delays based on the speed of your platform
#
HUGO_START=10
HUGO_CHANGE=3

blog_edit_post() {
  open -a "IA Writer" $1
# open -a "Sublime Text" $2
}

blog_start_hugo() {
  if [ -z "`pgrep hugo`" ]; then
    echo "Starting Hugo (output redirected to /dev/null)"
    POLL=""
    (cd $BLOG_HOME && hugo server -F -D $POLL $@ >/dev/null) &
    echo "... waiting $HUGO_START seconds for Hugo to start"
    sleep $HUGO_START
  else
    if [ -n "$HUGO_CHANGE" ]; then
      sleep $HUGO_CHANGE
    fi
  fi
}

blog_view_post() {
  blog_start_hugo
  BLOG_POST=$(get_filepath $1|sed 's#.*/posts##'|sed 's#md$#html#'|sed 's#.html#/#')
  open "http://localhost:1313$BLOG_POST"
}

blog_new_file() {
  if [ -f $1 ]; then
    echo $1 already exists...
    return
  fi
  FILE=$1
  TITLE=X
  DATE="date: `date +"%Y-%m-%d %H:%M:00%z"`"
  DRAFT=
  TEXT=
  TAGS=
  shift
  while [ $1 ]; do
    case "$1" in
      draft)
        DRAFT='draft: True'
        DATE="# $DATE"
        ;;
      title)
        TITLE=$2
        shift
        ;;
      tags)
        TAGS=$2
        shift
        ;;
      text)
        TEXT=$2
        shift
        ;;
    esac
    shift
  done

  cat >$FILE <<TEXT
---
title: "$TITLE"
$DATE
tags: [ $TAGS ]
TEXT
  if [ "$DRAFT" ]; then
    echo "$DRAFT" >>$FILE
  fi
  echo "---" >>$FILE
  if [ "$TEXT" ]; then
    echo "$TEXT" >>$FILE
  fi
}

blog_get_md_file() {
  echo "`echo $1|sed 's#[.]md$##'`.md"
}

blog_skip_url() {
  echo $1|sed 's#https://blog[.]ipspace[.]net/##'|sed 's#http://localhost:1313/##'
}

blog_md_to_html() {
  echo $1|sed 's#[.]md$#.html#'
}

blog_html_to_md() {
  echo $1|sed 's#[.]html$#.md#'
}

blog_find_file() {
  fname="$(echo $1|sed 's#/$#.html#')"
  if [ -f "$fname" ]; then
    echo $fname
  else
    blog_html_to_md $fname
  fi
}

blog_open_published() {
  echo $1
#  open https://blog.ipspace.net/$(echo %|perl -pe 's/\.md/.html/')
}

get_filepath() {
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

