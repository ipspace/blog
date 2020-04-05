URL=$1
TITLE=$(wget -qO- $URL|hxnormalize -x|hxselect -c head title|sed -e 's/ &#171;.*//')
echo '*' "[$TITLE]($URL)"
