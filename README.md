# DGL Library exploration

## Project overview
This is simple exploratory project of [DGL](https://www.dgl.ai/) that aim to 
discover possibilities of graph processing powered by Deep Learning.

## Project structure
```
repository_root
├── README.md                                       project description
├── requirements.txt                                dependecies definition
├── requirements-gpu.txt                            dependecies definition (GPU version)
├── resources                                       directory where to place data to be sued
├── notebooks                                       Jupyter notebooks with some experiments results.
└── src                                             main sources package
    └── config.py                                   global config of a project
```

## Setup
To set up the project:
* Create a conda environment (or venv if you like)
    ```bash
    conda create -n DGLExploration python=3.7
    ```
* Source the env
    ```bash
    conda activate DGLExploration
    ```
* Install requirements
    ```bash
    project_root$ pip install -r requirements.txt
    ```
    You can also install requirements suitable for GPU support 
    (in this case CUDA 10.0 is supported - check out [how to use different 
    version](https://docs.dgl.ai/en/0.4.x/install/)).
    ```bash
    project_root$ pip install -r requirements-gpu.txt
    ```
### Issues with jupyter notebook
Sometimes, in order to make the environment visible in jupyter notebook, the 
following command needs to be executed.
```bash
(DGLExploration) python -m ipykernel install --name "DGLExploration" --user
```