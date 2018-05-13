#!/usr/bin/env bash

inputData="cedict_processed.txt"
outputDir="cedict_dir"

mkdir $outputDir

while IFS= read -r LINE
do
  #CODE=$(echo $LINE | cut -f1) # fails to split
  #CHAR=$(echo $LINE | cut -f2)

  # Premature optimization is the root of all evil
  CHAR="$(echo "$LINE"| awk '{print $1}')"
  CODE="$(echo "$LINE"| awk '{print $2}')"

  #echo $CODE
  echo $CHAR

  ((NUM=0))

  # If file already exists
  while [ -f $outputDir/$CODE/$CODE$NUM.png ]; do
    ((NUM+=1))
  done

  mkdir $outputDir/$CODE/

  # Need to install ImageMagick to use this
  # -pointsize flag is font size
  # -resize flag gives output size, height is larger because aspect ratio is 1.4
  # -crop then turns it back into a square image with the character centered
  # We might want to give more padding around the character in the image
  #convert -pointsize 29 -resize 64x90\! -crop 64x64+0+13 -font /System/Library/Fonts/PingFang.ttc label:$CHAR $outputDir/$CODE.png
  convert -pointsize 29 -resize 64x90\! -crop 64x64+0+13 -negate -font /System/Library/Fonts/PingFang.ttc label:$CHAR $outputDir/$CODE/$CODE$NUM.png

done < "$inputData"

echo Done
tput bel
