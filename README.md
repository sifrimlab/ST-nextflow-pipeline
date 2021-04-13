# communISS: Spatial Transcriptomics processing end-to-end pipeline

### What you need to have installed:
- Nextflow: https://www.nextflow.io/docs/latest/getstarted.html
- (Ana)Conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html

### Running the pipeline
- Update your version of the repo to the most recent stable version:
- 	```bash
	nextflow clone WoutDavid/communISS ; cd communISS
	```
- Create a personal config file containing all the parameters you'll need for the functionality you want:
- ```bash
	nextflow config -profile conda,iss >> standard_iss_experiment.config
	```
- *Note that this config file is where you change everything that you want to change, such as data directory, output directory, image format etc.*
- After making the needed changes to the config file, you can run pipeline by specifying an entry point with "-entry", which takes as argument the name of one of the workflows included in the main.nf file.  
- ```bash
  nextflow -C standard_iss_experiment.config run  main.nf	\
						-entry iss							\
						--with_conda comunISS.yaml			\
	```


### Repository file hierarchy explanation
- *main.nf*: Running the pipeline should always start from here. Dynamically defined paths in the functionality count on the starting point of the "nextflow run"-command being the main.nf file.
- *decorators.py*: This file contains several decorators for the entire python pipeline. For end-users this will probably not be relevant, unless you want to perhaps add computation time to your pipeline usage.
