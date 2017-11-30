#!/bin/bash

for png in `find build -name "*.png"`;
do
  echo "crushing \"$png\""
  pngcrush -brute -ow -q "$png"
done
