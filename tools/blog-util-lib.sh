#!/bin/bash
#
# OSX hugo utilities - library
#
blog_edit_post() {
  open -a "IA Writer" $1
# open -a "Sublime Text" $2
}

blog_start_hugo() {
  if [ -z "`pgrep hugo`" ]; then
    (cd $BLOG_HOME && hugo server -F -D $@) &
    sleep $HUGO_START
  else
    if [ -n "$HUGO_CHANGE" ]; then
      sleep $HUGO_CHANGE
    fi
  fi
}

blog_new_file() {
  if [ -f $1 ]; then
    echo $1 already exists...
    return
  fi
  FILE=$1
  TITLE=X
  DATE="date: `date +"%Y-%m-%d %H:%M:00"`"
  DRAFT=
  TEXT=
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
tags:
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

blog_md_to_html() {
  echo $1|sed 's#[.]md$#.html#'
}

get_filepath() {
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

