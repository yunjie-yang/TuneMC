TuneMC
=====================================================

TuneMC is an example framework for Monte Carlo (MC) event generator tuning using Bayesian optimization. It provides the code realization for the method described in the following article:
    Event generator tuning using Bayesian optimization
    Philip Ilten, Mike Williams, Yunjie Yang
    [arXiv:1610.08328](https://arxiv.org/abs/1610.08328)

### Set up and run the TuneMC framework
**STEP 1: Install Spearmint and PYTHIA**

1. Follow the instructions on [Spearmint](https://github.com/HIPS/Spearmint) and [PYTHIA](http://home.thep.lu.se/~torbjorn/pythia82html/Welcome.html), and install both software. 
2. Download/clone the TuneMC code. 
3. In `./pythia_space/MakeFile`, change the `PYTHIA_HOME` variable to the top-level directory of your installation, and just type `make` to compile the `pythia_gen.cc` code. 

The framework should now be ready to use. If you like, you can also familiarize yourself with how to use Spearmint and/or PYTHIA with the examples they provide.

**STEP 2: Set up the tune**
The tuning configuration is specified in the `tune_config.json` file at the top-level directory. The user should specify all the variables in this json file. The meaning of these variables are explained below:
1. `WorkHOME`: the top-level directory of this TuneMC framework 
- `N_events`: number of PYTHIA events to generate per query 
- `n_cores`: number of virtual cores to use during PYTHIA event generation 
- `block1(2,3)`: the "block" to tune. The meaning of these blocks are described in our associated [article](https://arxiv.org/abs/1610.08328). Block1 is a 3-parameter tuning problem, while block2 and block3 have 6 and 11 parameters respectively 
- `spearmint_dir`: this points to the `Spearmint/spearmint` directory of your Spearmint installation, where the Spearmint `main.py` file lives 
- `spearmint_expt_name`: the name of the current spearmint tuning experiment. It is used by the MongoDB database used by Spearmint to associate tuning information with the corresponding experiment 
- `new_expt`: a boolean variable used to specify whether you want to continue with the existing experiment using existing database (when you specify this to be "False") or you want to start a new experiment 

**STEP 3: Run the tune**
Now you should be able to run the tune by executing the `master.py` code with command `$ python master.py`

### Monitor tuning progress
This part is not indispensible but provided as an example of monitoring the tuning progress. One can run `$ python get_tune_summay.py` once the tuning is running. It will generate a few plots that help monitoring the tuning progress. They are all generated in the `./spearmint_space/Plots` directory.

### Terminate the tune
One can `ctrl+c` the `master.py` process directly at any time. Spearmint uses the MongoDB database to manage the experiments. One can also resume an existing tuning experiment by setting the `new_expt` flag in the `tune_config.json` file to `"False"` and run `$ python master.py` to continue the tuning.

 
### Disclaimer
1. The method of using Bayesian optimization to the Monte Carlo event generator tuning problem is in principle not dependent on the specific generator used provided the generator contains free variables that need to be determined by comparing with data. We picked PYTHIA8 just as an example. 

- In addition, one could imagine applying other Bayesian optimization packages to this MC event generator tuning problem. The interface is provided by just calling the `get_objective_func()` function defined in `./pythia_space/pythia_functions.py` 

- Unlike in a real MC generator tuning where one compares the outcome of MC generator with real data, this framework performs a closure test where it treats the PYTHIA8 default tune as "data". Hence all parameter values are in fact known, and can be used to assess the performance of the optimizer. 

