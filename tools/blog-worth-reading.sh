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
if [ -z "$1" ]; then
  read -e -p "URL: " URL
else
  URL="$1"
  echo "URL set to $URL"
fi
TITLE=$(wget -qO- "$URL"|\
  hxnormalize -x|\
  hxselect -c head title|\
  sed -e 's/ &#171;.*//')

if [ -z "$TITLE" ]; then
  echo "Warning: Could not get page title"
  TITLE="WTF"
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
FNAME="worth-reading-$FNAME.md"
if [ -e "$DIR/$FNAME" ]; then
  echo "File already exists, fixing..."
else
  blog_new_file "$DIR/$FNAME" title "Worth Reading: $TITLE" text "[$TITLE]($URL)" tags "worth reading"
fi
blog_edit_post "$DIR/$FNAME"
blog_view_post "$DIR/$FNAME" &
(sleep 1; open "$URL") &
