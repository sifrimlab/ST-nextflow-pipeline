# communISS: In Situ Sequencing image processing end-to-end pipeline

### What you need to have installed:
- Nextflow: https://www.nextflow.io/docs/latest/getstarted.html
- (Ana)Conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html

### Running the pipeline
- ***Run***: nextflow clone WoutDavid/communISS ; cd communISS
- edit the nextflow.config file with specifications of your project (path to data, n_rounds etc...)
- ***Run***: nextflow run dsl2_nextflow_pipeline.nf -with-conda communISS.yaml


### File explanation
- *main.py*: Running the pipeline starts from here. See "Running the pipeline" for instructions how to run this from command line.
- *decorators.py*: This file contains several decorators for the entire python pipeline. For end-users this will probably not be relevant, unless you want to perhaps add computation time to your pipeline usage.
- *test_space.py*: Contains testing code snippets, to be thrown away before shipment.
- ***image_processing/***: This directory contains all image processing specific python scripts.
	- *tiling.py*: Tiles images into an even number of tiles.
	- *rigidRegister.py*: Registers images with respect to a reference image.
	- *filtering.py*: Filters and image using the white tophat algorithm.
	- *maxIP.py*: Creates a maximum intensity projection of an image stack.
