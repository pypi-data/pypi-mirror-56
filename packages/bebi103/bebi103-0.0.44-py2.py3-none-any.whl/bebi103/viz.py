import warnings

import numpy as np
import pandas as pd
import scipy.stats as st
import numba

try:
    import pymc3 as pm
except:
    pass

import scipy.ndimage
import skimage

import matplotlib._contour
from matplotlib.pyplot import get_cmap as mpl_get_cmap

import bokeh.application
import bokeh.application.handlers
import bokeh.models
import bokeh.palettes
import bokeh.plotting

try:
    import datashader as ds
    import datashader.bokeh_ext
except ImportError as e:
    warnings.warn(
        f"""DataShader import failed with error "{e}".
Features requiring DataShader will not work and you will get exceptions."""
    )


from . import utils
from . import image

try:
    from . import stan
except:
    warnings.warn(
        "Could not import `stan` submodule. Perhaps pystan is not properly installed."
    )


def plot_with_error_bars(
    centers, confs, names, marker_kwargs={}, line_kwargs={}, **kwargs
):
    """Make a horizontal plot of centers/conf ints with error bars.

    Parameters
    ----------
    centers : array_like, shape (n,)
        Array of center points for error bar plot.
    confs : array_like, shape (n, 2)
        Array of low and high values of confidence intervals
    names : list of strings
        Names of the variables for the plot. These give the y-ticks.
    marker_kwargs : dict, default {}
        Kwargs to be passed to p.circle() for plotting centers.
    line_kwargs : dict, default {}
        Kwargs passsed to p.line() to plot the confidence interval.
    kwargs : dict
        Any addition kwargs are passed to bokeh.plotting.figure().

    Returns
    -------
    output : Bokeh figure
        Plot of error bars.
    """
    n = len(names)
    if len(centers) != n:
        raise ValueError("len(centers) ≠ len(names)")
    if confs.shape != (n, 2):
        raise ValueError("Shape of `confs` must be (len(names), 2).")

    frame_height = kwargs.pop("frame_height", 50 * n)
    frame_width = kwargs.pop("frame_width", 450)
    line_width = kwargs.pop("line_width", 2)

    p = bokeh.plotting.figure(
        y_range=names[::-1],
        frame_height=frame_height,
        frame_width=frame_width,
        **kwargs,
    )

    p.circle(x=centers, y=names, **marker_kwargs)
    for conf, name in zip(confs, names):
        p.line(x=conf, y=[name, name], line_width=2)

    return p


def fill_between(
    x1=None,
    y1=None,
    x2=None,
    y2=None,
    x_axis_label=None,
    y_axis_label=None,
    x_axis_type="linear",
    y_axis_type="linear",
    title=None,
    plot_height=300,
    plot_width=450,
    fill_color="#1f77b4",
    line_color="#1f77b4",
    show_line=True,
    line_width=1,
    fill_alpha=1,
    line_alpha=1,
    p=None,
    **kwargs,
):
    """
    Create a filled region between two curves.

    Parameters
    ----------
    x1 : array_like
        Array of x-values for first curve
    y1 : array_like
        Array of y-values for first curve
    x2 : array_like
        Array of x-values for second curve
    y2 : array_like
        Array of y-values for second curve
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default None
        Label for the y-axis. Ignored if `p` is not None.
    x_axis_type : str, default 'linear'
        Either 'linear' or 'log'.
    y_axis_type : str, default 'linear'
        Either 'linear' or 'log'.    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    fill_color : str, default '#1f77b4'
        Color of fill as a hex string.
    line_color : str, default '#1f77b4'
        Color of the line as a hex string.
    show_line : bool, default True
        If True, show the lines on the edges of the fill.
    line_width : int, default 1
        Line width of lines on the edgs of the fill.
    fill_alpha : float, default 1.0
        Opacity of the fill.
    line_alpha : float, default 1.0
        Opacity of the lines.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with fill-between.

    Notes
    -----
    .. Any remaining kwargs are passed to bokeh.models.patch().
    """

    if p is None:
        p = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_type=x_axis_type,
            y_axis_type=y_axis_type,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            title=title,
        )

    p.patch(
        x=np.concatenate((x1, x2[::-1])),
        y=np.concatenate((y1, y2[::-1])),
        alpha=fill_alpha,
        fill_color=fill_color,
        line_width=0,
        line_alpha=0,
        **kwargs,
    )

    if show_line:
        p.line(x1, y1, line_width=line_width, alpha=line_alpha, color=line_color)
        p.line(x2, y2, line_width=line_width, alpha=line_alpha, color=line_color)

    return p


def ecdf(
    data=None,
    conf_int=False,
    ptiles=[2.5, 97.5],
    n_bs_reps=1000,
    fill_color="lightgray",
    fill_alpha=1,
    p=None,
    x_axis_label=None,
    y_axis_label="ECDF",
    title=None,
    plot_height=300,
    plot_width=450,
    formal=False,
    complementary=False,
    x_axis_type="linear",
    y_axis_type="linear",
    **kwargs,
):
    """
    Create a plot of an ECDF.

    Parameters
    ----------
    data : array_like
        One-dimensional array of data. Nan's are ignored.
    conf_int : bool, default False
        If True, display a confidence interval on the ECDF.
    ptiles : list, default [2.5, 97.5]
        The percentiles to use for the confidence interval. Ignored it
        `conf_int` is False.
    n_bs_reps : int, default 1000
        Number of bootstrap replicates to do to compute confidence
        interval. Ignored if `conf_int` is False.
    fill_color : str, default 'lightgray'
        Color of the confidence interbal. Ignored if `conf_int` is
        False.
    fill_alpha : float, default 1
        Opacity of confidence interval. Ignored if `conf_int` is False.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF' or 'ECCDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    formal : bool, default False
        If True, make a plot of a formal ECDF (staircase). If False,
        plot the ECDF as dots.
    complementary : bool, default False
        If True, plot the empirical complementary cumulative
        distribution functon.
    x_axis_type : str, default 'linear'
        Either 'linear' or 'log'.
    y_axis_type : str, default 'linear'
        Either 'linear' or 'log'.
    kwargs
        Any kwargs to be passed to either p.circle or p.line, for
        `formal` being False or True, respectively.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with ECDF.
    """
    # Check data to make sure legit
    data = utils._convert_data(data)

    # Get y-axis label
    if p is None and y_axis_label is None:
        if complementary:
            y_axis_label = "ECCDF"
        else:
            y_axis_label = "ECDF"

    # Data points on ECDF
    x, y = _ecdf_vals(data, formal, complementary)

    # Instantiate Bokeh plot if not already passed in
    if p is None:
        p = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            x_axis_type=x_axis_type,
            y_axis_type=y_axis_type,
            title=title,
        )

    # Do bootstrap replicates
    if conf_int:
        x_plot = np.sort(np.unique(x))
        bs_reps = np.array(
            [
                _ecdf_arbitrary_points(np.random.choice(data, size=len(data)), x_plot)
                for _ in range(n_bs_reps)
            ]
        )

        # Compute the confidence intervals
        ecdf_low, ecdf_high = np.percentile(np.array(bs_reps), ptiles, axis=0)

        # Make them formal
        _, ecdf_low = _to_formal(x=x_plot, y=ecdf_low)
        x_plot, ecdf_high = _to_formal(x=x_plot, y=ecdf_high)

        p = fill_between(
            x1=x_plot,
            y1=ecdf_low,
            x2=x_plot,
            y2=ecdf_high,
            fill_color=fill_color,
            fill_alpha=fill_alpha,
            show_line=False,
            p=p,
        )

    if formal:
        # Line of steps
        p.line(x, y, **kwargs)

        # Rays for ends
        if complementary:
            p.ray(x[0], 1, None, np.pi, **kwargs)
            p.ray(x[-1], 0, None, 0, **kwargs)
        else:
            p.ray(x[0], 0, None, np.pi, **kwargs)
            p.ray(x[-1], 1, None, 0, **kwargs)
    else:
        p.circle(x, y, **kwargs)

    return p


def histogram(
    data=None,
    bins=10,
    p=None,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_height=300,
    plot_width=450,
    density=False,
    kind="step",
    **kwargs,
):
    """
    Make a plot of a histogram of a data set.

    Parameters
    ----------
    data : array_like
        1D array of data to make a histogram out of
    bins : int, array_like, or one of 'exact' or 'integer' default 10
        Setting for `bins` kwarg to be passed to `np.histogram()`. If
        `'exact'`, then each unique value in the data gets its own bin.
        If `integer`, then integer data is assumed and each integer gets
        its own bin.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default None
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    density : bool, default False
        If True, normalized the histogram. Otherwise, base the histogram
        on counts.
    kind : str, default 'step'
        The kind of histogram to display. Allowed values are 'step' and
        'step_filled'.

    Returns
    -------
    output : Bokeh figure
        Figure populated with histogram.
    """
    if data is None:
        raise RuntimeError("Input `data` must be specified.")

    # Instantiate Bokeh plot if not already passed in
    if p is None:
        if y_axis_label is None:
            if density:
                y_axis_label = "density"
            else:
                y_axis_label = "count"

        p = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            title=title,
            y_range=bokeh.models.DataRange1d(start=0),
        )

    if bins == "exact":
        a = np.unique(data)
        if len(a) == 1:
            bins = np.array([a[0] - 0.5, a[0] + 0.5])
        else:
            bins = np.concatenate(
                (
                    (a[0] - (a[1] - a[0]) / 2,),
                    (a[1:] + a[:-1]) / 2,
                    (a[-1] + (a[-1] - a[-2]) / 2,),
                )
            )
    elif bins == "integer":
        if np.any(data != np.round(data)):
            raise RuntimeError("'integer' bins chosen, but data are not integer.")
        bins = np.arange(data.min() - 1, data.max() + 1) + 0.5

    # Compute histogram
    f, e = np.histogram(data, bins=bins, density=density)
    e0 = np.empty(2 * len(e))
    f0 = np.empty(2 * len(e))
    e0[::2] = e
    e0[1::2] = e
    f0[0] = 0
    f0[-1] = 0
    f0[1:-1:2] = f
    f0[2:-1:2] = f

    if kind == "step":
        p.line(e0, f0, **kwargs)

    if kind == "step_filled":
        x2 = [e0.min(), e0.max()]
        y2 = [0, 0]
        p = fill_between(e0, f0, x2, y2, show_line=True, p=p, **kwargs)

    return p


def jitter(
    data=None,
    cats=None,
    val=None,
    p=None,
    horizontal=False,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_height=300,
    plot_width=400,
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    width=0.4,
    order=None,
    val_axis_type="linear",
    show_legend=False,
    color_column=None,
    tooltips=None,
    **kwargs,
):
    """
    Make a jitter plot from a tidy DataFrame.

    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hastables
        Name of column(s) to use as categorical variable.
    val : hashable
        Name of column to use as value variable.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    horizontal : bool, default False
        If true, the categorical axis is the vertical axis.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    width : float, default 0.4
        Maximum allowable width of jittered points. A value of 1 means
        that the points take the entire space allotted.
    order : list or None
        If not None, must be a list of unique entries in `df[val]`. The
        order of the list specifies the order of the boxes. If None,
        the boxes appear in the order in which they appeared in the
        inputted DataFrame.
    val_axis_type : str, default 'linear'
        Type of scaling for the quantitative axis, wither 'linear' or
        'log'.
    show_legend : bool, default False
        If True, display legend.
    color_column : str, default None
        Column of `data` to use in determining color of glyphs. If None,
        then `cats` is used.
    tooltips : list of Bokeh tooltips
        Tooltips to add to the plot.
    kwargs
        Any kwargs to be passed to p.circle when making the jitter plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with jitter plot.
    """

    cols = _check_cat_input(data, cats, val, color_column, tooltips, palette, kwargs)

    grouped = data.groupby(cats)

    if p is None:
        p, factors, color_factors = _cat_figure(
            data,
            grouped,
            plot_height,
            plot_width,
            x_axis_label,
            y_axis_label,
            title,
            order,
            color_column,
            tooltips,
            horizontal,
            val_axis_type,
        )
    else:
        _, factors, color_factors = _get_cat_range(
            data, grouped, order, color_column, horizontal
        )
        if tooltips is not None:
            p.add_tools(bokeh.models.HoverTool(tooltips=tooltips))

    if "color" not in kwargs:
        if color_column is None:
            color_column = "cat"
        kwargs["color"] = bokeh.transform.factor_cmap(
            color_column, palette=palette, factors=color_factors
        )

    source = _cat_source(data, cats, cols, color_column)

    if show_legend:
        kwargs["legend"] = "__label"

    if horizontal:
        p.circle(
            source=source,
            x=val,
            y=bokeh.transform.jitter("cat", width=width, range=p.y_range),
            **kwargs,
        )
        p.ygrid.grid_line_color = None
    else:
        p.circle(
            source=source,
            y=val,
            x=bokeh.transform.jitter("cat", width=width, range=p.x_range),
            **kwargs,
        )
        p.xgrid.grid_line_color = None

    return p


def box(
    data=None,
    cats=None,
    val=None,
    p=None,
    horizontal=False,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_height=300,
    plot_width=400,
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    width=0.4,
    order=None,
    tooltips=None,
    val_axis_type="linear",
    display_outliers=True,
    box_kwargs=None,
    whisker_kwargs=None,
    outlier_kwargs=None,
):
    """
    Make a box-and-whisker plot from a tidy DataFrame.

    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hastables
        Name of column(s) to use as categorical variable.
    val : hashable
        Name of column to use as value variable.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all boxes are colored with that color. Default is
        the default color cycle employed by Altair.
    width : float, default 0.4
        Maximum allowable width of the boxes. A value of 1 means that
        the boxes take the entire space allotted.
    val_axis_type : str, default 'linear'
        Type of scaling for the quantitative axis, wither 'linear' or
        'log'.
    show_legend : bool, default False
        If True, display legend.
    tooltips : list of Bokeh tooltips
        Tooltips to add to the plot.
    order : list or None
        If not None, must be a list of unique entries in `df[val]`. The
        order of the list specifies the order of the boxes. If None,
        the boxes appear in the order in which they appeared in the
        inputted DataFrame.
    display_outliers : bool, default True
        If True, display outliers, otherwise suppress them. This should
        only be False when making an overlay with a jitter plot.
    box_kwargs : dict, default None
        A dictionary of kwargs to be passed into `p.hbar()` or
        `p.vbar()` when constructing the boxes for the box plot.
    whisker_kwargs : dict, default None
        A dictionary of kwargs to be passed into `p.segment()`
        when constructing the whiskers for the box plot.
    outlier_kwargs : dict, default None
        A dictionary of kwargs to be passed into `p.circle()`
        when constructing the outliers for the box plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with box-and-whisker plot.

    Notes
    -----
    .. Uses the Tukey convention for box plots. The top and bottom of
       the box are respectively the 75th and 25th percentiles of the
       data. The line in the middle of the box is the median. The
       top whisker extends to the lesser of the largest data point and
       the top of the box plus 1.5 times the interquartile region (the
       height of the box). The bottom whisker extends to the greater of
       the smallest data point and the bottom of the box minus 1.5 times
       the interquartile region. Data points not between the ends of the
       whiskers are considered outliers and are plotted as individual
       points.
    """
    cols = _check_cat_input(data, cats, val, None, tooltips, palette, box_kwargs)

    if whisker_kwargs is None:
        whisker_kwargs = {"line_color": "black"}
    elif type(whisker_kwargs) != dict:
        raise RuntimeError("`whisker_kwargs` must be a dict.")

    if outlier_kwargs is None:
        outlier_kwargs = dict()
    elif type(outlier_kwargs) != dict:
        raise RuntimeError("`outlier_kwargs` must be a dict.")

    if box_kwargs is None:
        box_kwargs = {"line_color": "black"}
    elif type(box_kwargs) != dict:
        raise RuntimeError("`box_kwargs` must be a dict.")

    grouped = data.groupby(cats)

    if p is None:
        p, factors, color_factors = _cat_figure(
            data,
            grouped,
            plot_height,
            plot_width,
            x_axis_label,
            y_axis_label,
            title,
            order,
            None,
            tooltips,
            horizontal,
            val_axis_type,
        )
    else:
        if tooltips is not None:
            p.add_tools(bokeh.models.HoverTool(tooltips=tooltips))

        _, factors, color_factors = _get_cat_range(
            data, grouped, order, None, horizontal
        )

    source_box, source_outliers = _box_source(data, cats, val, cols)

    if "fill_color" not in box_kwargs:
        box_kwargs["fill_color"] = bokeh.transform.factor_cmap(
            "cat", palette=palette, factors=factors
        )
    if "line_color" not in box_kwargs:
        box_kwargs["line_color"] = "black"

    if "color" in outlier_kwargs:
        if "line_color" in outlier_kwargs or "fill_color" in outlier_kwargs:
            raise RuntimeError(
                "If `color` is in `outlier_kwargs`, `line_color` and `fill_color` cannot be."
            )
    else:
        if "fill_color" not in outlier_kwargs:
            outlier_kwargs["fill_color"] = bokeh.transform.factor_cmap(
                "cat", palette=palette, factors=factors
            )
        if "line_color" not in outlier_kwargs:
            outlier_kwargs["line_color"] = bokeh.transform.factor_cmap(
                "cat", palette=palette, factors=factors
            )

    if horizontal:
        p.segment(
            source=source_box,
            y0="cat",
            y1="cat",
            x0="top",
            x1="top_whisker",
            **whisker_kwargs,
        )
        p.segment(
            source=source_box,
            y0="cat",
            y1="cat",
            x0="bottom",
            x1="bottom_whisker",
            **whisker_kwargs,
        )
        p.hbar(
            source=source_box,
            y="cat",
            left="top_whisker",
            right="top_whisker",
            height=width / 4,
            **whisker_kwargs,
        )
        p.hbar(
            source=source_box,
            y="cat",
            left="bottom_whisker",
            right="bottom_whisker",
            height=width / 4,
            **whisker_kwargs,
        )
        p.hbar(
            source=source_box,
            y="cat",
            left="bottom",
            right="top",
            height=width,
            **box_kwargs,
        )
        p.hbar(
            source=source_box,
            y="cat",
            left="middle",
            right="middle",
            height=width,
            **box_kwargs,
        )
        if display_outliers:
            p.circle(source=source_outliers, y="cat", x=val, **outlier_kwargs)
        p.ygrid.grid_line_color = None
    else:
        p.segment(
            source=source_box,
            x0="cat",
            x1="cat",
            y0="top",
            y1="top_whisker",
            **whisker_kwargs,
        )
        p.segment(
            source=source_box,
            x0="cat",
            x1="cat",
            y0="bottom",
            y1="bottom_whisker",
            **whisker_kwargs,
        )
        p.vbar(
            source=source_box,
            x="cat",
            bottom="top_whisker",
            top="top_whisker",
            width=width / 4,
            **whisker_kwargs,
        )
        p.vbar(
            source=source_box,
            x="cat",
            bottom="bottom_whisker",
            top="bottom_whisker",
            width=width / 4,
            **whisker_kwargs,
        )
        p.vbar(
            source=source_box,
            x="cat",
            bottom="bottom",
            top="top",
            width=width,
            **box_kwargs,
        )
        p.vbar(
            source=source_box,
            x="cat",
            bottom="middle",
            top="middle",
            width=width,
            **box_kwargs,
        )
        if display_outliers:
            p.circle(source=source_outliers, x="cat", y=val, **outlier_kwargs)
        p.xgrid.grid_line_color = None

    return p


def ecdf_collection(
    data=None,
    cats=None,
    val=None,
    p=None,
    complementary=False,
    formal=False,
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    order=None,
    show_legend=True,
    tooltips=None,
    val_axis_type="linear",
    ecdf_axis_type="linear",
    marker_kwargs={},
    **kwargs,
):
    """
    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hastables
        Name of column(s) to use as categorical variable (x-axis).
    val : hashable
        Name of column to use as value variable.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    complementary : bool, default False
        If True, plot the empirical complementary cumulative
        distribution functon.
    formal : bool, default False
        If True, make a plot of a formal ECDF (staircase). If False,
        plot the ECDF as dots.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    show_legend : bool, default False
        If True, show legend.
    order : list or None
        If not None, must be a list of unique entries in `df[val]`. The
        order of the list specifies the order of the boxes. If None,
        the boxes appear in the order in which they appeared in the
        inputted DataFrame.
    tooltips : list of 2-tuples
        Specification for tooltips. Ignored if `formal` is True.
    show_legend : bool, default False
        If True, show a legend.
    val_axis_type : 'linear' or 'log'
        Type of x-axis.
    ecdf_axis_type : 'linear' or 'log'
        Type of y-axis.

    kwargs
        Any kwargs to be passed to bokeh.plotting.figure().

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with jitter plot or box plot.
    if formal and tooltips is not None:
        raise RuntimeError('tooltips not possible for formal ECDFs.')
    """
    cols = _check_cat_input(data, cats, val, None, tooltips, palette, marker_kwargs)

    if complementary:
        y = "__ECCDF"
        if "y_axis_label" not in kwargs:
            kwargs["y_axis_label"] = "ECCDF"
    else:
        y = "__ECDF"
        if "y_axis_label" not in kwargs:
            kwargs["y_axis_label"] = "ECDF"

    if "x_axis_label" not in kwargs:
        kwargs["x_axis_label"] = val

    if p is None:
        if "height" not in kwargs:
            kwargs["height"] = 300
        if "width" not in kwargs:
            kwargs["width"] = 400
        p = bokeh.plotting.figure(**kwargs)

    if formal:
        p = _ecdf_collection_formal(
            data,
            val,
            cats,
            complementary,
            order,
            palette,
            show_legend,
            p,
            **marker_kwargs,
        )
    else:
        p = _ecdf_collection_dots(
            data,
            val,
            cats,
            cols,
            complementary,
            order,
            palette,
            show_legend,
            y,
            p,
            **marker_kwargs,
        )

    if not formal and tooltips is not None:
        p.add_tools(bokeh.models.HoverTool(tooltips=tooltips))

    if show_legend:
        if complementary:
            p.legend.location = "top_right"
        else:
            p.legend.location = "bottom_right"

    return p


def colored_ecdf(
    data=None,
    cats=None,
    val=None,
    p=None,
    complementary=False,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_height=300,
    plot_width=400,
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    order=None,
    show_legend=True,
    tooltips=None,
    val_axis_type="linear",
    ecdf_axis_type="linear",
    **kwargs,
):
    """
    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hashables
        Name of column(s) to use as categorical variable (x-axis).
    val : hashable
        Name of column to use as value variable.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    complementary : bool, default False
        If True, plot the empirical complementary cumulative
        distribution functon.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    show_legend : bool, default False
        If True, show legend.
    order : list or None
        If not None, must be a list of unique entries in `df[cat]`. The
        order of the list specifies the order of the colors. If None,
        the colors appear in the order in which they appeared in the
        inputted DataFrame.
    tooltips : list of 2-tuples
        Specification for tooltips.
    show_legend : bool, default False
        If True, show a legend.
    val_axis_type : 'linear' or 'log'
        Type of x-axis.
    ecdf_axis_type : 'linear' or 'log'
        Type of y-axis.
    kwargs
        Any kwargs to be passed to `p.circle()` when making the plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with jitter plot or box plot.
    if formal and tooltips is not None:
        raise RuntimeError('tooltips not possible for formal ECDFs.')
    """
    cols = _check_cat_input(data, cats, val, None, tooltips, palette, kwargs)

    if complementary:
        y = "__ECCDF"
        if y_axis_label is None:
            y_axis_label = "ECCDF"
    else:
        y = "__ECDF"
        if y_axis_label is None:
            y_axis_label = "ECDF"

    df = data.copy()
    df[y] = df[val].transform(_ecdf_y, complementary=complementary)
    cols += [y]
    source = _cat_source(df, cats, cols, None)
    _, _, color_factors = _get_cat_range(df, df.groupby(cats), order, None, False)

    if "color" not in kwargs:
        kwargs["color"] = bokeh.transform.factor_cmap(
            "cat", palette=palette, factors=color_factors
        )

    if show_legend:
        kwargs["legend"] = "__label"

    if p is None:
        p = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            x_axis_type=val_axis_type,
            y_axis_type=ecdf_axis_type,
            title=title,
            tooltips=tooltips,
        )

    p.circle(source=source, x=val, y=y, **kwargs)

    if show_legend:
        if complementary:
            p.legend.location = "top_right"
        else:
            p.legend.location = "bottom_right"

    return p


def colored_scatter(
    data=None,
    cats=None,
    x=None,
    y=None,
    p=None,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_height=300,
    plot_width=400,
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    order=None,
    show_legend=True,
    tooltips=None,
    x_axis_type="linear",
    y_axis_type="linear",
    **kwargs,
):
    """
    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hashables
        Name of column(s) to use as categorical variable (x-axis).
    x : hashable
        Name of column to use as x-axis.
    y : hashable
        Name of column to use as y-axis.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    show_legend : bool, default False
        If True, show legend.
    order : list or None
        If not None, must be a list of unique entries in `df[cat]`. The
        order of the list specifies the order of the colors. If None,
        the colors appear in the order in which they appeared in the
        inputted DataFrame.
    tooltips : list of 2-tuples
        Specification for tooltips.
    show_legend : bool, default False
        If True, show a legend.
    x_axis_type : 'linear' or 'log'
        Type of x-axis.
    y_axis_type : 'linear' or 'log'
        Type of y-axis.
    kwargs
        Any kwargs to be passed to `p.circle()` when making the plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with jitter plot or box plot.
    if formal and tooltips is not None:
        raise RuntimeError('tooltips not possible for formal ECDFs.')
    """
    cols = _check_cat_input(data, cats, x, None, tooltips, palette, kwargs)
    if y in data:
        cols += [y]
    else:
        raise RuntimeError(f"Column {y} not in inputted dataframe.")

    df = data.copy()
    source = _cat_source(df, cats, cols, None)
    _, _, color_factors = _get_cat_range(df, df.groupby(cats), order, None, False)

    if "color" not in kwargs:
        kwargs["color"] = bokeh.transform.factor_cmap(
            "cat", palette=palette, factors=color_factors
        )

    if show_legend:
        kwargs["legend"] = "__label"

    if p is None:
        p = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            x_axis_type=x_axis_type,
            y_axis_type=y_axis_type,
            title=title,
            tooltips=tooltips,
        )

    p.circle(source=source, x=x, y=y, **kwargs)

    return p


def boxwhisker(
    data,
    cats,
    val,
    p=None,
    horizontal=False,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_height=300,
    plot_width=400,
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    width=0.4,
    order=None,
    val_axis_type="linear",
    display_outliers=True,
    box_kwargs=None,
    whisker_kwargs=None,
    outlier_kwargs=None,
):
    """Deprecated, see `box`."""
    warnings.warn(
        "`boxwhisker` is deprecated and will be removed in future versions. Use `box`.",
        DeprecationWarning,
    )

    return box(
        data,
        cats,
        val,
        p,
        horizontal,
        x_axis_label,
        y_axis_label,
        title,
        plot_height,
        plot_width,
        palette,
        width,
        order,
        val_axis_type,
        display_outliers,
        box_kwargs,
        whisker_kwargs,
        outlier_kwargs,
    )


def predictive_ecdf(
    samples=None,
    name=None,
    diff=False,
    data=None,
    percentiles=[80, 60, 40, 20],
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_width=350,
    plot_height=225,
    color="blue",
    data_color="orange",
    data_line=True,
    data_size=2,
    x=None,
    discrete=False,
):
    """Plot a predictive ECDF from samples.

    Parameters
    ----------
    samples : StanFit4Model instance or Pandas DataFrame
        Samples generated from running a Stan calculation.
    name : str
        Name of the array to use in plotting the predictive ECDF. The
        array must be one-dimensional.
    diff : bool, default True
        If True, the ECDFs minus median of the predictive ECDF are
        plotted.
    data : 1D Numpy array, default None
        If not None, ECDF of measured data, overlaid with predictive
        ECDF.
    percentiles : list, default [80, 60, 40, 20]
        Percentiles for making colored envelopes for confidence
        intervals for the predictive ECDFs. Maximally four can be
        specified.
    x_axis_label : str, default None
        Label for the x-axis. If None, the value of `name` is used.
    y_axis_label : str, default None
        Label for the y-axis. If None, 'ECDF' is used if `diff` is
        False and 'ECDF difference' is used if `diff` is True. Ignored
        if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    color : str, default 'blue'
        One of ['green', 'blue', 'red', 'gray', 'purple', 'orange'].
        There are used to make the color scheme of shading of
        percentiles.
    data_color : str, default 'orange'
        String representing the color of the data to be plotted over the
        confidence interval envelopes.
    data_line : bool, default True
        If True, plot the ECDF of the data "formally," as a line.
        Otherwise plot it as dots.
    data_size : int, default 2
        Size of marker (if `data_line` if False) or thickness of line
        (if `data_line` is True) of plot of data.
    x : Numpy array, default None
        Points at which to evaluate the ECDF. If None, points are
        automatically generated based on the data range.
    discrete : bool, default False, TO BE IMPLEMENTED.
        If True, the samples take on discrete values. When this is the
        case, `x` may be determined unambiguously. This is not yet
        implemented, so `x` must be provided.

    Returns
    -------
    output : Bokeh figure
        Figure populated with glyphs describing range of values for the
        ECDF of the samples. The shading goes according to percentiles
        of samples of the ECDF, with the median ECDF plotted as line in
        the middle.
    """
    if discrete:
        raise NotImplementedError("`discrete` must be False.")

    if name is None:
        raise RuntimeError("`name` must be provided.")

    df = stan._fit_to_df(samples, diagnostics=False)

    if len(percentiles) > 4:
        raise RuntimeError("Can specify maximally four percentiles.")

    # Build ptiles
    ptiles = [pt for pt in percentiles if pt > 0]
    ptiles = (
        [50 - pt / 2 for pt in percentiles]
        + [50]
        + [50 + pt / 2 for pt in percentiles[::-1]]
    )
    ptiles_str = [str(pt) for pt in ptiles]

    if color not in ["green", "blue", "red", "gray", "purple", "orange", "betancourt"]:
        raise RuntimeError(
            "Only allowed colors are 'green', 'blue', 'red', 'gray', 'purple', 'orange'"
        )

    if x_axis_label is None:
        x_axis_label = str(name)
    if y_axis_label is None:
        if diff:
            y_axis_label = "ECDF difference"
        else:
            y_axis_label = "ECDF"

    sub_df = stan.extract_array(df, name)

    if "index_j" in sub_df:
        raise RuntimeError("Can only plot ECDF for one-dimensional data.")

    colors = {
        "blue": ["#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#084594"],
        "green": ["#a1d99b", "#74c476", "#41ab5d", "#238b45", "#005a32"],
        "red": ["#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#99000d"],
        "orange": ["#fdae6b", "#fd8d3c", "#f16913", "#d94801", "#8c2d04"],
        "purple": ["#bcbddc", "#9e9ac8", "#807dba", "#6a51a3", "#4a1486"],
        "gray": ["#bdbdbd", "#969696", "#737373", "#525252", "#252525"],
        "betancourt": [
            "#DCBCBC",
            "#C79999",
            "#B97C7C",
            "#A25050",
            "#8F2727",
            "#7C0000",
        ],
    }

    data_range = sub_df[name].max() - sub_df[name].min()
    if x is None:
        x = np.linspace(
            sub_df[name].min() - 0.05 * data_range,
            sub_df[name].max() + 0.05 * data_range,
            400,
        )

    df_ecdf = _ecdf_from_samples(sub_df, name, ptiles, x)

    if diff:
        for ptile in filter(lambda item: item != "50", ptiles_str):
            df_ecdf[ptile] -= df_ecdf["50"]
        df_ecdf["50"] = 0.0

    if data is not None and diff:
        df_ecdf_data_median = _ecdf_from_samples(sub_df, name, [50], np.sort(data))

    if diff and y_axis_label == "ECDF":
        y_axis_label = "ECDF diff. from median PPC"

    p = bokeh.plotting.figure(
        plot_width=plot_width,
        plot_height=plot_height,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        title=title,
    )

    for i, ptile in enumerate(ptiles_str[: len(ptiles_str) // 2]):
        fill_between(
            df_ecdf["x"],
            df_ecdf[ptile],
            df_ecdf["x"],
            df_ecdf[ptiles_str[-i - 1]],
            p=p,
            show_line=False,
            fill_color=colors[color][i],
        )

    # The median as a solid line
    p.line(df_ecdf["x"], df_ecdf["50"], line_width=2, color=colors[color][-1])

    # Overlay data set
    if data is not None:
        x_data, y_data = _ecdf_vals(data, formal=False)
        if diff:
            y_data -= df_ecdf_data_median["50"]
        if data_line:
            x_data, y_data = _to_formal(x_data, y_data)
            p.line(x_data, y_data, color=data_color, line_width=data_size)
        else:
            p.circle(x_data, y_data, color=data_color, size=data_size)

    return p


def predictive_regression(
    samples=None,
    name=None,
    diff=True,
    data_x=None,
    data_y=None,
    inds=None,
    percentiles=[80, 60, 40, 20],
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_width=350,
    plot_height=225,
    color="blue",
    data_color="orange",
    data_alpha=1,
    data_size=2,
):
    """Plot a predictive regression plot from samples.

    Parameters
    ----------
    samples : StanFit4Model instance or Pandas DataFrame
        Samples generated from running a Stan calculation.
    name : str
        Name of the array to use in plotting the predictive ECDF. The
        array must be one-dimensional.
    diff : bool, default True
        If True, the predictive y-values minus the median of the
        predictive y-values are plotted.
    data_x : 1D Numpy array, default None
        If not None, x-values for measured data. These are plotted as
        points over the predictive plot.
    data_y : 1D Numpy array, default None
        If not None, y-values for measured data. These are plotted as
        points over the predictive plot.
    inds : list, default None
        If given, a list of indices (one-origin, as per Stan) to use
        in the predictive plot. This is useful to only plot a portion
        of the results, particularly when they are repeated x-values.
    percentiles : list, default [80, 60, 40, 20]
        Percentiles for making colored envelopes for confidence
        intervals for the predictive ECDFs. Maximally four can be
        specified.
    x_axis_label : str, default None
        Label for the x-axis. If None, the value of `name` is used.
    y_axis_label : str, default None
        Label for the y-axis. If None, 'ECDF' is used if `diff` is
        False and 'ECDF difference' is used if `diff` is True. Ignored
        if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    color : str, default 'blue'
        One of ['green', 'blue', 'red', 'gray', 'purple', 'orange'].
        There are used to make the color scheme of shading of
        percentiles.
    data_color : str, default 'orange'
        String representing the color of the data to be plotted over the
        confidence interval envelopes.
    data_alpha : float, default 1
        Transparency for data.
    data_size : int, default 2
        Size of marker of plot of data.

    Returns
    -------
    output : Bokeh figure
        Figure populated with glyphs describing range of values for the
        the samples. The shading goes according to percentiles of
        samples, with the median plotted as line in the middle.
    """
    df = stan._fit_to_df(samples, diagnostics=False)

    if name is None:
        raise RuntimeError("`name` must be provided.")
    if data_x is None:
        raise RuntimeError("`data_x` must be provided.")

    if len(percentiles) > 4:
        raise RuntimeError("Can specify maximally four percentiles.")

    # Build ptiles
    ptiles = [pt for pt in percentiles if pt > 0]
    ptiles = (
        [50 - pt / 2 for pt in percentiles]
        + [50]
        + [50 + pt / 2 for pt in percentiles[::-1]]
    )
    ptiles = np.array(ptiles) / 100
    ptiles_str = [str(pt) for pt in ptiles]

    if color not in ["green", "blue", "red", "gray", "purple", "orange", "betancourt"]:
        raise RuntimeError(
            "Only allowed colors are 'green', 'blue', 'red', 'gray', 'purple', 'orange'"
        )

    sub_df = stan.extract_array(df, name)

    if inds is not None:
        sub_df = sub_df.loc[sub_df["index_1"].isin(inds), :]

    if "index_j" in sub_df:
        raise RuntimeError("Can only make plot for one-dimensional data.")

    colors = {
        "blue": ["#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#084594"],
        "green": ["#a1d99b", "#74c476", "#41ab5d", "#238b45", "#005a32"],
        "red": ["#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#99000d"],
        "orange": ["#fdae6b", "#fd8d3c", "#f16913", "#d94801", "#8c2d04"],
        "purple": ["#bcbddc", "#9e9ac8", "#807dba", "#6a51a3", "#4a1486"],
        "gray": ["#bdbdbd", "#969696", "#737373", "#525252", "#252525"],
        "betancourt": [
            "#DCBCBC",
            "#C79999",
            "#B97C7C",
            "#A25050",
            "#8F2727",
            "#7C0000",
        ],
    }

    df_ppc = (
        sub_df.groupby("index_1")[name]
        .quantile(ptiles)
        .unstack()
        .reset_index(drop=True)
    )
    df_ppc.columns = df_ppc.columns.astype(str)

    # Add data_x column to enable sorting
    df_ppc["__data_x"] = data_x
    if data_y is not None:
        df_ppc["__data_y"] = data_y
    df_ppc = df_ppc.sort_values(by="__data_x")

    p = bokeh.plotting.figure(
        plot_width=plot_width,
        plot_height=plot_height,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        title=title,
    )

    for i, ptile in enumerate(ptiles_str[: len(ptiles_str) // 2]):
        if diff:
            y1 = df_ppc[ptile] - df_ppc["0.5"]
            y2 = df_ppc[ptiles_str[-i - 1]] - df_ppc["0.5"]
        else:
            y1 = df_ppc[ptile]
            y2 = df_ppc[ptiles_str[-i - 1]]

        fill_between(
            x1=df_ppc["__data_x"],
            x2=df_ppc["__data_x"],
            y1=y1,
            y2=y2,
            p=p,
            show_line=False,
            fill_color=colors[color][i],
        )

    # The median as a solid line
    if diff:
        p.line(
            df_ppc["__data_x"],
            np.zeros_like(data_x),
            line_width=2,
            color=colors[color][-1],
        )
    else:
        p.line(df_ppc["__data_x"], df_ppc["0.5"], line_width=2, color=colors[color][-1])

    # Overlay data set
    if data_y is not None:
        if diff:
            p.circle(
                df_ppc["__data_x"],
                df_ppc["__data_y"] - df_ppc["0.5"],
                color=data_color,
                size=data_size,
                alpha=data_alpha,
            )
        else:
            p.circle(
                df_ppc["__data_x"],
                df_ppc["__data_y"],
                color=data_color,
                size=data_size,
                alpha=data_alpha,
            )

    return p


def sbc_rank_ecdf(
    sbc_output=None,
    parameters=None,
    diff=True,
    formal=False,
    ptile=99.0,
    bootstrap_envelope=False,
    n_bs_reps=None,
    show_envelope=True,
    p=None,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    plot_height=300,
    plot_width=450,
    color=None,
    palette=None,
    alpha=1,
    color_by_warning_code=False,
    fill_color="gray",
    fill_alpha=0.5,
    show_line=True,
    line_color="gray",
    show_legend=False,
    **kwargs,
):
    """Make a rank ECDF plot from simulation-based calibration.

    Parameters
    ----------
    sbc_output : DataFrame
        Output of bebi103.stan.sbc() containing results from an SBC
        calculation.
    parameters : list, default None
        List of parameters to include in the SBC rank ECDF plot. If
        None, use all parameters.
    diff : bool, default True
        If True, plot the ECDF minus the ECDF of a Uniform distribution.
        Otherwise, plot the ECDF of the rank statistic from SBC.
    formal : bool, default False
        If True, plot the ECDF "formally," that is connected by lines.
        Otherwise, plot with dots.
    ptile : float, default 99.9
        Which precentile to use as the envelope in the plot.
    bootstrap_envelope : bool, default False
        If True, use bootstrapping on the appropriate Uniform
        distribution to compute the envelope. Otherwise, use the
        Gaussian approximation for the envelope.
    n_bs_reps : bool, default None
        Number of bootstrap replicates to use when computing the
        envelope. If None, n_bs_reps is determined from the formula
        int(max(n, max(L+1, 100/(100-ptile))) * 100), where n is the
        number of simulations used in the SBC calculation.
    show_envelope : bool, default True
        If true, display the envelope encompassing the ptile percent
        confidence interval for the SBC ECDF.
    p : bokeh.plotting.Figure instance, defaul None
        Plot to which to add the SBC rank ECDF plot. If None, create a
        new figure.
    x_axis_label : str, default None
        Label for the x-axis. If None, 'rank statistic' is used. Ignored
        if `p` is not None.
    y_axis_label : str, default None
        Label for the y-axis. If None, 'ECDF' is used if `diff` is
        False and 'ECDF difference' is used if `diff` is True. Ignored
        if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    color : str, default None
        Specification of the color of the ECDF plot. All ECDFs are
        plotted with this color. If None, the ECDFs are colored by
        parameter or by diagnostics warning code if
        `color_by_warning_code` is True.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use if `color` is None. If a single
        string representing a hex color, all glyphs are colored with
        that color. Otherwise, a default is chosen based on the number
        of colors needed.
    alpha : float, default 1
        Opacity of the glyphs of the ECDFs.
    color_by_warning_code : bool, default False
        If True, color glyphs by diagnostics warning code instead of
        coloring the glyphs by parameter
    fill_color : str, default 'gray'
        Color of envelope as a hex string or named CSS color.
    fill_alpha : float, default 1.0
        Opacity of the envelope.
    show_line : bool, default True
        If True, show the lines on the edges of the envelope.
    line_color : str, default 'gray'
        Color of envelope line as a hex string or named CSS color.
    show_legend : bool, default False
        If True, show legend.
    kwargs : dict
        And kwargs to pass to the call to p.circle or p.line when making
        the ECDF plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        A plot containing the SBC plot.

    Notes
    -----
    .. You can see example SBC ECDF plots in Fig. 14 b and c in this
       paper: https://arxiv.org/abs/1804.06788
    """
    if sbc_output is None:
        raise RuntimeError("Argument `sbc_output` must be specified.")

    if x_axis_label is None:
        x_axis_label = "rank statistic"
    if y_axis_label is None:
        if diff:
            y_axis_label = "ECDF difference"
        else:
            y_axis_label = "ECDF"

    if formal and color_by_warning_code:
        raise RuntimeError("Cannot color by warning code for formal ECDFs.")
    if color is not None and color_by_warning_code:
        raise RuntimeError("`color` must be `None` if `color_by_warning_code` is True.")

    if parameters is None:
        parameters = list(sbc_output["parameter"].unique())
    elif type(parameters) not in [list, tuple]:
        parameters = [parameters]

    L = sbc_output["L"].iloc[0]
    df = sbc_output.loc[
        sbc_output["parameter"].isin(parameters),
        ["parameter", "rank_statistic", "warning_code"],
    ]
    n = (df["parameter"] == df["parameter"].unique()[0]).sum()

    if show_envelope:
        x, y_low, y_high = _sbc_rank_envelope(
            L,
            n,
            ptile=ptile,
            diff=diff,
            bootstrap=bootstrap_envelope,
            n_bs_reps=n_bs_reps,
        )
        p = fill_between(
            x1=x,
            x2=x,
            y1=y_high,
            y2=y_low,
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            fill_color=fill_color,
            fill_alpha=fill_alpha,
            show_line=show_line,
            line_color=line_color,
            p=p,
        )
    else:
        p = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
        )

    if formal:
        dfs = []
        for param in parameters:
            if diff:
                x_data, y_data = _ecdf_diff(
                    df.loc[df["parameter"] == param, "rank_statistic"], L, formal=True
                )
            else:
                x_data, y_data = _ecdf_vals(
                    df.loc[df["parameter"] == param, "rank_statistic"], formal=True
                )
            dfs.append(
                pd.DataFrame(
                    data=dict(rank_statistic=x_data, __ECDF=y_data, parameter=param)
                )
            )
        df = pd.concat(dfs, ignore_index=True)
    else:
        df["__ECDF"] = df.groupby("parameter")["rank_statistic"].transform(_ecdf_y)
        df["warning_code"] = df["warning_code"].astype(str)
        if diff:
            df["__ECDF"] -= (df["rank_statistic"] + 1) / L

    cat = "warning_code" if color_by_warning_code else "parameter"
    source = _cat_source(df, cat, ["__ECDF", "rank_statistic"], None)

    _, _, color_factors = _get_cat_range(df, df.groupby(cat), None, None, False)

    if palette is None:
        if len(df[cat].unique()) <= 8:
            palette = bokeh.palettes.Colorblind8
        elif len(df[cat].unique()) <= 10:
            palette = bokeh.palettes.d3.Category10
        elif len(df[cat].unique()) <= 20:
            palette = bokeh.palettes.d3.Category20
        else:
            palette = bokeh.palettes.Viridis256[::8]
    elif palette not in [list, tuple]:
        palette = [palette]

    if formal:
        if color is None:
            color = palette
        else:
            color = [color] * len(parameters)
    elif color is None:
        color = bokeh.transform.factor_cmap(
            "cat", palette=palette, factors=color_factors
        )

    if formal:
        for i, (param, g) in enumerate(df.groupby("parameter")):
            p.line(
                source=g,
                x="rank_statistic",
                y="__ECDF",
                color=color[i],
                legend=param if show_legend else None,
                **kwargs,
            )
    else:
        p.circle(
            source=source,
            x="rank_statistic",
            y="__ECDF",
            color=color,
            legend="__label" if show_legend else None,
            **kwargs,
        )

    return p


def parcoord_plot(
    samples=None,
    pars=None,
    plot_width=600,
    plot_height=175,
    x_axis_label=None,
    y_axis_label=None,
    inc_warmup=False,
    color_by_chain=False,
    color="black",
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    alpha=0.02,
    line_width=0.5,
    line_join="bevel",
    divergence_color="orange",
    divergence_alpha=1,
    divergence_line_width=1,
    xtick_label_orientation="horizontal",
    transformation=None,
    **kwargs,
):
    """
    Make a parallel coordinate plot of MCMC samples. The x-axis is the
    parameter name and the y-axis is the value of the parameter centered
    by its median and scaled by its 95 percentile range.

    Parameters
    ----------
    samples : StanFit4Model instance or Pandas DataFrame
        Result of MCMC sampling.
    pars : list
        List of variables as strings included in `samples` to construct
        the plot.
    plot_width : int, default 600
        Width of the trace plot for each variable in pixels.
    plot_height : int, default 175
        Height of the trace plot for each variable in pixels.
    x_axis_label : str or None, default None
        Label for x-axis in the plot.
    y_axis_label : str, default 'scaled value'
        Label for x-axis in the plot.
    inc_warmup : bool, default False
        If True, include warmup samples in the trace.
    color_by_chain : bool, default False
        If True, color the lines by chain.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    alpha : float, default 0.02
        Opacity of the traces.
    line_width : float, default 0.5
        Width of the lines in the trace plot.
    line_join : str, default 'bevel'
        Specification for `line_join` for lines in the plot.
    divergence_color : str, default 'orange'
        Color of samples that are divergent.
    divergence_alpha : float, default 1.0
        Opactive for samples that are divergent
    divergence_line_width : float, default 1
        Width of lines for divergent samples.
    xtick_label_orientation : str or float, default 'horizontal'
        Orientation of x tick labels. In some plots, horizontally
        labeled ticks will have label clashes, and this can fix that.
    transformation : function or list of functions, default None
        A transformation to apply to each set of samples. The function
        must take a single array as input and return an array as the
        same size. If None, nor transformation is done. If a list of
        functions, the transformations are applied to the respective
        variables in `pars`.
    kwargs
        Any kwargs to be passed to the `line()` function while making
        the plot.

    Returns
    -------
    output : Bokeh plot
        Parallel coordinates plot.

    """
    if type(samples) == pd.core.frame.DataFrame:
        df = samples
        if inc_warmup and "warmup" in df.columns:
            df = df.loc[df["warmup"] == 0, :]
    elif "pymc3" in str(type(samples)):
        raise NotImplementedError("Plots of PyMC3 traces not implemented.")
    elif "StanFit4Model" in str(type(samples)):
        df = stan.to_dataframe(samples, diagnostics=True, inc_warmup=inc_warmup)

    if pars is None:
        exclude = [
            "chain",
            "chain_idx",
            "warmup",
            "divergent__",
            "energy__",
            "treedepth__",
            "accept_stat__",
            "stepsize__",
            "n_leapfrog__",
        ]
        pars = [col for col in df.columns if col not in exclude]

    if type(pars) not in (list, tuple):
        raise RuntimeError("`pars` must be a list or tuple.")

    if type(transformation) not in (list, tuple):
        transformation = [transformation] * len(pars)
    for i, trans in enumerate(transformation):
        if trans is None:
            transformation[i] = lambda x: x

    if not color_by_chain:
        palette = [color] * len(palette)

    for col in pars:
        if col not in df.columns:
            raise RuntimeError("Column " + col + " not in the columns of DataFrame.")

    cols = pars + ["divergent__", "chain", "chain_idx"]
    df = df[cols].copy()
    df = df.melt(id_vars=["divergent__", "chain", "chain_idx"])

    p = bokeh.plotting.figure(
        plot_height=plot_height,
        plot_width=plot_width,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        x_range=bokeh.models.FactorRange(*list(df["variable"].unique())),
        toolbar_location="above",
    )

    # Plots for samples that were not divergent
    ys = np.array(
        [
            group["value"].values
            for _, group in df.loc[df["divergent__"] == 0].groupby(
                ["chain", "chain_idx"]
            )
        ]
    )
    if len(ys) > 0:
        for j in range(ys.shape[1]):
            ys[:, j] = transformation[j](ys[:, j])
        ys = [y for y in ys]
        xs = [list(df["variable"].unique())] * len(ys)

        p.multi_line(
            xs,
            ys,
            line_width=line_width,
            alpha=alpha,
            line_join=line_join,
            color=[palette[i % len(palette)] for i in range(len(ys))],
        )

    # Plots for samples that were divergent
    ys = np.array(
        [
            group["value"].values
            for _, group in df.loc[df["divergent__"] == 1].groupby(
                ["chain", "chain_idx"]
            )
        ]
    )
    if len(ys) > 0:
        for j in range(ys.shape[1]):
            ys[:, j] = transformation[j](ys[:, j])
        ys = [y for y in ys]
        xs = [list(df["variable"].unique())] * len(ys)

        p.multi_line(
            xs,
            ys,
            alpha=divergence_alpha,
            line_join=line_join,
            color=divergence_color,
            line_width=divergence_line_width,
        )

    p.xaxis.major_label_orientation = xtick_label_orientation

    return p


def trace_plot(
    samples=None,
    pars=None,
    labels=None,
    plot_width=600,
    plot_height=150,
    x_axis_label="step",
    inc_warmup=False,
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    alpha=0.02,
    line_width=0.5,
    line_join="bevel",
    **kwargs,
):
    """
    Make a trace plot of MCMC samples.

    Parameters
    ----------
    samples : StanFit4Model instance or Pandas DataFrame
        Result of MCMC sampling.
    pars : list
        List of variables as strings included in `samples` to construct
        the plot.
    labels : list, default None
        List of labels for the respective variables given in `pars`. If
        None, the variable names from `pars` are used.
    plot_width : int, default 600
        Width of the trace plot for each variable in pixels.
    plot_height : int, default 150
        Height of the trace plot for each variable in pixels.
    x_axis_label : str, default 'step'
        Label for x-axis in the trace plots.
    inc_warmup : bool, default False
        If True, include warmup samples in the trace.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    alpha : float, default 0.1
        Opacity of the traces.
    line_width : float, default 0.5
        Width of the lines in the trace plot.
    line_join : str, default 'bevel'
        Specification for `line_join` for lines in the plot.
    kwargs
        Any kwargs to be passed to the `line()` function while making
        the plot.

    Returns
    -------
    output : Bokeh gridplot
        Set of chain traces as a Bokeh gridplot.
    """
    if type(samples) == pd.core.frame.DataFrame:
        df = samples
        if inc_warmup and "warmup" in df.columns:
            df = df.loc[df["warmup"] == 0, :]
    elif "pymc3" in str(type(samples)):
        raise NotImplementedError("Plots of PyMC3 traces not implemented.")
    elif "StanFit4Model" in str(type(samples)):
        df = stan.to_dataframe(samples, inc_warmup=inc_warmup)

    if pars is None:
        raise RuntimeError("Must specify pars.")

    if type(pars) not in (list, tuple):
        raise RuntimeError("`pars` must be a list or tuple.")

    for col in pars:
        if col not in df.columns:
            raise RuntimeError("Column " + col + " not in the columns of DataFrame.")

    if labels is None:
        labels = pars
    elif len(labels) != len(pars):
        raise RuntimeError("len(pars) must equal len(labels)")

    plots = []
    grouped = df.groupby("chain")
    for i, (par, label) in enumerate(zip(pars, labels)):
        p = bokeh.plotting.figure(
            plot_width=plot_width,
            plot_height=plot_height,
            x_axis_label=x_axis_label,
            y_axis_label=label,
        )
        for chain, group in grouped:
            p.line(
                group["chain_idx"],
                group[par],
                line_width=line_width,
                line_join=line_join,
                color=palette[int(chain) - 1],
            )

        plots.append(p)

    if len(plots) == 1:
        return plots[0]

    # Link ranges
    for i, p in enumerate(plots[:-1]):
        plots[i].x_range = plots[-1].x_range

    return bokeh.layouts.gridplot(plots, ncols=1)


def contour_from_samples(
    x,
    y,
    bins_2d=50,
    levels=None,
    weights=None,
    smooth=1,
    extend_contour_domain=False,
    marker_kwargs={},
    line_kwargs={},
    **kwargs,
):
    raise NotImplementedError("Contour from samples not yet implemented.")


def corner(
    samples=None,
    pars=None,
    labels=None,
    datashade=False,
    plot_width=150,
    plot_ecdf=False,
    cmap="black",
    color_by_chain=False,
    palette=[
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    divergence_color="orange",
    alpha=0.02,
    single_param_color="black",
    bins=20,
    show_contours=False,
    contour_color="black",
    bins_2d=50,
    levels=None,
    weights=None,
    smooth=1,
    extend_contour_domain=False,
    plot_width_correction=50,
    plot_height_correction=40,
    xtick_label_orientation="horizontal",
):
    """
    Make a corner plot of MCMC results. Heavily influenced by the corner
    package by Dan Foreman-Mackey.

    Parameters
    ----------
    samples : StanFit4Model instance or Pandas DataFrame
        Result of MCMC sampling.
    pars : list
        List of variables as strings included in `samples` to construct
        corner plot.
    labels : list, default None
        List of labels for the respective variables given in `pars`. If
        None, the variable names from `pars` are used.
    datashade : bool, default False
        Whether or not to convert sampled points to a raster image using
        Datashader.
    plot_width : int, default 150
        Width of each plot in the corner plot in pixels. The height is
        computed from the width to make the plots roughly square.
    plot_ecdf : bool, default False
        If True, plot ECDFs of samples on the diagonal of the corner
        plot. If False, histograms are plotted.
    cmap : str, default 'black'
        Valid colormap string for DataShader or for coloring Bokeh
        glyphs.
    color_by_chain : bool, default False
        If True, color the glyphs by chain index.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair. Ignored is
        `color_by_chain` is False.
    divergence_color : str, default 'orange'
        Color to use for showing points where the sampler experienced a
        divergence.
    alpha : float, default 1.0
        Opacity of glyphs. Ignored if `datashade` is True.
    single_param_color : str, default 'black'
        Color of histogram or ECDF lines.
    bins : int, default 20
        Number of bins to use in constructing histograms. Ignored if
        `plot_ecdf` is True.
    show_contours : bool, default False
        If True, show contour plot on top of samples.
    contour_color : str, default 'black'
        Color of contour lines
    bins_2d : int, default 50
        Number of bins in each direction for binning 2D histograms when
        computing contours.
    levels : list of floats, default None
        Levels to use when constructing contours. By default, these are
        chosen according to this principle from Dan Foreman-Mackey:
        http://corner.readthedocs.io/en/latest/pages/sigmas.html
    weights : default None
        Value to pass as `weights` kwarg to np.histogram2d(), used in
        constructing contours.
    smooth : int or None, default 1
        Width of smoothing kernel for making contours.    plot_width_correction : int, default 50
        Correction for width of plot taking into account tick and axis
        labels.
    extend_contour_domain : bool, default False
        If True, extend the domain of the contours a little bit beyond
        the extend of the samples. This is done in the corner package,
        but I prefer not to do it.
    plot_width_correction : int, default 50
        Correction for width of plot taking into account tick and axis
        labels.
    plot_height_correction : int, default 40
        Correction for height of plot taking into account tick and axis
        labels.
    xtick_label_orientation : str or float, default 'horizontal'
        Orientation of x tick labels. In some plots, horizontally
        labeled ticks will have label clashes, and this can fix that.

    Returns
    -------
    output : Bokeh gridplot
        Corner plot as a Bokeh gridplot.
    """

    if pars is None:
        raise RuntimeError("Must specify pars.")

    if type(pars) not in (list, tuple):
        raise RuntimeError("`pars` must be a list or tuple.")

    if color_by_chain:
        if datashade:
            raise NotImplementedError(
                "Can only color by chain if `datashade` is False."
            )
        if cmap not in ["black", None]:
            warnings.warn("Ignoring cmap values to color by chain.")

    if divergence_color is None:
        divergence_color = cmap

    if type(samples) == pd.core.frame.DataFrame:
        df = samples
    elif "pymc3" in str(type(samples)):
        try:
            df = pm.trace_to_dataframe(samples)
        except:
            raise RuntimeError(
                "PyMC3 could not be imported. Check your installation."
                + " PyMC3 features will soon be deprecated."
            )
    elif "StanFit4Model" in str(type(samples)):
        df = stan.to_dataframe(samples, diagnostics=True)

    if color_by_chain:
        # Have to convert datatype to string to play nice with Bokeh
        df["chain"] = df["chain"].astype(str)

        factors = tuple(df["chain"].unique())
        cmap = bokeh.transform.factor_cmap("chain", palette=palette, factors=factors)

    # Add dummy divergent column if no divergence information is given
    if "divergent__" not in df.columns:
        df = df.copy()
        df["divergent__"] = 0

    if len(pars) > 6:
        raise RuntimeError("For space purposes, can show only six variables.")

    for col in pars:
        if col not in df.columns:
            raise RuntimeError("Column " + col + " not in the columns of DataFrame.")

    if labels is None:
        labels = pars
    elif len(labels) != len(pars):
        raise RuntimeError("len(pars) must equal len(labels)")

    if len(pars) == 1:
        x = pars[0]
        if plot_ecdf:
            if datashade:
                if plot_width == 150:
                    plot_height = 200
                    plot_width = 300
                else:
                    plot_width = 200
                    plot_height = 200
                x_range, _ = _data_range(df, pars[0], pars[0])
                p = bokeh.plotting.figure(
                    x_range=x_range,
                    y_range=[-0.02, 1.02],
                    plot_width=plot_width,
                    plot_height=plot_height,
                )
                x_ecdf, y_ecdf = _ecdf_vals(df[pars[0]], formal=True)
                df_ecdf = pd.DataFrame(data={pars[0]: x_ecdf, "ECDF": y_ecdf})
                _ = datashader.bokeh_ext.InteractiveImage(
                    p,
                    _create_line_image,
                    df=df_ecdf,
                    x=x,
                    y="ECDF",
                    cmap=single_param_color,
                )
            else:
                p = ecdf(
                    df[pars[0]],
                    formal=True,
                    line_width=2,
                    line_color=single_param_color,
                )
        else:
            p = histogram(
                df[pars[0]],
                bins=bins,
                density=True,
                line_width=2,
                color=single_param_color,
                x_axis_label=pars[0],
            )
        p.xaxis.major_label_orientation = xtick_label_orientation
        return p

    if not datashade:
        if len(df) > 10000:
            raise RuntimeError(
                "Cannot render more than 10,000 samples without DataShader."
            )
        elif len(df) > 5000:
            warnings.warn("Rendering so many points without DataShader is ill-advised.")

    plots = [[None for _ in range(len(pars))] for _ in range(len(pars))]

    for i, j in zip(*np.tril_indices(len(pars))):
        pw = plot_width
        ph = plot_width
        if j == 0:
            pw += plot_width_correction
        if i == len(pars) - 1:
            ph += plot_height_correction

        x = pars[j]
        if i != j:
            y = pars[i]
            x_range, y_range = _data_range(df, x, y)
            plots[i][j] = bokeh.plotting.figure(
                x_range=x_range, y_range=y_range, plot_width=pw, plot_height=ph
            )
            if datashade:
                _ = datashader.bokeh_ext.InteractiveImage(
                    plots[i][j], _create_points_image, df=df, x=x, y=y, cmap=cmap
                )
                plots[i][j].circle(
                    df.loc[df["divergent__"] == 1, x],
                    df.loc[df["divergent__"] == 1, y],
                    size=2,
                    color=divergence_color,
                )
            else:
                if divergence_color is None:
                    plots[i][j].circle(df[x], df[y], size=2, alpha=alpha, color=cmap)
                else:
                    plots[i][j].circle(
                        source=df.loc[df["divergent__"] == 0, [x, y, "chain"]],
                        x=x,
                        y=y,
                        size=2,
                        alpha=alpha,
                        color=cmap,
                    )
                    plots[i][j].circle(
                        df.loc[df["divergent__"] == 1, x],
                        df.loc[df["divergent__"] == 1, y],
                        size=2,
                        color=divergence_color,
                    )

            if show_contours:
                xs, ys = _get_contour_lines_from_samples(
                    df[x].values,
                    df[y].values,
                    bins=bins_2d,
                    smooth=smooth,
                    levels=levels,
                    weights=weights,
                    extend_domain=extend_contour_domain,
                )
                plots[i][j].multi_line(xs, ys, line_color=contour_color, line_width=2)
        else:
            if plot_ecdf:
                x_range, _ = _data_range(df, x, x)
                plots[i][i] = bokeh.plotting.figure(
                    x_range=x_range,
                    y_range=[-0.02, 1.02],
                    plot_width=pw,
                    plot_height=ph,
                )
                if datashade:
                    x_ecdf, y_ecdf = _ecdf_vals(df[x], formal=True)
                    df_ecdf = pd.DataFrame(data={x: x_ecdf, "ECDF": y_ecdf})
                    _ = datashader.bokeh_ext.InteractiveImage(
                        plots[i][i],
                        _create_line_image,
                        df=df_ecdf,
                        x=x,
                        y="ECDF",
                        cmap=single_param_color,
                    )
                else:
                    plots[i][i] = ecdf(
                        df[x],
                        p=plots[i][i],
                        formal=True,
                        line_width=2,
                        line_color=single_param_color,
                    )
            else:
                x_range, _ = _data_range(df, x, x)
                plots[i][i] = bokeh.plotting.figure(
                    x_range=x_range,
                    y_range=bokeh.models.DataRange1d(start=0.0),
                    plot_width=pw,
                    plot_height=ph,
                )
                f, e = np.histogram(df[x], bins=bins, density=True)
                e0 = np.empty(2 * len(e))
                f0 = np.empty(2 * len(e))
                e0[::2] = e
                e0[1::2] = e
                f0[0] = 0
                f0[-1] = 0
                f0[1:-1:2] = f
                f0[2:-1:2] = f

                plots[i][i].line(e0, f0, line_width=2, color=single_param_color)
        plots[i][j].xaxis.major_label_orientation = xtick_label_orientation

    # Link axis ranges
    for i in range(1, len(pars)):
        for j in range(i):
            plots[i][j].x_range = plots[j][j].x_range
            plots[i][j].y_range = plots[i][i].x_range

    # Label axes
    for i, label in enumerate(labels):
        plots[-1][i].xaxis.axis_label = label

    for i, label in enumerate(labels[1:]):
        plots[i + 1][0].yaxis.axis_label = label

    if plot_ecdf:
        plots[0][0].yaxis.axis_label = "ECDF"

    # Take off tick labels
    for i in range(len(pars) - 1):
        for j in range(i + 1):
            plots[i][j].xaxis.major_label_text_font_size = "0pt"

    if not plot_ecdf:
        plots[0][0].yaxis.major_label_text_font_size = "0pt"

    for i in range(1, len(pars)):
        for j in range(1, i + 1):
            plots[i][j].yaxis.major_label_text_font_size = "0pt"

    grid = bokeh.layouts.gridplot(plots, toolbar_location="left")

    return grid


def contour(
    X,
    Y,
    Z,
    levels=None,
    p=None,
    overlaid=False,
    cmap=None,
    overlay_grid=False,
    fill=False,
    fill_palette=None,
    fill_alpha=0.75,
    line_kwargs={},
    **kwargs,
):
    """
    Make a contour plot, possibly overlaid on an image.

    Parameters
    ----------
    X : 2D Numpy array
        Array of x-values, as would be produced using np.meshgrid()
    Y : 2D Numpy array
        Array of y-values, as would be produced using np.meshgrid()
    Z : 2D Numpy array
        Array of z-values.
    levels : array_like
        Levels to plot, ranging from 0 to 1. The contour around a given
        level contains that fraction of the total probability if the
        contour plot is for a 2D probability density function. By
        default, the levels are given by the one, two, three, and four
        sigma levels corresponding to a marginalized distribution from
        a 2D Gaussian distribution.
    p : bokeh plotting object, default None
        If not None, the contour are added to `p`. This option is not
        allowed if `overlaid` is True.
    overlaid : bool, default False
        If True, `Z` is displayed as an image and the contours are
        overlaid.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    line_color : str, defaults to Bokeh default
        Color, either named CSS color or hex, of contour lines.
    line_width : int, default 2
        Width of contour lines.
    cmap : str or list of hex colors, default None
        If `im` is an intensity image, `cmap` is a mapping of
        intensity to color. If None, default is 256-level Viridis.
        If `im` is a color image, then `cmap` can either be
        'rgb' or 'cmy' (default), for RGB or CMY merge of channels.
    overlay_grid : bool, default False
        If True, faintly overlay the grid on top of image. Ignored if
        overlaid is False.
    line_kwargs : dict, default {}
        Keyword arguments passed to `p.multiline()` for rendering the
        contour.

    Returns
    -------
    output : Bokeh plotting object
        Plot populated with contours, possible with an image.
    """
    if len(X.shape) != 2 or Y.shape != X.shape or Z.shape != X.shape:
        raise RuntimeError("All arrays must be 2D and of same shape.")

    if overlaid and p is not None:
        raise RuntimeError("Cannot specify `p` if showing image.")

    # Set defaults
    x_axis_label = kwargs.pop("x_axis_label", "x")
    y_axis_label = kwargs.pop("y_axis_label", "y")
    frame_height = kwargs.pop("frame_height", 300)
    frame_width = kwargs.pop("frame_width", 300)
    title = kwargs.pop("title", None)

    if "line_color" not in line_kwargs:
        if overlaid:
            line_kwargs["line_color"] = "white"
        else:
            line_kwargs["line_color"] = "black"

    line_width = line_kwargs.pop("line_width", 2)

    if p is None:
        if overlaid:
            p = image.imshow(
                Z,
                cmap=cmap,
                frame_height=frame_height,
                frame_width=frame_width,
                x_axis_label=x_axis_label,
                y_axis_label=y_axis_label,
                title=title,
                x_range=[X.min(), X.max()],
                y_range=[Y.min(), Y.max()],
                no_ticks=False,
                flip=False,
                return_im=False,
            )
        else:
            p = bokeh.plotting.figure(
                frame_width=frame_width,
                frame_height=frame_height,
                x_axis_label=x_axis_label,
                y_axis_label=y_axis_label,
                title=title,
                **kwargs,
            )

    # Set default levels
    if levels is None:
        levels = 1.0 - np.exp(-np.arange(0.5, 2.1, 0.5) ** 2 / 2)

    # Compute contour lines
    if fill or line_width:
        xs, ys = _contour_lines(X, Y, Z, levels)

    # Make fills. This is currently not supported
    if fill:
        raise NotImplementedError("Filled contours are not yet implemented.")
        if fill_palette is None:
            if len(levels) <= 6:
                fill_palette = bokeh.palettes.Greys[len(levels) + 3][1:-1]
            elif len(levels) <= 10:
                fill_palette = bokeh.palettes.Viridis[len(levels) + 1]
            else:
                raise RuntimeError(
                    "Can only have maximally 10 levels with filled contours"
                    + " unless user specifies `fill_palette`."
                )
        elif len(fill_palette) != len(levels) + 1:
            raise RuntimeError(
                "`fill_palette` must have 1 more entry" + " than `levels`"
            )

        p.patch(
            xs[-1], ys[-1], color=fill_palette[0], alpha=fill_alpha, line_color=None
        )
        for i in range(1, len(levels)):
            x_p = np.concatenate((xs[-1 - i], xs[-i][::-1]))
            y_p = np.concatenate((ys[-1 - i], ys[-i][::-1]))
            p.patch(x_p, y_p, color=fill_palette[i], alpha=fill_alpha, line_color=None)

        p.background_fill_color = fill_palette[-1]

    # Populate the plot with contour lines
    p.multi_line(xs, ys, line_width=line_width, **line_kwargs)

    if overlay_grid and overlaid:
        p.grid.level = "overlay"
        p.grid.grid_line_alpha = 0.2

    return p


def ds_line_plot(
    df,
    x,
    y,
    cmap="#1f77b4",
    plot_height=300,
    plot_width=500,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    margin=0.02,
):
    """
    Make a datashaded line plot.

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame containing the data
    x : Valid column name of Pandas DataFrame
        Column containing the x-data.
    y : Valid column name of Pandas DataFrame
        Column containing the y-data.
    cmap : str, default '#1f77b4'
        Valid colormap string for DataShader and for coloring Bokeh
        glyphs.
    plot_height : int, default 300
        Height of plot, in pixels.
    plot_width : int, default 500
        Width of plot, in pixels.
    x_axis_label : str, default None
        Label for the x-axis.
    y_axis_label : str, default None
        Label for the y-axis.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    margin : float, default 0.02
        Margin, in units of `plot_width` or `plot_height`, to leave
        around the plotted line.

    Returns
    -------
    output : datashader.bokeh_ext.InteractiveImage
        Interactive image of plot. Note that you should *not* use
        bokeh.io.show() to view the image. For most use cases, you
        should just call this function without variable assignment.
    """

    if x_axis_label is None:
        if type(x) == str:
            x_axis_label = x
        else:
            x_axis_label = "x"

    if y_axis_label is None:
        if type(y) == str:
            y_axis_label = y
        else:
            y_axis_label = "y"

    x_range, y_range = _data_range(df, x, y, margin=margin)
    p = bokeh.plotting.figure(
        plot_height=plot_height,
        plot_width=plot_width,
        x_range=x_range,
        y_range=y_range,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        title=title,
    )
    return datashader.bokeh_ext.InteractiveImage(
        p, _create_line_image, df=df, x=x, y=y, cmap=cmap
    )


def ds_point_plot(
    df,
    x,
    y,
    cmap="#1f77b4",
    plot_height=300,
    plot_width=500,
    x_axis_label=None,
    y_axis_label=None,
    title=None,
    margin=0.02,
):
    """
    Make a datashaded point plot.

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame containing the data
    x : Valid column name of Pandas DataFrame
        Column containing the x-data.
    y : Valid column name of Pandas DataFrame
        Column containing the y-data.
    cmap : str, default '#1f77b4'
        Valid colormap string for DataShader and for coloring Bokeh
        glyphs.
    plot_height : int, default 300
        Height of plot, in pixels.
    plot_width : int, default 500
        Width of plot, in pixels.
    x_axis_label : str, default None
        Label for the x-axis.
    y_axis_label : str, default None
        Label for the y-axis.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    margin : float, default 0.02
        Margin, in units of `plot_width` or `plot_height`, to leave
        around the plotted line.

    Returns
    -------
    output : datashader.bokeh_ext.InteractiveImage
        Interactive image of plot. Note that you should *not* use
        bokeh.io.show() to view the image. For most use cases, you
        should just call this function without variable assignment.
    """

    if x_axis_label is None:
        if type(x) == str:
            x_axis_label = x
        else:
            x_axis_label = "x"

    if y_axis_label is None:
        if type(y) == str:
            y_axis_label = y
        else:
            y_axis_label = "y"

    x_range, y_range = _data_range(df, x, y, margin=margin)
    p = bokeh.plotting.figure(
        plot_height=plot_height,
        plot_width=plot_width,
        x_range=x_range,
        y_range=y_range,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        title=title,
    )
    return datashader.bokeh_ext.InteractiveImage(
        p, _create_points_image, df=df, x=x, y=y, cmap=cmap
    )


def distribution_plot_app(
    x_min=None,
    x_max=None,
    scipy_dist=None,
    transform=None,
    custom_pdf=None,
    custom_pmf=None,
    custom_cdf=None,
    params=None,
    n=400,
    plot_height=200,
    plot_width=300,
    x_axis_label="x",
    title=None,
):
    """
    Build interactive Bokeh app displaying a univariate
    probability distribution.

    Parameters
    ----------
    x_min : float
        Minimum value that the random variable can take in plots.
    x_max : float
        Maximum value that the random variable can take in plots.
    scipy_dist : scipy.stats distribution
        Distribution to use in plotting.
    transform : function or None (default)
        A function of call signature `transform(*params)` that takes
        a tuple or Numpy array of parameters and returns a tuple of
        the same length with transformed parameters.
    custom_pdf : function
        Function with call signature f(x, *params) that computes the
        PDF of a distribution.
    custom_pmf : function
        Function with call signature f(x, *params) that computes the
        PDF of a distribution.
    custom_cdf : function
        Function with call signature F(x, *params) that computes the
        CDF of a distribution.
    params : list of dicts
        A list of parameter specifications. Each entry in the list gives
        specifications for a parameter of the distribution stored as a
        dictionary. Each dictionary must have the following keys.
            name : str, name of the parameter
            start : float, starting point of slider for parameter (the
                smallest allowed value of the parameter)
            end : float, ending point of slider for parameter (the
                largest allowed value of the parameter)
            value : float, the value of the parameter that the slider
                takes initially. Must be between start and end.
            step : float, the step size for the slider
    n : int, default 400
        Number of points to use in making plots of PDF and CDF for
        continuous distributions. This should be large enough to give
        smooth plots.
    plot_height : int, default 200
        Height of plots.
    plot_width : int, default 300
        Width of plots.
    x_axis_label : str, default 'x'
        Label for x-axis.
    title : str, default None
        Title to be displayed above the PDF or PMF plot.

    Returns
    -------
    output : Bokeh app
        An app to visualize the PDF/PMF and CDF. It can be displayed
        with bokeh.io.show(). If it is displayed in a notebook, the
        notebook_url kwarg should be specified.
    """
    if None in [x_min, x_max]:
        raise RuntimeError("`x_min` and `x_max` must be specified.")

    if scipy_dist is None:
        fun_c = custom_cdf
        if (custom_pdf is None and custom_pmf is None) or custom_cdf is None:
            raise RuntimeError(
                "For custom distributions, both PDF/PMF and" + " CDF must be specified."
            )
        if custom_pdf is not None and custom_pmf is not None:
            raise RuntimeError("Can only specify custom PMF or PDF.")
        if custom_pmf is None:
            discrete = False
            fun_p = custom_pdf
        else:
            discrete = True
            fun_p = custom_pmf
    elif custom_pdf is not None or custom_pmf is not None or custom_cdf is not None:
        raise RuntimeError("Can only specify either custom or scipy distribution.")
    else:
        fun_c = scipy_dist.cdf
        if hasattr(scipy_dist, "pmf"):
            discrete = True
            fun_p = scipy_dist.pmf
        else:
            discrete = False
            fun_p = scipy_dist.pdf

    if discrete:
        p_y_axis_label = "PMF"
    else:
        p_y_axis_label = "PDF"

    if params is None:
        raise RuntimeError("`params` must be specified.")

    def _plot_app(doc):
        p_p = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label=p_y_axis_label,
            title=title,
        )
        p_c = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label="CDF",
        )

        # Link the axes
        p_c.x_range = p_p.x_range

        # Make sure CDF y_range is zero to one
        p_c.y_range = bokeh.models.Range1d(-0.05, 1.05)

        # Make array of parameter values
        param_vals = np.array([param["value"] for param in params])
        if transform is not None:
            param_vals = transform(*param_vals)

        # Set up data for plot
        if discrete:
            x = np.arange(int(np.ceil(x_min)), int(np.floor(x_max)) + 1)
            x_size = x[-1] - x[0]
            x_c = np.empty(2 * len(x))
            x_c[::2] = x
            x_c[1::2] = x
            x_c = np.concatenate(
                (
                    (max(x[0] - 0.05 * x_size, x[0] - 0.95),),
                    x_c,
                    (min(x[-1] + 0.05 * x_size, x[-1] + 0.95),),
                )
            )
            x_cdf = np.concatenate(((x_c[0],), x))
        else:
            x = np.linspace(x_min, x_max, n)
            x_c = x_cdf = x

        # Compute PDF and CDF
        y_p = fun_p(x, *param_vals)
        y_c = fun_c(x_cdf, *param_vals)
        if discrete:
            y_c_plot = np.empty_like(x_c)
            y_c_plot[::2] = y_c
            y_c_plot[1::2] = y_c
            y_c = y_c_plot

        # Set up data sources
        source_p = bokeh.models.ColumnDataSource(data={"x": x, "y_p": y_p})
        source_c = bokeh.models.ColumnDataSource(data={"x": x_c, "y_c": y_c})

        # Plot PDF and CDF
        p_c.line("x", "y_c", source=source_c, line_width=2)
        if discrete:
            p_p.circle("x", "y_p", source=source_p, size=5)
            p_p.segment(x0="x", x1="x", y0=0, y1="y_p", source=source_p, line_width=2)
        else:
            p_p.line("x", "y_p", source=source_p, line_width=2)

        def _callback(attr, old, new):
            param_vals = tuple([slider.value for slider in sliders])
            if transform is not None:
                param_vals = transform(*param_vals)

            # Compute PDF and CDF
            source_p.data["y_p"] = fun_p(x, *param_vals)
            y_c = fun_c(x_cdf, *param_vals)
            if discrete:
                y_c_plot = np.empty_like(x_c)
                y_c_plot[::2] = y_c
                y_c_plot[1::2] = y_c
                y_c = y_c_plot
            source_c.data["y_c"] = y_c

        sliders = [
            bokeh.models.Slider(
                start=param["start"],
                end=param["end"],
                value=param["value"],
                step=param["step"],
                title=param["name"],
            )
            for param in params
        ]
        for slider in sliders:
            slider.on_change("value", _callback)

        # Add the plot to the app
        widgets = bokeh.layouts.widgetbox(sliders)
        grid = bokeh.layouts.gridplot([p_p, p_c], ncols=2)
        doc.add_root(bokeh.layouts.column(widgets, grid))

    handler = bokeh.application.handlers.FunctionHandler(_plot_app)
    return bokeh.application.Application(handler)


def mpl_cmap_to_color_mapper(cmap):
    """
    Convert a Matplotlib colormap to a bokeh.models.LinearColorMapper
    instance.

    Parameters
    ----------
    cmap : str
        A string giving the name of the color map.

    Returns
    -------
    output : bokeh.models.LinearColorMapper instance
        A linear color_mapper with 25 gradations.

    Notes
    -----
    .. See https://matplotlib.org/examples/color/colormaps_reference.html
       for available Matplotlib colormaps.
    """
    cm = mpl_get_cmap(cmap)
    palette = [rgb_frac_to_hex(cm(i)[:3]) for i in range(256)]
    return bokeh.models.LinearColorMapper(palette=palette)


def adjust_range(element, buffer=0.05):
    """
    Adjust soft ranges of dimensions of HoloViews element.

    Parameters
    ----------
    element : holoviews element
        Element which will have the `soft_range` of each kdim and vdim
        recomputed to give a buffer around the glyphs.
    buffer : float, default 0.05
        Buffer, as a fraction of the whole data range, to give around
        data.

    Returns
    -------
    output : holoviews element
        Inputted HoloViews element with updated soft_ranges for its
        dimensions.
    """
    # This only works with DataFrames
    if type(element.data) != pd.core.frame.DataFrame:
        raise RuntimeError("Can only adjust range if data is Pandas DataFrame.")

    # Adjust ranges of kdims
    for i, dim in enumerate(element.kdims):
        if element.data[dim.name].dtype in [float, int]:
            data_range = (element.data[dim.name].min(), element.data[dim.name].max())
            if data_range[1] - data_range[0] > 0:
                buff = buffer * (data_range[1] - data_range[0])
                element.kdims[i].soft_range = (
                    data_range[0] - buff,
                    data_range[1] + buff,
                )

    # Adjust ranges of vdims
    for i, dim in enumerate(element.vdims):
        if element.data[dim.name].dtype in [float, int]:
            data_range = (element.data[dim.name].min(), element.data[dim.name].max())
            if data_range[1] - data_range[0] > 0:
                buff = buffer * (data_range[1] - data_range[0])
                element.vdims[i].soft_range = (
                    data_range[0] - buff,
                    data_range[1] + buff,
                )

    return element


def _ecdf_vals(data, formal=False, complementary=False):
    """Get x, y, values of an ECDF for plotting.
    Parameters
    ----------
    data : ndarray
        One dimensional Numpy array with data.
    formal : bool, default False
        If True, generate x and y values for formal ECDF (staircase). If
        False, generate x and y values for ECDF as dots.
    complementary : bool
        If True, return values for ECCDF.

    Returns
    -------
    x : ndarray
        x-values for plot
    y : ndarray
        y-values for plot
    """
    x = np.sort(data)
    y = np.arange(1, len(data) + 1) / len(data)

    if formal:
        x, y = _to_formal(x, y)
        if complementary:
            y = 1 - y
    elif complementary:
        y = 1 - y + 1 / len(y)

    return x, y


@numba.jit(nopython=True)
def _ecdf_arbitrary_points(data, x):
    """Give the value of an ECDF at arbitrary points x."""
    y = np.arange(len(data) + 1) / len(data)
    return y[np.searchsorted(np.sort(data), x, side="right")]


def _ecdf_from_samples(df, name, ptiles, x):
    """Compute ECDFs and percentiles from samples."""
    df_ecdf = pd.DataFrame()
    df_ecdf_vals = pd.DataFrame()
    grouped = df.groupby(["chain", "chain_idx"])
    for i, g in grouped:
        df_ecdf_vals[i] = _ecdf_arbitrary_points(g[name].values, x)

    for ptile in ptiles:
        df_ecdf[str(ptile)] = df_ecdf_vals.quantile(
            ptile / 100, axis=1, interpolation="higher"
        )
    df_ecdf["x"] = x

    return df_ecdf


def _to_formal(x, y):
    """Convert to formal ECDF."""
    # Set up output arrays
    x_formal = np.empty(2 * len(x))
    y_formal = np.empty(2 * len(x))

    # y-values for steps
    y_formal[0] = 0
    y_formal[1::2] = y
    y_formal[2::2] = y[:-1]

    # x- values for steps
    x_formal[::2] = x
    x_formal[1::2] = x

    return x_formal, y_formal


@numba.jit(nopython=True)
def _y_ecdf(data, x):
    y = np.arange(len(data) + 1) / len(data)
    return y[np.searchsorted(np.sort(data), x, side="right")]


@numba.jit(nopython=True)
def _draw_ecdf_bootstrap(L, n, n_bs_reps=100000):
    x = np.arange(L + 1)
    ys = np.empty((n_bs_reps, len(x)))
    for i in range(n_bs_reps):
        draws = np.random.randint(0, L + 1, size=n)
        ys[i, :] = _y_ecdf(draws, x)
    return ys


def _sbc_rank_envelope(L, n, ptile=95, diff=True, bootstrap=False, n_bs_reps=None):
    x = np.arange(L + 1)
    y = st.randint.cdf(x, 0, L + 1)
    std = np.sqrt(y * (1 - y) / n)

    if bootstrap:
        if n_bs_reps is None:
            n_bs_reps = int(max(n, max(L + 1, 100 / (100 - ptile))) * 100)
        ys = _draw_ecdf_bootstrap(L, n, n_bs_reps=n_bs_reps)
        y_low, y_high = np.percentile(ys, [50 - ptile / 2, 50 + ptile / 2], axis=0)
    else:
        y_low = np.concatenate(
            (st.norm.ppf((50 - ptile / 2) / 100, y[:-1], std[:-1]), (1.0,))
        )
        y_high = np.concatenate(
            (st.norm.ppf((50 + ptile / 2) / 100, y[:-1], std[:-1]), (1.0,))
        )

    # Ensure that ends are appropriate
    y_low = np.maximum(0, y_low)
    y_high = np.minimum(1, y_high)

    # Make "formal" stepped ECDFs
    _, y_low = _to_formal(x, y_low)
    x_formal, y_high = _to_formal(x, y_high)

    if diff:
        _, y = _to_formal(x, y)
        y_low -= y
        y_high -= y

    return x_formal, y_low, y_high


def _ecdf_diff(data, L, formal=False):
    x, y = _ecdf_vals(data)
    y_uniform = (x + 1) / L
    if formal:
        x, y = _to_formal(x, y)
        _, y_uniform = _to_formal(np.arange(len(data)), y_uniform)
    y -= y_uniform

    return x, y


def _get_cat_range(df, grouped, order, color_column, horizontal):
    if order is None:
        if isinstance(list(grouped.groups.keys())[0], tuple):
            factors = tuple(
                [tuple([str(k) for k in key]) for key in grouped.groups.keys()]
            )
        else:
            factors = tuple([str(key) for key in grouped.groups.keys()])
    else:
        if type(order[0]) in [list, tuple]:
            factors = tuple([tuple([str(k) for k in key]) for key in order])
        else:
            factors = tuple([str(entry) for entry in order])

    if horizontal:
        cat_range = bokeh.models.FactorRange(*(factors[::-1]))
    else:
        cat_range = bokeh.models.FactorRange(*factors)

    if color_column is None:
        color_factors = factors
    else:
        color_factors = tuple(sorted(list(df[color_column].unique().astype(str))))

    return cat_range, factors, color_factors


def _cat_figure(
    df,
    grouped,
    plot_height,
    plot_width,
    x_axis_label,
    y_axis_label,
    title,
    order,
    color_column,
    tooltips,
    horizontal,
    val_axis_type,
):
    fig_kwargs = dict(
        plot_height=plot_height,
        plot_width=plot_width,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        title=title,
        tooltips=tooltips,
    )

    cat_range, factors, color_factors = _get_cat_range(
        df, grouped, order, color_column, horizontal
    )

    if horizontal:
        fig_kwargs["y_range"] = cat_range
        fig_kwargs["x_axis_type"] = val_axis_type
    else:
        fig_kwargs["x_range"] = cat_range
        fig_kwargs["y_axis_type"] = val_axis_type

    return bokeh.plotting.figure(**fig_kwargs), factors, color_factors


def _cat_source(df, cats, cols, color_column):
    if type(cats) in [list, tuple]:
        cat_source = list(zip(*tuple([df[cat].astype(str) for cat in cats])))
        labels = [", ".join(cat) for cat in cat_source]
    else:
        cat_source = list(df[cats].astype(str).values)
        labels = cat_source

    if type(cols) in [list, tuple, pd.core.indexes.base.Index]:
        source_dict = {col: list(df[col].values) for col in cols}
    else:
        source_dict = {cols: list(df[cols].values)}

    source_dict["cat"] = cat_source
    if color_column in [None, "cat"]:
        source_dict["__label"] = labels
    else:
        source_dict["__label"] = list(df[color_column].astype(str).values)
        source_dict[color_column] = list(df[color_column].astype(str).values)

    return bokeh.models.ColumnDataSource(source_dict)


def _tooltip_cols(tooltips):
    if tooltips is None:
        return []
    if type(tooltips) not in [list, tuple]:
        raise RuntimeError("`tooltips` must be a list or tuple of two-tuples.")

    cols = []
    for tip in tooltips:
        if type(tip) not in [list, tuple] or len(tip) != 2:
            raise RuntimeError("Invalid tooltip.")
        if tip[1][0] == "@":
            if tip[1][1] == "{":
                cols.append(tip[1][2 : tip[1].find("}")])
            elif "{" in tip[1]:
                cols.append(tip[1][1 : tip[1].find("{")])
            else:
                cols.append(tip[1][1:])

    return cols


def _cols_to_keep(cats, val, color_column, tooltips):
    cols = _tooltip_cols(tooltips)
    cols += [val]

    if type(cats) in [list, tuple]:
        cols += list(cats)
    else:
        cols += [cats]

    if color_column is not None:
        cols += [color_column]

    return list(set(cols))


def _check_cat_input(df, cats, val, color_column, tooltips, palette, kwargs):
    if df is None:
        raise RuntimeError("`df` argument must be provided.")
    if cats is None:
        raise RuntimeError("`cats` argument must be provided.")
    if val is None:
        raise RuntimeError("`val` argument must be provided.")

    if type(palette) not in [list, tuple]:
        raise RuntimeError("`palette` must be a list or tuple.")

    if val not in df.columns:
        raise RuntimeError(f"{val} is not a column in the inputted data frame")

    cats_array = type(cats) in [list, tuple]

    if cats_array:
        for cat in cats:
            if cat not in df.columns:
                raise RuntimeError(f"{cat} is not a column in the inputted data frame")
    else:
        if cats not in df.columns:
            raise RuntimeError(f"{cats} is not a column in the inputted data frame")

    if color_column is not None and color_column not in df.columns:
        raise RuntimeError(f"{color_column} is not a column in the inputted data frame")

    cols = _cols_to_keep(cats, val, color_column, tooltips)

    for col in cols:
        if col not in df.columns:
            raise RuntimeError(f"{col} is not a column in the inputted data frame")

    bad_kwargs = ["x", "y", "source", "cat", "legend"]
    if kwargs is not None and any([key in kwargs for key in bad_kwargs]):
        raise RuntimeError(", ".join(bad_kwargs) + " are not allowed kwargs.")

    if val == "cat":
        raise RuntimeError("`'cat'` cannot be used as `val`.")

    if val == "__label" or (cats == "__label" or (cats_array and "__label" in cats)):
        raise RuntimeError("'__label' cannot be used for `val` or `cats`.")

    return cols


def _outliers(data):
    bottom, middle, top = np.percentile(data, [25, 50, 75])
    iqr = top - bottom
    outliers = data[(data > top + 1.5 * iqr) | (data < bottom - 1.5 * iqr)]
    return outliers


def _box_and_whisker(data):
    middle = data.median()
    bottom = data.quantile(0.25)
    top = data.quantile(0.75)
    iqr = top - bottom
    top_whisker = data[data <= top + 1.5 * iqr].max()
    bottom_whisker = data[data >= bottom - 1.5 * iqr].min()
    return pd.Series(
        {
            "middle": middle,
            "bottom": bottom,
            "top": top,
            "top_whisker": top_whisker,
            "bottom_whisker": bottom_whisker,
        }
    )


def _box_source(df, cats, val, cols):
    """Construct a data frame for making box plot."""

    # Need to reset index for use in slicing outliers
    df_source = df.reset_index(drop=True)

    if type(cats) in [list, tuple]:
        level = list(range(len(cats)))
    else:
        level = 0

    if cats is None:
        grouped = df_source
    else:
        grouped = df_source.groupby(cats)

    # Data frame for boxes and whiskers
    df_box = grouped[val].apply(_box_and_whisker).unstack().reset_index()
    source_box = _cat_source(
        df_box, cats, ["middle", "bottom", "top", "top_whisker", "bottom_whisker"], None
    )

    # Data frame for outliers
    df_outliers = grouped[val].apply(_outliers).reset_index(level=level)
    df_outliers[cols] = df_source.loc[df_outliers.index, cols]
    source_outliers = _cat_source(df_outliers, cats, cols, None)

    return source_box, source_outliers


def _ecdf_y(data, complementary=False):
    """Give y-values of an ECDF for an unsorted column in a data frame.

    Parameters
    ----------
    data : Pandas Series
        Series (or column of a DataFrame) from which to generate ECDF
        values
    complementary : bool, default False
        If True, give the ECCDF values.

    Returns
    -------
    output : Pandas Series
        Corresponding y-values for an ECDF when plotted with dots.

    Notes
    -----
    .. This only works for plotting an ECDF with points, not for formal
       ECDFs
    """
    if complementary:
        return 1 - data.rank(method="first") / len(data) + 1 / len(data)
    else:
        return data.rank(method="first") / len(data)


def _point_ecdf_source(data, val, cats, cols, complementary, colored):
    """DataFrame for making point-wise ECDF."""
    df = data.copy()

    if complementary:
        col = "__ECCDF"
    else:
        col = "__ECDF"

    if cats is None or colored:
        df[col] = _ecdf_y(df[val], complementary)
    else:
        df[col] = df.groupby(cats)[val].transform(_ecdf_y, complementary)

    cols += [col]

    return _cat_source(df, cats, cols, None)


def _ecdf_collection_dots(
    df, val, cats, cols, complementary, order, palette, show_legend, y, p, **kwargs
):
    _, _, color_factors = _get_cat_range(df, df.groupby(cats), order, None, False)

    source = _point_ecdf_source(df, val, cats, cols, complementary, False)

    if "color" not in kwargs:
        kwargs["color"] = bokeh.transform.factor_cmap(
            "cat", palette=palette, factors=color_factors
        )

    if show_legend:
        kwargs["legend"] = "__label"

    p.circle(source=source, x=val, y=y, **kwargs)

    return p


def _ecdf_collection_formal(
    df, val, cats, complementary, order, palette, show_legend, p, **kwargs
):
    grouped = df.groupby(cats)

    color_not_in_kwargs = "color" not in kwargs

    if order is None:
        order = list(grouped.groups.keys())
    grouped_iterator = [
        (order_val, grouped.get_group(order_val)) for order_val in order
    ]

    for i, g in enumerate(grouped_iterator):
        if show_legend:
            if type(g[0]) == tuple:
                legend = ", ".join([str(c) for c in g[0]])
            else:
                legend = str(g[0])
        else:
            legend = None

        if color_not_in_kwargs:
            kwargs["color"] = palette[i % len(palette)]

        ecdf(
            g[1][val],
            formal=True,
            p=p,
            legend=legend,
            complementary=complementary,
            **kwargs,
        )

    return p


def _display_clicks(div, attributes=[], style="float:left;clear:left;font_size=0.5pt"):
    """Build a suitable CustomJS to display the current event
    in the div model."""
    return bokeh.models.CustomJS(
        args=dict(div=div),
        code="""
        var attrs = %s; var args = [];
        for (var i=0; i<attrs.length; i++ ) {
            args.push(Number(cb_obj[attrs[i]]).toFixed(4));
        }
        var line = "<span style=%r>[" + args.join(", ") + "], </span>\\n";
        var text = div.text.concat(line);
        var lines = text.split("\\n")
        if ( lines.length > 35 ) { lines.shift(); }
        div.text = lines.join("\\n");
    """
        % (attributes, style),
    )


def _data_range(df, x, y, margin=0.02):
    x_range = df[x].max() - df[x].min()
    y_range = df[y].max() - df[y].min()
    return (
        [df[x].min() - x_range * margin, df[x].max() + x_range * margin],
        [df[y].min() - y_range * margin, df[y].max() + y_range * margin],
    )


def _create_points_image(x_range, y_range, w, h, df, x, y, cmap):
    cvs = ds.Canvas(
        x_range=x_range, y_range=y_range, plot_height=int(h), plot_width=int(w)
    )
    agg = cvs.points(df, x, y, agg=ds.reductions.count())
    return ds.transfer_functions.dynspread(
        ds.transfer_functions.shade(agg, cmap=cmap, how="linear")
    )


def _create_line_image(x_range, y_range, w, h, df, x, y, cmap=None):
    cvs = ds.Canvas(
        x_range=x_range, y_range=y_range, plot_height=int(h), plot_width=int(w)
    )
    agg = cvs.line(df, x, y)
    return ds.transfer_functions.dynspread(ds.transfer_functions.shade(agg, cmap=cmap))


def _contour_lines(X, Y, Z, levels):
    """
    Generate lines for contour plot.
    """
    # Compute the density levels.
    Zflat = Z.flatten()
    inds = np.argsort(Zflat)[::-1]
    Zflat = Zflat[inds]
    sm = np.cumsum(Zflat)
    sm /= sm[-1]
    V = np.empty(len(levels))
    for i, v0 in enumerate(levels):
        try:
            V[i] = Zflat[sm <= v0][-1]
        except:
            V[i] = Zflat[0]
    V.sort()
    m = np.diff(V) == 0

    while np.any(m):
        V[np.where(m)[0][0]] *= 1.0 - 1e-4
        m = np.diff(V) == 0
    V.sort()

    # Make contours
    c = matplotlib._contour.QuadContourGenerator(X, Y, Z, None, True, 0)
    xs = []
    ys = []
    for level in V:
        paths = c.create_contour(level)
        for line in paths:
            xs.append(line[:, 0])
            ys.append(line[:, 1])

    return xs, ys


def _get_contour_lines_from_samples(
    x, y, smooth=1, levels=None, bins=50, weights=None, extend_domain=False
):
    """
    Get lines for contour overlay.

    Based on code from emcee by Dan Forman-Mackey.
    """
    data_range = [[x.min(), x.max()], [y.min(), y.max()]]

    # Choose the default "sigma" contour levels.
    if levels is None:
        levels = 1.0 - np.exp(-0.5 * np.arange(0.5, 2.1, 0.5) ** 2)

    # We'll make the 2D histogram to directly estimate the density.
    try:
        H, X, Y = np.histogram2d(
            x.flatten(),
            y.flatten(),
            bins=bins,
            range=list(map(np.sort, data_range)),
            weights=weights,
        )
    except ValueError:
        raise ValueError(
            "It looks like at least one of your sample columns "
            "have no dynamic data_range. You could try using the "
            "'data_range' argument."
        )

    if smooth is not None:
        H = scipy.ndimage.gaussian_filter(H, smooth)

    # Compute the bin centers.
    X1, Y1 = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1])

    # Extend the array for the sake of the contours at the plot edges.
    if extend_domain:
        H2 = H.min() + np.zeros((H.shape[0] + 4, H.shape[1] + 4))
        H2[2:-2, 2:-2] = H
        H2[2:-2, 1] = H[:, 0]
        H2[2:-2, -2] = H[:, -1]
        H2[1, 2:-2] = H[0]
        H2[-2, 2:-2] = H[-1]
        H2[1, 1] = H[0, 0]
        H2[1, -2] = H[0, -1]
        H2[-2, 1] = H[-1, 0]
        H2[-2, -2] = H[-1, -1]
        X2 = np.concatenate(
            [
                X1[0] + np.array([-2, -1]) * np.diff(X1[:2]),
                X1,
                X1[-1] + np.array([1, 2]) * np.diff(X1[-2:]),
            ]
        )
        Y2 = np.concatenate(
            [
                Y1[0] + np.array([-2, -1]) * np.diff(Y1[:2]),
                Y1,
                Y1[-1] + np.array([1, 2]) * np.diff(Y1[-2:]),
            ]
        )
        X2, Y2 = np.meshgrid(X2, Y2)
    else:
        X2, Y2 = np.meshgrid(X1, Y1)
        H2 = H

    return _contour_lines(X2, Y2, H2.transpose(), levels)
