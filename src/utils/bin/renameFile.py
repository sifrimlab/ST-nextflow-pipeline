import os
import sys
import shutil


file1 = sys.argv[1]
prefix = sys.argv[2]

shutil.copyfile(file1, f"{prefix}_{file1}")

