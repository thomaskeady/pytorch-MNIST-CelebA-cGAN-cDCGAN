#!/bin/bash

cd cedict_dir

for filename in *.png;
do
    #./MyProgram.exe "$filename" "Logs/$(basename "$filename" .txt)_Log$i.txt"
    IFS='.' read -ra NAME <<< "$filename"

    #echo ${NAME[0]}
    #echo ${NAME[1]}

    mkdir ${NAME[0]}
    cp $filename ${NAME[0]}/$filename
    echo Did $filename

done
