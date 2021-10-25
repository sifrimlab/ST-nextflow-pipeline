# Installation & Usage

### Requirements
For the current version of the pipeline, you only need two frameworks are required to run it on any system that has acces to the pipeline.

- **Nextflow**: This can be installed by following the instructions at [Nextflow's documentation](https://www.nextflow.io/docs/latest/getstarted.html).
The current working version is guaranteed to work with nextflow version 20.10, however it will soon be updated to be compatible to the most recent nextflow version.

- **Conda**: Any form of environment management will most likely do. The recomended software is (Ana)Conda, which can be installed folowing [these steps](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).  This is used to automatically create the programming environment with all used languages and software packages without creating version conflicts.


### Dependencies
Here is a list of all dependencies that were installed to run the full pipeline in case you'd like to build them from scratch.
A complete list including version numbers can be found in the form of the staple.yml file, as can be described below.
- python
- numpy
- pip
- imagecodecs
- scikit-image
- scikit-learn
- pandas
- beautifusoup4
- umap-learn
- aicspylibczi
- tensorflow
- stardist
- csbdeep

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

That is everything that needs to be installed. After this, general usage of the pipeline is performed as such:

### Usage
- Create a personal config file containing all the parameters for your experiment. 
 ```bash
nextflow config -profile iss >> iss_exp.config
  ```
- *Note that this config file is where you change everything that you want to change, such as data directory, output directory, image format etc.*
For more details about the configuration of a pipeline run, see [Configuration](configuration.md).

 After making the needed changes to the config file, you can run pipeline by specifying an entry point with "-entry", which takes as argument the name of one of the workflows included in the main.nf file.  


 ```bash
nextflow -C iss_exp.config run main.nf	                \
			        -entry iss	        \
				--with_conda staple.yml	\
```

The *--with_conda* flag is only needed if you decide not the activate the conda environment prior to running the pipeline. This can be useful when submitting jobs to a high compute cluster.



