#! /bin/bash
for x
do
  filename=$(echo $x|sed -e "s/\.wiki$/.md/")
  sed -f ex "$x" > "$filename"
  echo "$filename"
done
