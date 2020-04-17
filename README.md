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

## Project details
### Virus expansion simulation
#### Simulation rules
Simulation rules are extremely simple:
* People are located on map and can move in nine possible directions (including 
staying at given position) - space borders cannot be crossed out;
* Initial positions of people are randomly chosen;
* At each simulation step each person decides (by random choice) where
to go (only one step can be done); 
* Group of people being in certain position in certain time will set up a 
meeting. Each person can meet another from a group and the intensity of 
pairwise meeting is measured by duration (random number from range [0.0; 1.0]);
* If within group there is a sick person - he/she may pass the virus to 
another person - the actual probability of virus transmission is 
calculated as meeting_duration * global_transition_probability and the 
transmission event is decided by a flip of Bayesian coin;
* Each person infected in time stamp _t_, starts infecting from time stamp 
_t+1_.

#### Usage
To run a simulation execute the following command:
```bash
(DGLExploration) project_root$ python -m src.virus_simulation.execute \
    --map_size=100 \
    --people_number=100 \
    --simulation_name=test_simulation \
    --steps=200 \
    --snapshot_steps 50 100 150 \
    --transmission_probability=0.75 \
    --initial_seek_people=1
```
Where:
* `--map_size` is a size of space to place virtual people
* `--people_number` is a number of simulated people
* `--simulation_name` is a distinguishable name of simulation that will be 
used to generate snapshots
* `--steps` is a number of simulation steps _(default: 100)_
* `--snapshot_steps` are numbers of steps that simulation state snapshot will
be taken (apart from the last step which is enabled by default). _(default: not set)_
* `--transmission_probability` is a probability of virus transmission. _(default: 0.5)_
* `--initial_seek_people` is an initial number of people infected. _(default: 1)_


#### Results
One should expect results placed under location specified in 
`src.config.VIRUS_SIMULATION_OUTPUT_PATH` (located by design under `resources`).

The result format is the following:
```json
{
    "people": [
        {
            "person_id": 0,
            "person_sick": false
        },
        {
            "person_id": 1,
            "person_sick": true
        }
    ],
    "meetings": [
      {
            "meeting_pair": [
                16,
                34
            ],
            "meeting_duration": 0.7409445831243038,
            "meeting_time_stamp": 64
        },
        {
            "meeting_pair": [
                22,
                45
            ],
            "meeting_duration": 0.6641336785359672,
            "meeting_time_stamp": 64
        }
    ]
    
}
```
