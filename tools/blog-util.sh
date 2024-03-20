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
  blog search - search for blog posts matching a regex within files matching a second regex
                (example: blog search 'API|CLI' '201[5-9]')

  blog fix    - fix a blog post
  blog new    - new blog post
  blog kb     - KB article management
  blog migrate- migrate an old HTML blog post into Markdown
  blog sertag - applies series tag to a Markdown blog post
  blog draft  - new draft
  blog ls     - list blog posts

  blog tag    - list tags
  blog series - series management
  blog title  - get a title of a published blog post. Use URL to print title on STDOUT,
                'clip' for clipboard-to-clipboard operation, or 'md' for Markdown
                clipboard-to-clipboard operation.

  blog diff   - start 'git diff --word-diff'
  blog commit - add content to commit staging area, commit with message

  blog server - go to blog directory, start hugo, open link in browser
  blog kill   - kill the hugo server
DOC
}

blog_argument() {
  if [ $# -lt 2 ]; then
    echo "Missing argument to blog $1"
    exit 1
  fi
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
    shift
    for name in "$@"; do
      name=$(blog_skip_url $name)
      name=$(blog_find_file $name)
      blog_edit_post $name
      blog_view_post $name
    done
    ;;
  migrate)
    set -e
    blog_argument "$@"
    INFILE=$(blog_skip_url $2)
    if [ -f "$INFILE" ]; then
      MDFILE=$(blog_html_to_md $INFILE)
      echo "Migrating $INFILE to $MDFILE"
      $SCRIPT_DIR/migrate-post.py $INFILE
      blog_edit_post $MDFILE
      blog_view_post $MDFILE
      open "https://blog.ipspace.net/$INFILE"
    else
      echo "Failed: cannot find $INFILE"
    fi
    ;;
  sertag)
    HUGO_CHANGE=
    if [ -z "BLOG_SERIES" ]; then
      if [ -z "BLOG_CATEGORY" ]; then
        echo "Set BLOG_SERIES or BLOG_CATEGORY environment variable first"
        exit 1
      fi
    fi
    if [ -z "BLOG_SERIES_TAG" ]; then
      echo "Set BLOG_SERIES_TAG environment variable first"
      exit 1
    fi
    shift
    SERTAG_EDIT=True
    if [ "$1" == "--noedit" ]; then
      SERTAG_EDIT=
      shift
    fi
    if [[ "$BLOG_SERTAG_CLI" ]]; then
      SERTAG_EDIT=
    fi
    set -e
    for name in "$@"; do
      echo "Applying ${BLOG_SERIES:-$BLOG_CATEGORY} tag $BLOG_SERIES_TAG to $name"
      name=$(blog_skip_url $name)
      name=$(blog_find_file $name)
      echo "... final file name $name"
      if [[ "$name" == *".html" ]]; then
        open "https://blog.ipspace.net/$name"
        MDFILE=$(blog_html_to_md $name)
        echo "Migrating $name to $MDFILE"
        $SCRIPT_DIR/migrate-post.py $name
        SERTAG_EDIT=True
        name="$MDFILE"
      else
        $SCRIPT_DIR/series-tag-post.py $name
      fi
      if [[ $SERTAG_EDIT ]]; then
        blog_edit_post $name
        blog_view_post $name
      fi
    done
    ;;
  open)
    HUGO_CHANGE=
    shift
    for name in "$@"; do
      name=$(blog_skip_url $name)
      name=$(blog_find_file $name)
      blog_view_post $name
    done
    ;;
  diff)
    git diff --patience --word-diff=color --word-diff-regex='[^ "'']+'
    ;;
  ls)
    shift
    case "$1" in
      ideas*)
        shift
        $BLOG_HOME/tools/list-ideas.py $@
        ;;
      draft*)
        (cd $BLOG_HOME && hugo list drafts)
        ;;
      future*)
        (cd $BLOG_HOME && hugo list future)
        ;;
      series*)
        shift
        $BLOG_HOME/tools/list-posts.py --series $@
        ;;
      tag*)
        shift
        $BLOG_HOME/tools/list-posts.py --tags $@
        ;;
      "")
        $BLOG_HOME/tools/list-posts.py $(date +"%Y/%m") $(date -v+1m +"%Y/%m")
        ;;
      *)
        $BLOG_HOME/tools/list-posts.py "$@"
    esac
    ;;
  new)
    blog_argument "$@"
    BLOG_FILE="`blog_get_md_file $2`"
    blog_new_file "$BLOG_FILE"
    blog_edit_post "$BLOG_FILE"
    blog_start_hugo
    open "http://localhost:1313/`blog_md_to_html $BLOG_FILE`"
    ;;
  kb)
    shift
    $BLOG_HOME/tools/kb-actions.py $@
    ;;
  search)
    if [ -z "$3" ]; then
      echo 'Usage: blog search <regex> <files>'
    fi
    ack -l "$2"|ack "$3"|sort|xargs -n 1 -I % $SCRIPT_DIR/blog-open-published.sh %
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
  title)
    URL=$(pbpaste)
    FIXURL=$(echo $URL|sed -e 's#http://localhost:1313##')
    case "${2:-link}" in
      clip)
        $SCRIPT_DIR/url-to-title.sh $URL|pbcopy
        ;;
      link)
        TITLE=$($SCRIPT_DIR/url-to-title.sh $URL)
        echo -n "[$TITLE]($FIXURL)"|pbcopy
        ;;
      md)
        TITLE=$($SCRIPT_DIR/url-to-title.sh $URL)
        echo '*' "[$TITLE]($FIXURL)"|pbcopy
        ;;
      em)
        TITLE=$($SCRIPT_DIR/url-to-title.sh $URL)
        echo "_[$TITLE]($FIXURL)_"|pbcopy
        ;;
      wiki)
        TITLE=$($SCRIPT_DIR/url-to-title.sh $URL)
        echo '*' "[$FIXURL $TITLE]"|pbcopy
        ;;
      yaml)
        TITLE=$($SCRIPT_DIR/url-to-title.sh $URL)
        cat <<YAML|pbcopy
  - link: $URL
    title: "$TITLE"
YAML
        ;;
      http*)
        $SCRIPT_DIR/url-to-title.sh $2|pbcopy
        ;;
      *)
        echo "Usage: blog title url|clip|md|em|wiki|yaml"
        ;;
    esac
    ;;
  series)
    case "$2" in
      new)
        if [ -z "$3" ]; then
          echo "Need series tag"
          exit
        fi
        BLOG_SERIES="$BLOG_HOME/content/series"
        mkdir -p "$BLOG_SERIES/$3"
        touch "$BLOG_SERIES/$3/_index.md"
        blog_edit_post "$BLOG_SERIES//$3/_index.md"
        ;;
      *)
        echo "Usage blog series new <tag>"
    esac
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
    $BLOG_HOME/tools/blog-worth-reading.sh "$2"
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
