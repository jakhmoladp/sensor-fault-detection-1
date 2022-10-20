import os

with open("requirements.txt", 'r') as f:
    lst = f.read().splitlines()

lst = [lib for lib in lst if not (lib.strip() == '' or lib.strip() == '-e .')]

print(lst)

