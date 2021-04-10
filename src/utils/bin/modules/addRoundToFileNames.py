import os
import sys
import glob
import pathlib

dataDir = os.getcwd()
roundDirName = "Round*"

round_dirs = glob.glob(os.path.join(dataDir, roundDirName))
for round_dir in round_dirs:
        dir_name = pathlib.PurePath(round_dir).name
        for file in os.listdir(round_dir):
                previous_name = os.path.join(round_dir, file)
                new_name = os.path.join(round_dir, f"{dir_name}_{file}")
                os.rename(previous_name, new_name)

