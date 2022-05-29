
import os, glob, shutil

in_dir = os.getcwd()

pattern = ['__pycache__']

for p in pattern:
    [shutil.rmtree(x) for x in glob.iglob(os.path.join(in_dir, "**", p), recursive=True)]