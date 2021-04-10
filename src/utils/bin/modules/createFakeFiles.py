import os 
import touch
for i in range(1,6):
    newDir = os.path.join(os.getcwd(), f"Round{i}")
    os.mkdir(newDir)
    for j in range(1,6):
            touch.touch(os.path.join(newDir, f"c{j}.tif"))	
