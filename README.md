# communISS: In Situ Sequencing image processing end-to-end pipeline
@licence: Property of LMIB
@authors: David Wouters
@maintainer: David Wouters
@e-mail: david.wouters1@student.kuleuven.be

### Installation

### File explanation
- *main.py*: Running the pipeline starts from here. See "Running the pipeline" for instructions how to run this from command line.
- *decorators.py*: This file contains several decorators for the entire python pipeline. For end-users this will probably not be relevant, unless you want to perhaps add computation time to your pipeline usage.
- ***image_processing_env***: This directory contains all image processing specific python scripts.
	- *tiling.py*: Contains all helper functions for the tiling functionality. 
