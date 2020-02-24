from smartsim import Controller, Generator, State

# init state
state= State(experiment="h2o")

# create ensembles
ensemble_params = {"STEPS": [10, 15, 20, 25]}
run_settings = {"executable": "cp2k.psmp",
                "partition": "gpu",
                "exe_args": "-i h2o.inp",
                "nodes": 1}
state.create_ensemble("h2o-1", params=ensemble_params, run_settings=run_settings)

# Data Generation Phase
gen = Generator(state, model_files="./h2o.inp")
gen.generate()

sim = Controller(state, launcher="slurm")
sim.start()
sim.poll()
sim.release()
