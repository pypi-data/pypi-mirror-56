#!/usr/bin/python

# vim: set expandtab ts=4 sw=4:

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colorbar as cb
from mpl_toolkits.axes_grid1 import Grid
from matplotlib import patches

__all__ = []


def root_plot(rts, ax=None, figargs=dict(), plotargs=dict()):
    """
    Plot a set of roots (complex numbers).

    :param rts: Roots to plot
    :param ax: Optional Axes on which to place plot.

    :returns: Axes object on which plot was drawn
    """

    if 'figsize' not in figargs:
        figargs['figsize'] = (6, 6)

    if ax is None:
        plt.figure(*figargs)
        ax = plt.subplot(111)

    # Unit Circle
    y = np.sin(np.linspace(0, 2*np.pi, 128))
    x = np.cos(np.linspace(0, 2*np.pi, 128))
    ax.plot(x, y, 'k')
    # Inner circles
    ax.plot(.75*x, .75*y, 'k--', linewidth=.2)
    ax.plot(.5*x, .5*y, 'k--', linewidth=.2)
    ax.plot(.25*x, .25*y, 'k--', linewidth=.2)
    ax.grid(True)

    # Arrow annotation
    ax.plot(1.15*x[8:25], 1.15*y[8:25], 'k')
    ax.arrow(1.15*x[23], 1.15*y[23], x[24]-x[23], y[24]-y[23],
             head_width=.05, color='k')

    # Add poles
    print(plotargs)
    ax.plot(rts.real, rts.imag, 'k+', **plotargs)

    # Labels
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlim(-1.2, 1.2)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.annotate('Frequency', xy=(.56, 1.02))

    return ax


__all__.append('root_plot')


def plot_diagonal(freq_vect, metric, F=None, title=None, ax=None):

    if F is None:
        F = plt.figure(figsize=(6, 6))

    if ax is None:
        ax = F.subplots(1)

    for ii in range(metric.shape[0]):
        ax.plot(freq_vect, metric[ii, ii, :, 0])

    if title is not None:
        ax.set_title(title)

    ax.set_xlabel('Frequency')
    ax.grid(True)


def plot_metric_summary(freq_vect, metric, ind=0, F=None, title=None):

    F = plt.figure(figsize=(12, 6))
    ax = F.subplots(1, 2)

    plot_diagonal(freq_vect, metric, F=F, ax=ax[0])
    ylimits = ax[0].get_ylim()
    ax[0].vlines(freq_vect[ind], ylimits[0], ylimits[1])

    s = metric[:, :, ind, 0] - np.diag(np.diag(metric[:, :, ind, 0]))
    im = ax[1].imshow(np.abs(s))
    F.colorbar(im)


def plot_vector(metric, x_vect, y_vect=None, x_label=None, y_label=None,
                title=None, labels=None, line_labels=None, F=None,
                cmap=plt.cm.jet, triangle=None, diag=False,
                thresh=None, two_tail_thresh=False, font_size=10,
                use_latex=False):
    """
    Function for plotting frequency domain connectivity at a single time-point.

    :params metric: matrix containing connectivity values [nsignals x signals x
                    frequencies x participants] in which the first dimension
                    refers to source nodes and the second dimension refers to
                    target nodes
    :type metric: ndarray

    :params x_vect: vector of frequencies to label the x axis
    :type x_vect: 1d ndarray

    :params y_vect: y_vect: vector containing the values for the y-axis
    :type y_vect: 1d ndarray [optional]

    :param x_label: label for the x axis
    :type x_label: string [optional]

    :param y_label: label for the y axis
    :type y_label: string [optional]

    :param title: title for the figure
    :type title: string [optional]

    :param labels: list of node labels for columns and vectors
    :type labels: list

    :param line_labels: list of labels for each separate line (participant
                        dimension in metric)
    :type line_labels: list

    :param F: handle of existing figure to plot within
    :type F: figurehandle [optional]

    :param triangle: string to indicate whether only the 'upper' or 'lower'
                     triangle of the matrix should be plotted
    :type triangle: string [optional]

    :param diag: flag to indicate whether the diagonal elements should
                 be plotted
    :type diag: bool [optional]

    :param thresh: matrix containing thesholds to be plotted alongside
                   connectivity values [nsignals x nsignals x frequencies]
    :type thresh: ndarray [optional]

    :param two_tailed_thresh: flag to indicate whether both signs (+/-) of the
                              threshold should be plotted
    :type two_tailed_thresh: bool [optional]

    :param font_size: override the default font size
    :type font_size: int [optional]
    """

    # Set up plotting parameters
    matplotlib.rcParams.update({'font.size': font_size})
    if use_latex:
        matplotlib.rcParams['text.latex.preamble'].append(r'\usepackage{amsmath}')
        plt.rc('font', **{'family': 'sans-serif',
                          'sans-serif': ['Helvetica']})
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

    if metric.ndim > 3 and metric.shape[3] > 1:
        # We want to plot each line separately
        ppt = metric.shape[3]
    elif metric.ndim > 3 and metric.shape[3] == 1:
        ppt = 1
    elif metric.ndim == 3:
        ppt = 1
        metric = metric[..., None]

    # Sanity check axis labels
    x_vect = x_vect.squeeze()
    if y_vect is not None:
        y_vect = y_vect.squeeze()
    nbSignals = metric.shape[0]

    # If we don't have any labels, make some up
    if labels is None:
        labels = [chr(65 + (x % 26)) for x in range(nbSignals)]

    if line_labels is None:
        line_labels = [chr(97 + (x % 26)) for x in range(ppt)]

    # Make figure if we don't have one
    if F is None:
        F = plt.figure(figsize=(8.3, 5.8))
        plt.axis('off')

    # Get label indices
    x_label_idx = []
    y_label_idx = []
    for g in range(nbSignals * nbSignals):
        i = int(g / nbSignals)
        j = int(g % nbSignals)

        if triangle == 'upper':
            if i == 0:
                x_label_idx.append(g)
            if i == j-1:
                y_label_idx.append(g)

        elif triangle == 'lower':
            if j == 0:
                x_label_idx.append(g)
            if i == j+1:
                y_label_idx.append(g)
        else:
            if i == 0:
                x_label_idx.append(g)
            if j == 0:
                y_label_idx.append(g)

    # Write labels to plot
    ax_pad = 0.25

    # Make grid with appropriate amount of subplots
    grid = Grid(F, 111,
                nrows_ncols=(nbSignals, nbSignals),
                axes_pad=ax_pad,
                share_all=True)

    # Plot up the matrix
    for g in range(nbSignals*nbSignals):
        i = int(g / nbSignals)
        j = int(g % nbSignals)

        if triangle == 'lower' and i < j:
            grid[g].set_visible(False)
            continue
        elif triangle == 'upper' and i > j:
            grid[g].set_visible(False)
            continue

        if diag is False and i == j:
            grid[g].set_visible(False)
            [grid[g].axis[k].set_visible(False) for k in grid[g].axis.keys()]

        if thresh is not None:
            grid[g].plot(x_vect, thresh[i, j, :], 'k--')
            if two_tail_thresh:
                grid[g].plot(x_vect, -thresh[i, j, :], 'k--')

        if ppt > 1 or thresh is not None:
            for p in range(ppt):
                grid[g].plot(x_vect, metric[i, j, :, p],
                             label=line_labels[p])
                grid[g].set_xlim(x_vect[0], x_vect[-1])

        else:
            grid[g].fill_between(x_vect, metric[i, j, :, 0],
                                 0, facecolor='black',
                                 alpha=.9)

        if y_vect is not None:
            grid[g].set_ylim(y_vect[0], y_vect[-1])

        grid[g].grid()

    if line_labels is not None and ppt > 1:
        grid[nbSignals-1].legend(bbox_to_anchor=(1.05, 1), loc=2)

    ymin, ymax = grid[g].get_ylim()

    grid.axes_llc.set_xlim(x_vect[0], x_vect[-1])

    if triangle == 'lower':
        x_x_pos = x_vect[2]
        x_y_pos = ymax*1.2
        y_x_pos = -x_vect[-2]
        y_y_pos = 1.2
        # Plot the labels
        for g in x_label_idx:
            i = int(g / nbSignals)
            j = int(g % nbSignals)

            grid[g].text(y_x_pos, y_y_pos, r'$\mathbf{%s}$' % (labels[i]))

        for g in y_label_idx:
            i = int(g / nbSignals)
            j = int(g % nbSignals)

            grid[g].text(x_x_pos, x_y_pos,
                         r'$\mathbf{%s \rightarrow}$' % (labels[i-1]))
    elif triangle == 'upper':
        x_x_pos = x_vect[:-2].mean()
        x_y_pos = ymax*1.2
        y_x_pos = -x_vect[-2]
        y_y_pos = .5
        # Plot the labels
        for g in x_label_idx:
            i = int(g / nbSignals)
            j = int(g % nbSignals)

            grid[g].text(x_x_pos, x_y_pos,
                         r'$\mathbf{%s \rightarrow}$' % (labels[j]))

        for g in y_label_idx:
            i = int(g / nbSignals)
            j = int(g % nbSignals)

            grid[g].text(y_x_pos, y_y_pos,
                         r'$\mathbf{%s}$' % (labels[i]))
    else:
        x_x_pos = x_vect[2]
        x_y_pos = ymax*1.2
        y_x_pos = -x_vect[:-2].mean() * 1.7
        y_y_pos = ymax * .5
        # Plot the labels
        for g in x_label_idx:
            i = int(g / nbSignals)
            j = int(g % nbSignals)

            grid[g].text(x_x_pos, x_y_pos,
                         r'$\mathbf{%s \rightarrow}$' % (labels[j]))

        for g in y_label_idx:
            i = int(g / nbSignals)
            j = int(g % nbSignals)

            grid[g].text(y_x_pos, y_y_pos,
                         r'$\mathbf{%s}$' % (labels[i]))

    for g in range(nbSignals * nbSignals):
        [k.set_visible(True) for k in grid[g].texts]

    if x_label is not None:
        grid[nbSignals*(nbSignals-1)].set_xlabel(x_label)
    if y_label is not None:
        grid[nbSignals*(nbSignals-1)].set_ylabel(y_label)

    if title is not None:
        plt.suptitle(title)

    return F


def plot_matrix(metric, x_vect, y_vect, x_label=None, y_label=None,
                z_vect=None, title=None, labels=None, F=None,
                cmap=plt.cm.jet, font_size=8, use_latex=False, diag=True):

    """
    Function for plotting frequency domain connectivity over many time points

    :param metric: matrix containing connectivity values [nsignals x signals x
                   frequencies x participants] in which the first dimension
                   refers to source nodes and the second dimension refers to
                   target nodes
    :type metric: ndarray

    :param x_vect: vector of frequencies to label the x axis
    :type x_vect: 1d array

    :param y_vect: vector containing the values for the y-axis
    :type y_vect: 1d array [optional]

    :param z_vect: vector containing values for the colour scale
    :type z_vect: 1d array [optional]

    :param x_label: label for the x axis
    :type x_label: string [optional]

    :param y_label: label for the y axis
    :type y_label: string [optional]

    :param title: title for the figure
    :type title: string [optional]

    :param labels: list of node labels for columns and vectors
    :type labels: list

    :param F: handle of existing figure to plot within
    :type F: figurehandle [optional]

    :param cmap: matplotlib.cm.<colormapname> to use for
                 colourscale (redundant for plot vector??)
    :type cmap: matplotlib colormap [optional]

    :param font_size: override the default font size
    :type font_size: int [optional]

    """
    # Set up plotting parameters
    matplotlib.rcParams.update({'font.size': font_size})
    if use_latex:
        matplotlib.rcParams['text.latex.preamble'].append(r'\usepackage{amsmath}')
        plt.rc('font', **{'family': 'sans-serif',
                          'sans-serif': ['Helvetica']})
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

    # Sanity check axis labels
    x_vect = x_vect.squeeze()
    y_vect = y_vect.squeeze()
    nbSignals = metric.shape[0]

    # Set up colour scale
    if z_vect is None:
        cbounds = np.linspace(0, 1)
        col = np.linspace(0, 1)
    else:
        cbounds = z_vect
        col = z_vect

    # Make figure if we don't have one
    if F is None:
        F = plt.figure(figsize=(8.3, 5.8))
        plt.axis('off')

    # Write labels to plot
    step = 1. / nbSignals

    # Horizontal
    for i in range(len(labels)):
        plt.text((step*i)+.05, 1.01,
                 r'$\mathbf{%s \rightarrow}$' % (labels[i]),
                 fontsize=font_size,
                 rotation='horizontal')

    # Vertical
    for i in range(len(labels), 0, -1):
        plt.text(-.08, (step*i)-step/10 - .06,
                 r'$\mathbf{%s}$' % (labels[-i]),
                 fontsize=font_size,
                 rotation='vertical')

    # Make grid with appropriate amount of subplots
    grid = Grid(F, 111,
                nrows_ncols=(nbSignals, nbSignals),
                axes_pad=0.1,
                share_all=True)

    # Plot up the matrix
    for g in range(nbSignals*nbSignals):
        i = int(g / nbSignals)
        j = int(g % nbSignals)

        if i != j or diag is True:
            grid[g].contourf(x_vect, y_vect, metric[i, j, :, :],
                             np.linspace(cbounds[0], cbounds[-1], 10),
                             cmap=cmap)
            grid[g].vlines(0, y_vect[0], y_vect[-1])
        else:
            grid[g].set_visible(False)

    # Set labels
    grid.axes_llc.set_ylim(y_vect[0], y_vect[-1])
    n_ticks = len(grid[g].xaxis.get_majorticklocs())
    grid.axes_llc.set_xticklabels(np.round(np.linspace(x_vect[0], x_vect[-1],
                                                       n_ticks), 2))
    # grid.axes_llc.set_xticks(x_vect[::4])

    # Set colourbar
    ax = F.add_axes([.92, .12, .02, .7])
    if col[-1] < 2:
        # Round to nearest .1
        rcol = np.array(.1 * np.round(col/.1))
    elif col[-1] < 10:
        # Round to nearest 1
        rcol = np.array(1 * np.round(col/1)).astype(int)
    else:
        # Round to nearest 10
        rcol = np.array(10 * np.round(col/10)).astype(int)
    cb.ColorbarBase(ax, boundaries=cbounds, cmap=cmap, ticks=rcol)

    if title is not None:
        plt.suptitle(title)

    if x_label is not None:
        grid[nbSignals*(nbSignals-1)].set_xlabel(x_label)
    if y_label is not None:
        grid[nbSignals*(nbSignals-1)].set_ylabel(y_label)

    return F


def plot_netmat(data, colors=None, cnames=None, xtick_pos=None, ytick_pos=None,
                labels=None, ax=None, hregions='top', vregions='right', showgrid=True,
                **kwargs):
    """
    data: (nrois, nrois) 2D numpy array of netmat data to plot
    cnames: None or list of len(nrois).  List of colour names for each region
    colors: None or dictionary mapping colour names to matplotlib-usable colours.
            If not provided, name from cnames will be used.
    labels: None or a list of region labels for the X and Y axes
    ax: matplotlib Axes on which to draw.  A new figure will be created if this
        is not supplied

    Optional arguments:
      xtick_pos: Positions of X ROI division lines in netmat
      ytick_pos: Positions of Y ROI division lines in netmat
      hbar_offset: Offset of ROI bar in Y co-ordinates (default: 2)
      vbar_offset: Offset of ROI bar in X co-ordinates (default: 2)
      bar_gap: Gap to put between ROI bars (default: 0.1)
      bar_thickness: Thickness of the ROI bar (default: 2.5)
      label_fontsize: Font size to use for region labels (default: 5)
      hregions: Location to place horizontal coloured bars indicating regions of ROIs.
                One of 'top', 'bottom', 'off'.  Defaults to 'top'
      vregions: Location to place vertical coloured bars indicating regions of ROIs.
                One of 'left', 'right', 'off'.  Defaults to 'right'

    Any additional keyword arguments will be passed into pcolormesh
    """

    num_rois = data.shape[0]

    hbar_offset = kwargs.pop('hbar_offset', 2)
    vbar_offset = kwargs.pop('vbar_offset', 2)
    bar_gap = kwargs.pop('bar_gap', 0.1)
    bar_thickness = kwargs.pop('bar_thickness', 2.5)
    label_fontsize = kwargs.pop('label_fontsize', 5)

    # Parse the h and vregions parameters
    if hregions not in ['top', 'bottom', 'off', True, False]:
        raise Exception("hregions must be one of top, bottom, off")

    if hregions is True:
        hregions = 'top'
    if hregions is False:
        hregions = 'off'

    if vregions not in ['left', 'right', 'off', True, False]:
        raise Exception("vregions must be one of left, right, off")

    if vregions is True:
        vregions = 'top'
    if vregions is False:
        vregions = 'off'

    # Ensure that we have a set of axes
    if ax is None:
        plt.figure()
        ax = plt.subplot(1, 1, 1)

    # See comment below regarding pcolormesh vs imshow
    ax.pcolormesh(data, **kwargs)
    plt.axis('scaled')

    if cnames is not None:
        start = None

        for k in range(num_rois):
            thiscname = cnames[k]

            if start is None:
                start = k
                curcname = thiscname

            if k != (num_rois - 1):
                nextcname = cnames[k+1]

            if (k == (num_rois - 1)) or (nextcname != curcname):
                # Need to draw and reset start point
                if colors is not None:
                    color = colors[curcname]
                else:
                    color = curcname

                width = bar_thickness

                if vregions == 'right':
                    ll_x = num_rois + vbar_offset
                else:
                    ll_x = -vbar_offset

                if start == 0:
                    ll_y = start
                    height = k - start + 1 - bar_gap
                elif k == (num_rois - 1):
                    ll_y = start + bar_gap
                    height = k - start + 1
                else:
                    ll_y = start + bar_gap
                    height = k - start + 1 - bar_gap - bar_gap

                if vregions != 'off':
                    rect = patches.Rectangle((ll_x, ll_y), width, height,
                                             linewidth=0, facecolor=color,
                                             clip_on=False)
                    ax.add_patch(rect)

                height = bar_thickness

                if hregions == 'top':
                    ll_y = num_rois + hbar_offset
                else:
                    ll_y = -hbar_offset

                if start == 0:
                    ll_x = start
                    width = k - start + 1 - bar_gap
                elif k == (num_rois - 1):
                    ll_x = start + bar_gap
                    width = k - start + 1
                else:
                    ll_x = start + bar_gap
                    width = k - start + 1 - bar_gap - bar_gap

                if hregions != 'off':
                    rect = patches.Rectangle((ll_x, ll_y), width, height,
                                             linewidth=0, facecolor=color,
                                             clip_on=False)
                    ax.add_patch(rect)

                start = None

    if xtick_pos is None:
        ax.set_xticks([])
    else:
        ax.set_xticks(xtick_pos)

    if ytick_pos is None:
        ax.set_yticks([])
    else:
        ax.set_yticks(ytick_pos)

    # Remove the major labels either way
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    if labels is not None:
        ax.set_xticks([x + 0.5 for x in range(num_rois)], minor=True)
        ax.set_yticks([x + 0.5 for x in range(num_rois)], minor=True)
        ax.set_xticklabels(labels, minor=True, fontsize=label_fontsize, rotation=-90)
        ax.set_yticklabels(labels, minor=True, fontsize=label_fontsize)

    plt.xlim(0, num_rois)
    plt.ylim(0, num_rois)

    if showgrid:
        plt.grid(True, color='w', lw=1)

    return ax


__all__.append('plot_netmat')
