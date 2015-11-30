from itertools import cycle
import contextlib

"""
red,blue,green,purple,orange,yellow,brown,pink,gray = (
    brewer2mpl.get_map('Set1', 'Qualitative', 9).hex_colors)
black = '#000000'
collist = [red,blue,green,purple,orange,brown,pink,gray,yellow,black]
collist
"""

color_list = colors10 = red, blue, green, purple, orange, brown, ppink, grey, yellow, black = (
    '#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00',
    '#A65628', '#F781BF', '#999999', '#FFFF33', '#000000')
color_dict = dict(red=red, blue=blue, green=green, purple=purple, orange=orange,
               brown=brown, pink=ppink, grey=grey, yellow=yellow, black=black)

colors8 = ['#1B9E77', '#D95F02', '#7570B3', '#E7298A',
         '#66A61E', '#E6AB02', '#A6761D', '#666666']

# Set 3
colors12 = ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072',
          '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
          '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F']


def color_cycle():
    """
    Cycle through the 10-color list.
    """
    return cycle(color_list)


def new_cmaps():
    """
    Defines a set of new colormaps for matplotlib, and registers them.
    
    The `grormute` colormap is particularly helpful.
    """
    import matplotlib.colors as mcolors
    import matplotlib.cm as mcm
    cmaps = {
        'roygbiv': [(1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 1.0),
                    (0.0, 0.0, 1.0)],
        'PkOrBu': [(1, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 1), (0, 0, 1)],
        'rainbow2': [(0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
        'redblue': [(0, 0, 1), (1, 0, 1), (1, 0, 0)],
        'grayred': ['#999999', '#E41A1C'],
        'blackgrayred': ['#000000', '#999999', '#E41A1C'],
        'blackred': ['#000000', '#E41A1C'],
        'bgro': ['#000000', '#999999', '#E41A1C', '#FF7F00'],
        'rbmute': ['#E41A1C', '#984EA3', '#377EB8'],
        # 'redblue2':['#b2182b', '#2166ac'],
        'rwb': ['#ca0020', '#f4a582', '#FFFFFF', '#92c5de', '#0571b0'],
        'redblue2': ['#d7191c', '#fdae61', '#abdda4', '#2b83ba'],
        # green, blue,  purple, red, orange
        'grormute': ['#4DAF4A', '#377EB8', '#984EA3', '#E41A1C', '#FF7F00'],

        # green, blue,  purple, red, orange, yellow, green
        'grorgr': ['#4DAF4A', '#377EB8', '#984EA3', '#E41A1C', '#FF7F00', '#FFFF33', '#4DAF4A'],
    }
    for name, colorlist in cmaps.items():
        cmap = mcolors.LinearSegmentedColormap.from_list(name, colorlist)
        mcm.register_cmap(name, cmap)

        rname = name + '_r'
        cmap = mcolors.LinearSegmentedColormap.from_list(rname, list(reversed(colorlist)))
        mcm.register_cmap(rname, cmap)

    return set(cmaps.keys())


def diverging_colors(N, cmap=None):
    """
    Make a list of N colors from a color map.
    """
    import matplotlib.cm as mcm
    sm = mcm.ScalarMappable(cmap=cmap)
    return sm.to_rgba(range(N))


def to_colors(scalars, vmin=None, vmax=None, cmap=None):
    """Converts a set of scalars to colors, using the specified colormap."""
    if vmin is None:
        vmin = min(scalars)
    if vmax is None:
        vmax = max(scalars)
    import matplotlib as mpl
    sm = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin, vmax), cmap=cmap)
    return [sm.to_rgba(s) for s in scalars]


def eczip(*args, start=0, step=1, **kw):
    """A combination of enumerate and zip-with-diverging-colors:

    eczip(list1, list2) = [(0, color0, list1[0], list2[0]), (1, color1, list1[1], list2[1]), ...]
    
    Useful for iterating over lists to plot:
    
    >>> for n, color, data in eczip(datasets):
    ...     plt.plot(data, color=color, label='Plot %s' % n)
    """

    args = [list(a) for a in args]
    N = min([len(a) for a in args])

    return zip(range(start, (N + start)*step, step),
        diverging_colors(N, **kw), *args)


@contextlib.contextmanager
def twincolored(ax=None, col1=red, col2=blue):
    """
    A context manager for twin axes, with colored labels and ticks.

    Example:

    with twincolored() as (ax1, ax2, col1, col2):
        ax1.plot([1,2,3],[0,2,1]. color=col1)
        ax2.plot([1,2,3],[4,6,5]. color=col2)
    """
    import matplotlib.pyplot as plt
    if ax is None:
        ax = plt.gca()
    ax2 = ax.twinx()
    ax.yaxis.label.set_color(col1)
    ax2.yaxis.label.set_color(col2)
    try:
        yield ax, ax2, col1, col2
    finally:
        for tl in ax.get_yticklabels():
            tl.set_color(col1)
        for tl in ax2.get_yticklabels():
            tl.set_color(col2)
