import core

import parameters
import numpy as np
import os
import platypus
from matplotlib import pyplot as plt


def sample_sem():
    structure = core.FilesFolders(parameters.sem_originals)
    sample = structure.random_pick()
    sem = core.Sem(sample)
    return sem


def plot_best_fit():
    post = core.PostProcessing()
    sem = sample_sem()
    [sem.min_diameter, sem.max_diameter, sem.min_threshold, sem.max_threshold] = post.find_best_params()
    sem.plot()


def run_ga(cpu_number):
    proc = core.Processing()
    problem = platypus.Problem(4, 6, 1)  # where Problem(variables, objective_funcs, constraints)

    problem.types[:] = [platypus.Real(5, 50), platypus.Real(50, 250),
                        platypus.Real(0, 255), platypus.Real(0, 255)]

    problem.constraints[0] = ">0"
    problem.function =  proc.objective_function
    if __name__ == "__main__":
        algorithms = [platypus.NSGAII]
        problems = [problem]
        with platypus.ProcessPoolEvaluator(cpu_number) as evaluator:
            results = platypus.experiment(algorithms, problems, nfe=900000, evaluator=evaluator)


# sem = core.Sem(parameters.sem_originals + '12 well_5mm height_3mm cross section_center_01.tif')
# sem.set_scale_bar()
# sem.set_anlysis_region()

# process = core.Processing()
# process.batch_adjust()
# process.batch_crop()

run_ga(cpu_number=6)




# params = [6.034690930796206, 144.71754272612029, 53.85510048175122, 121.59396264605]
# sem_cropped = core.Sem(parameters.sem_cropped + '12 well_5mm height_3mm cross section_center_01.tif')
# sem_cropped.min_diameter, sem_cropped.max_diameter, \
# sem_cropped.min_threshold, sem_cropped.max_threshold = params
# sem_cropped.plot(plot_type='ellipse')