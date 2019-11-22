import os
from os import listdir
import re
from copy import deepcopy

def tryint(c):
    if c.isdigit():
        return int(c)
    return c

def human_sort_key(s):
    #Turn a string into a list of string and number chunks.
    #"z23a" -> ["z", 23, "a"]
    #reference:https://nedbatchelder.com/blog/200712/human_sorting.html

    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

docs_dir = os.path.dirname(os.path.abspath(__file__))
print(docs_dir)

hidden_files=['.pages', '.version', 'nav_generator.py', 'index.md']
hidden_dirs=['images', 'admin', 'arcus-c-client', 'arcus-java-client', 'arcus-server']

for cur, sub_dirs, files in os.walk(docs_dir):

    if cur == docs_dir:
        print("pass home")
        continue

    docs=sorted(deepcopy(files), key=human_sort_key)

    for doc in docs:
        if doc[len(doc)-2:len(doc)] != "md":
            hidden_files.append(doc)

    for hidden_file in hidden_files:
        if hidden_file in docs:
            docs.remove(hidden_file)

# latest verson come first
    version_dir = '.version' in files
    dirs=sorted(deepcopy(sub_dirs), reverse=version_dir)

    for hidden_dir in hidden_dirs:
        if hidden_dir in dirs:
            dirs.remove(hidden_dir)

    if not dirs and not docs:
        continue

    page_file = open(cur + '/.pages', mode='wt', encoding='utf-8')
    print(cur+'/.pages')
    page_file.write("arrange:\n")

    for dir in dirs: 
        page_file.write("    - " + dir + "\n")

    for doc in docs:
        page_file.write("    - " + doc + "\n")

    page_file.close()