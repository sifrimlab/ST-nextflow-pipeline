# communISS: Spatial Transcriptomics processing end-to-end pipeline

This repository represents the code-base behind the author's dissertation of his master in bioinformatics of 2021.
It contains an entire end-to-end image processing and analysis pipeline for Spatial Transcriptomics. 
Currently it supports both ISS data and MERFISH data.

### What you need to have installed:
- Nextflow: https://www.nextflow.io/docs/latest/getstarted.html
- (Ana)Conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html

### Running the pipeline
- Update your version of the repo to the most recent stable version:
- 	```bash
	nextflow pull WoutDavid/communISS ; cd communISS
	```
- Create a personal config file containing all the parameters you'll need for the functionality you want:
- ```bash
	nextflow config -profile conda,iss >> standard_iss_experiment.config
	```
- *Note that this config file is where you change everything that you want to change, such as data directory, output directory, image format etc.*
For an explanation on all possible parameters you might encounter in the generated configs, check configs/*_explanation.txt

- After making the needed changes to the config file, you can run pipeline by specifying an entry point with "-entry", which takes as argument the name of one of the workflows included in the main.nf file.  
- ```bash
  nextflow -C standard_iss_experiment.config run  main.nf	\
						-entry iss							\
						--with_conda comunISS.yaml			\
	```


### Repository file hierarchy explanation
- *main.nf*: Running the pipeline should always start from here. Dynamically defined paths in the functionality count on the starting point of the "nextflow run"-command being the main.nf file.
- ***workflows/***: This directory contains a file for each type of experiment the pipeline supports. (ISS, MERFISH, ...) Each file represents a workflow for that type of experiment. If you're not a developer and solely want to adapt the pipeline somewhat to your usecase, this is the only file that you want to adapt. For instance: if you don't want to normalize your images, you can simply comment out that line. 
- ***src/***: This directory contains the entire codebase on which the pipeline is built. If you are somewhat familiar with nextflow or the Groovy language, you can also finetune any workflow in here, but at your own risk of course.

	- Every directory in the src/ directory will follow the same structure, which allows any contributor or user to add processes and workflows as he wishes, while maintaining a structured pipeline:
	- ***bin/***: This directory contains the binaries to whatever codebase the feature is implemented in.
	- ***processes/***: This directory contains .nf files that represent the lowest level of nextflow processes, these processes call whatever binaries are stored in bin/.
	- ***workflows/***: This directory contains a higher level of nextflow process management