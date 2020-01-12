import autoarray as aa
from autoarray.plotters import plotters, mat_objs
from autoastro.plots import lensing_plotters
from autoastro import exc


@plotters.set_labels
def subplot(
    fit,
    positions=None,
    include=lensing_plotters.Include(),
    sub_plotter=plotters.SubPlotter(),
):

    number_subplots = 4

    sub_plotter = sub_plotter.plotter_with_new_output(
        output=mat_objs.Output(filename="fit_galaxy"),
    )


    sub_plotter.setup_subplot_figure(number_subplots=number_subplots)

    sub_plotter.setup_subplot(number_subplots=number_subplots, subplot_index=1)

    galaxy_data_array(
        galaxy_data=fit.galaxy_data, positions=positions, plotter=sub_plotter
    )

    sub_plotter.setup_subplot(number_subplots=number_subplots, subplot_index= 2)

    aa.plot.fit_imaging.model_image(
        fit=fit, include=include, points=positions, plotter=sub_plotter
    )

    sub_plotter.setup_subplot(number_subplots=number_subplots, subplot_index= 3)

    aa.plot.fit_imaging.residual_map(
        fit=fit, include=include, plotter=sub_plotter
    )

    sub_plotter.setup_subplot(number_subplots=number_subplots, subplot_index= 4)

    aa.plot.fit_imaging.chi_squared_map(
        fit=fit, include=include, plotter=sub_plotter
    )

    sub_plotter.output.subplot_to_figure()

    sub_plotter.close_figure()


def individuals(
    fit,
    positions=None,
    plot_image=False,
    plot_noise_map=False,
    plot_model_image=False,
    plot_residual_map=False,
    plot_chi_squared_map=False,
    include=lensing_plotters.Include(),
    plotter=plotters.Plotter(),
):

    if plot_image:

        galaxy_data_array(
            galaxy_data=fit.galaxy_data,
            mask=fit.mask,
            positions=positions,
            include=include,
            plotter=plotter,
        )

    if plot_noise_map:

        aa.plot.fit_imaging.noise_map(
            fit=fit,
            mask=fit.mask,
            points=positions,
            include=include,
            plotter=plotter,
        )

    if plot_model_image:

        aa.plot.fit_imaging.model_image(
            fit=fit,
            mask=fit.mask,
            points=positions,
            include=include,
            plotter=plotter,
        )

    if plot_residual_map:

        aa.plot.fit_imaging.residual_map(
            fit=fit, mask=fit.mask, include=include, plotter=plotter
        )

    if plot_chi_squared_map:

        aa.plot.fit_imaging.chi_squared_map(
            fit=fit, mask=fit.mask, include=include, plotter=plotter
        )


@plotters.set_labels
def galaxy_data_array(
    galaxy_data,
    positions=None,
    include=lensing_plotters.Include(),
    plotter=plotters.Plotter(),
):

    if galaxy_data.use_image:
        title = "Galaxy Data Image"
    elif galaxy_data.use_convergence:
        title = "Galaxy Data Convergence"
    elif galaxy_data.use_potential:
        title = "Galaxy Data Potential"
    elif galaxy_data.use_deflections_y:
        title = "Galaxy Data Deflections (y)"
    elif galaxy_data.use_deflections_x:
        title = "Galaxy Data Deflections (x)"
    else:
        raise exc.PlottingException(
            "The galaxy data_type arrays does not have a True use_profile_type"
        )

    plotter.array.plot(
        array=galaxy_data.image,
        mask=galaxy_data.mask,
        points=positions,
        include_origin=include.origin,
    )