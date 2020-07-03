#!/bin/bash
#
# Create Worth Reading blog post
#
if [ -z "$BLOG_HOME" ]; then
  echo "BLOG_HOME environment variable not set, aborting..."
  exit
fi

SCRIPT_DIR=$( dirname "${BASH_SOURCE[0]}" )
. "$SCRIPT_DIR/blog-util-lib.sh"

cat <<TEXT
Generate "Worth Reading" blog posts. Starting within the content directory.

TEXT
cd $BLOG_HOME/content/posts
read -e -p "URL: " URL
TITLE=$(wget -qO- "$URL"|\
  hxnormalize -x|\
  hxselect -c head title|\
  sed -e 's/ &#171;.*//')

if [ -z "$TITLE" ]; then
  echo "Could not get page title, aborting"
  exit
fi

echo ""
echo "Got page title: $TITLE"
echo ""

until [ -d "$DIR" ]; do
  read -e -p "Directory: " DIR
  if [ ! -d "$DIR" ]; then
    echo "... not found"
  fi
done
read -e -p "Filename: " FNAME
FNAME="worth-reading-$FILE.md"
if [ -e "$DIR/$FNAME" ]; then
  echo "File already exists, fixing..."
else
  blog_new_file "$DIR/$FNAME" title "Worth Reading: $TITLE" text "[$TITLE]($URL)"
fi
blog_edit_post "$DIR/$FNAME"
open "$URL"
