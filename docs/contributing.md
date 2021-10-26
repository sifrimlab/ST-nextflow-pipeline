# Contributing
If you would like to add a feature (process, workflow etc.) to the pipeline, please follow these steps:

### Create your own feature branch
- First fork the development branch to your local machine if you're not an active contributor.
```
git clone https://github.com/sifrimlab/ST-nextflow-pipeline/tree/development
```
- Create a feature branch with a descriptive name, e.g.:

```
git checkout -b graph-decoding-iss
```

- Add any all code necessary for the feature to the branch.

### Merging branches
Make sure that after editing, the main test suites are still functional by running:
```
nextflow -C ./configs/tests/TYPE_test.config run test.main.nf --test TYPE

```
where TYPE = all profiles given in at the top of the ```test.main.nf``` file.

If your feature passes all test suites, you can submit a pull request to merge it with the development branch. 
Never merge with the Master branch, this will be done by the main contributors.



