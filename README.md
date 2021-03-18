# communISS: In Situ Sequencing image processing end-to-end pipeline

### Installation

### File explanation
- *main.py*: Running the pipeline starts from here. See "Running the pipeline" for instructions how to run this from command line.
- *inputParsing.py*: Contains code used to parse input images and codebook as inputted by the user. 
- *decorators.py*: This file contains several decorators for the entire python pipeline. For end-users this will probably not be relevant, unless you want to perhaps add computation time to your pipeline usage.
- *test_space.py*: Contains testing code snippets, to be thrown away before shipment.
- ***image_processing/***: This directory contains all image processing specific python scripts.
	- *tiling.py*: Contains all helper functions for the tiling functionality. 
