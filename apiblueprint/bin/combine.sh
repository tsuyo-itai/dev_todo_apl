#!/bin/bash

output_file_name="ToDoAplAPI"

cd `dirname $0`

files_list=()
files_list+=(../src/AuthCreate.apib)
files_list+=(../src/Auth.apib)
files_list+=(../src/ToDoGet.apib)
files_list+=(../src/ToDoCreate.apib)
files_list+=(../src/ToDoDelete.apib)
files_list+=(../src/ToDoUpdate.apib)
files_list+=(../src/ToDoSearch.apib)

for file in ${files_list[@]}
do
    files+=(${file})
    aglio -i ${file} -o ../output/$(basename ${file} .apib).html
done
echo 'FORMAT: 1A' > ../${output_file_name}.md || exit $?
cat ${files[@]} | sed -e '/^FORMAT: 1A/d' >> ../${output_file_name}.md || exit $?
mkdir -p ../output 2>/dev/null
aglio -i ../${output_file_name}.md -o ../output/${output_file_name}.html || exit $?

exit 0
