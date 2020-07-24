#!/bin/bash
#
# OSX hugo utilities
#
blog_usage() {
  cat <<DOC
Usage:

  blog home   - go to blog directory
  blog posts  - go to blog posts directory

  blog open   - open a local blog post
  blog fix    - fix a blog post
  blog new    - new blog post
  blog draft  - new draft
  blog ls     - list blog posts
  blog tag    - list tags

  blog diff   - start 'git diff --word-diff'
  blog commit - add content to commit staging area, commit with message

  blog server - go to blog directory, start hugo, open link in browser
  blog kill   - kill the hugo server
DOC
}

SCRIPT_DIR=$( dirname "${BASH_SOURCE[0]}" )
. "$SCRIPT_DIR/blog-util-lib.sh"

if [ -z "$BLOG_HOME" ]; then
  echo "BLOG_HOME environment variable not set, aborting..."
  exit
fi

case "$1" in
  fix)
    HUGO_CHANGE=
    blog_edit_post $2
    blog_view_post $2
    ;;
  open)
    HUGO_CHANGE=
    blog_view_post $2
    ;;
  diff)
    git diff --patience --word-diff=color --word-diff-regex='[^ "'']+'
    ;;
  ls)
    shift
    case "$1" in
      draft*)
        (cd $BLOG_HOME && hugo list drafts)
        ;;
      future*)
        (cd $BLOG_HOME && hugo list future)
        ;;
      "")
	$BLOG_HOME/tools/list-posts.py $(date +"%Y/%m") $(date -v+1m +"%Y/%m")
        ;;
      *)
        $BLOG_HOME/tools/list-posts.py "$@"
    esac
    ;;
  new)
    BLOG_FILE="`blog_get_md_file $2`"
    blog_new_file "$BLOG_FILE"
    blog_edit_post "$BLOG_FILE"
    blog_start_hugo
    open "http://localhost:1313/`blog_md_to_html $BLOG_FILE`"
    ;;
  draft)
    if [ -z "$2" ]; then
      echo "Need the filename of the draft post"
    else
      BLOG_FILE="$(blog_get_md_file $BLOG_HOME/content/draft/$(basename $2))"
      blog_new_file "$BLOG_FILE" draft
      blog_edit_post "$BLOG_FILE"
      blog_start_hugo
      open "http://localhost:1313/draft/$(blog_md_to_html $(basename $BLOG_FILE))"
    fi
    ;;
  kill)
    ps -ef|grep hugo
    pkill $1 hugo
    ;;
  server)
    cd $BLOG_HOME
    if [ -n "`pgrep hugo`" ]; then
      echo "Killing old Hugo instance"
      pkill hugo
      sleep 1
    fi
    HUGO_THEME=
    if [ "$2" == "minimal" ]; then
      HUGO_THEME="--theme minimal,ipspace"
    fi
    blog_start_hugo $HUGO_THEME
    open http://localhost:1313
    ;;
  worth)
    $BLOG_HOME/tools/blog-worth-reading.sh
    ;;
  commit)
    pushd $BLOG_HOME >/dev/null
    git add static content
    if [ -n "$2" ]; then
      git commit -m "$2"
    else
      git commit
    fi
    git push
    popd >/dev/null
    ;;
  tag*)
    pushd $BLOG_HOME >/dev/null
    ack -i "$2" data/tags.yaml|tee /dev/tty|sed 's/\- //'|pbcopy
    popd >/dev/null
    ;;
  *)
    blog_usage
    ;;
esac
