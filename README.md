TuneMC
=====================================================

TuneMC is an example framework for applying Bayesian optimization to Monte Carlo (MC) event generator tuning. We provide the code realization for the method described in the [article](https://arxiv.org/abs/1610.08328) below:

    Event generator tuning using Bayesian optimization
    Philip Ilten, Mike Williams, Yunjie Yang
    arXiv:1610.08328

where you can also find much more details about the method and background information.

### Set up and run the TuneMC framework

**STEP 1: Install Spearmint and PYTHIA**

1. Follow the instructions on [Spearmint](https://github.com/HIPS/Spearmint) (a Bayesian optimization realization in Python) and [PYTHIA](http://home.thep.lu.se/Pythia/) (a popular Monte Carlo event generator widely used in High Energy Physics event simulation, e.g. LHC physics) to install both software. (Note: no special package flags are needed during Pythia installation.) 
2. Git clone the TuneMC code. 
3. In `./pythia_space/MakeFile`, change the `PYTHIA_HOME` variable to the top-level directory of your installation, and just type `make` to compile the `pythia_gen.cc` code. 

The framework should now be ready to use. If you like, you are welcome to familiarize yourself with basic usage of Spearmint and/or PYTHIA by looking at the examples they provide.

**STEP 2: Set up the tune**

The tuning configuration is specified in the `tune_config.json` file at the top-level directory. The user should specify all the variables in this json file. The meaning of these variables are explained below: 

- `WorkHOME`: the highest-level directory of this TuneMC framework 
- `N_events`: number of PYTHIA events to generate per query 
- `n_cores`: number of virtual cores to parallelize the PYTHIA event generation, e.g. if `N_events` is 100,000 and `n_cores` is 5, then the generation is parallelized with 5 processes and each core generates 20,000 events 
- `block1(2,3)`: the "block" to tune. The meaning of these blocks is described in our [article](https://arxiv.org/abs/1610.08328). Block1 is a 3-parameter tuning problem, while block2 and block3 have 6 and 11 parameters respectively. Whether to tune a block is specified by a Pythonic boolean, `"True"` or `"False"`. At least one of the three needs to be `"True"`, you can also choose to turn on two or even all three blocks 
- `spearmint_dir`: this points to the `Spearmint/spearmint` directory of your Spearmint installation, where the Spearmint `main.py` file is found 
- `spearmint_expt_name`: the name of the current spearmint tuning experiment. It is used by the MongoDB database used by Spearmint to associate tuning information with the corresponding experiment 
- `new_expt`: a boolean variable used to specify whether you want to continue with an existing experiment (when you specify this to be `"False"`) or you want to start a new experiment (when you set it to `"True"`) 

**STEP 3: Run the tune**
Now you should be able to run a MC tuning by simply executing the `master.py` code with command `$ python master.py` at the top-level 

### Monitor/visualize the tuning progress
This part is not indispensible but provided for the convenience of monitoring the tuning progress. One can run `$ python get_tune_summay.py` once the tuning is up and running. It will generate a few plots that help monitoring the tuning progress. The plots are generated in the `./spearmint_space/plots` directory. The `save_results.py` code is provided for convenience to save a particular tune experiments.

### Terminate the tune
One can simply "ctrl+c" the `master.py` process directly at any time. Spearmint uses the MongoDB database to manage the experiments. One can choose to resume an existing tuning experiment by setting the `new_expt` flag in the `tune_config.json` file to `"False"` and simply run `$ python master.py` to continue the tuning.

 
### Disclaimers

-  The method of using Bayesian optimization to the Monte Carlo event generator tuning problem is in principle independent on the specific generator used as long as the generator of interest contains free parameter that need to be determined by comparing with data. We picked PYTHIA just as an example. 

- In addition, one could imagine applying other Bayesian optimization packages to this MC event generator tuning problem. The interface is provided by just calling the `get_objective_func()` function defined in `$WorkHOME/pythia_space/pythia_functions.py`. One can look at `$WorkHOME/spearmint_space/Spearmint-Pythia-Tune.py` as an example.  

- Unlike in a real MC generator tuning where one compares the outcome of MC generator with real data, this framework performs a closure test where it treats the PYTHIA8 default tune as "data". Hence all parameter values are known, and can be used to assess the performance of the optimizer. Again, we refer the interested reader to our [article](https://arxiv.org/abs/1610.08328) regarding the justification of this choice.

