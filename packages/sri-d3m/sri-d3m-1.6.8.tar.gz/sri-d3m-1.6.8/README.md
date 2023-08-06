# PSL TA1 Implementations
This code base contains the code to create TA1 primities that contain PSL solutoions to 
common modelling problems.


## Building & Submitting the docker images:
1. The following must be located in the docker folder before the docker image is built:
    - PSL Jar: Canary jars can be found at ```https://linqs-data.soe.ucsc.edu/maven/repositories/psl-releases/org/linqs/psl-cli/CANARY/```
    - primitive-interfaces: git@gitlab.datadrivendiscovery.org:d3m/primitive-interfaces.git
    - types: git@gitlab.datadrivendiscovery.org:d3m/types.git

2. cd to the docker directory and run the following command. The label ensures that the image is registered against 
the correct docker ci project in the d3m gitlab ```docker build -f Dockerfile -t registry.datadrivendiscovery.org/ta1/sri_ta1:latest .```

3. Udating the primitives and generating the sample pipelines and the pipeline_runs
   - Update the DOCKER_IMAGE, DATASET_HOME and VERSION variables in config.py
   - pip uninstall sri-d3m
   - rm dist/*.*
   - python setup.py sdist bdist_wheel
   - pip install dist/sri-d3m-1. <tab>
   - ~/.local/bin/twine upload dist/*
   * Build the ta2 docker image with the sri-d3m version build above in the Dockerfile
   - ./sh scripts/generate_primitive_definitions.sh <path to branched fork of the d3m primitives repo>
   - Do a merge request between the forked branch and the master branch once you have pushed and CI passes.
   

## Implementations
### Graph completion:
