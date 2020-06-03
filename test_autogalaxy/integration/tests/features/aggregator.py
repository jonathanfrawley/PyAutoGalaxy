import os

import autofit as af
import autogalaxy as ag
from test_autogalaxy.integration.tests.imaging import runner

test_type = "features"
test_name = "aggregator"
data_label = "galaxy_x1__dev_vaucouleurs"
instrument = "vro"


def make_pipeline(name, phase_folders, non_linear_class=af.MultiNest):
    phase1 = ag.PhaseImaging(
        phase_name="phase_1",
        phase_folders=phase_folders,
        galaxies=dict(
            galaxy=ag.GalaxyModel(redshift=0.5, sersic=ag.lp.EllipticalSersic)
        ),
        non_linear_class=non_linear_class,
    )

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 40
    phase1.optimizer.sampling_efficiency = 0.8

    return ag.PipelineDataset(name, phase1)


if __name__ == "__main__":
    import sys

    runner.run(sys.modules[__name__])

    test_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))
    output_path = f"{test_path}../output"
    agg = af.Aggregator(directory=str(output_path))

    # This should print "test_dataset" -> see integration/tests/imaging/runner.py

    for dataset in agg.values("dataset"):

        print(dataset)
        print(dataset.name)

    for mask in agg.values("mask"):

        print(mask)

    # for meta_dataset in agg.values("meta_dataset"):
    #
    #     print(meta_dataset.sub_size)

    agg_phase_1 = agg.filter(agg.phase == "phase_1")

    phase_attribute_gen = agg_phase_1.values("phase_attributes")

    for phase_attribute in phase_attribute_gen:

        hyper_galaxy_image_path_dict = phase_attribute.hyper_galaxy_image_path_dict
        print(hyper_galaxy_image_path_dict)

    agg_phase_2 = agg.filter(agg.phase == "phase_2")

    phase_attribute_gen = agg_phase_2.values("phase_attributes")

    for phase_attribute in phase_attribute_gen:

        hyper_galaxy_image_path_dict = phase_attribute.hyper_galaxy_image_path_dict
        print(hyper_galaxy_image_path_dict)