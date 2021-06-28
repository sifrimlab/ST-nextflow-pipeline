# Installation & Usage

### Requirements
For the current version of the pipeline, you only need two frameworks are required to run it on any system that has acces to the pipeline.

- **Nextflow**: This can be installed by following the instructions at https://www.nextflow.io/docs/latest/getstarted.html.
The current working version is guaranteed to work with nextflow version 20.10, however it will soon be updated to be compatible to the most recent nextflow version.

- **Conda**: Any form of environment managent will most likely do. The recomended software is (Ana)Conda, which can be installed folowwing these steps: https://conda.io/projects/conda/en/latest/user-guide/install/index.html. This is used to automatically create the programming environment with all used languages and software packages without creating version conflicts.


### Installation

- Clone/fork the current master branch of the pipeline to your system.
 	```bash
	git clone https://github.com/WoutDavid/ST-nextflow-pipeline; cd ST-nextflow-pipeline
	```
- Create a conda environment containing all the dependencies of the current pipeline, and activate it.
 	```bash
	conda env create --file=staple.yml --prefix ./staple_env/
	conda activate ./staple_env/
	```
- Create a personal config file containing all the parameters you'll need for the functionality you want:
 ```bash
	nextflow config -profile iss >> standard_iss_experiment.config
  ```
- *Note that this config file is where you change everything that you want to change, such as data directory, output directory, image format etc.*
For more details about the configuration of a pipeline run, see [Configuration](configuration.md).

### Usage
 After making the needed changes to the config file, you can run pipeline by specifying an entry point with "-entry", which takes as argument the name of one of the workflows included in the main.nf file.  


 ```bash
  nextflow -C standard_iss_experiment.config run  main.nf	\
						-entry iss							\
						--with_conda staple.yml			\
```

The *--with_conda* flag is only needed if you decide not the activate the conda environment prior to running the pipeline. This can be useful when submitting jobs to a high compute cluster.



