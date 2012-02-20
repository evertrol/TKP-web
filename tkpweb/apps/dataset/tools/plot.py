import StringIO
import base64
import datetime
import time
import numpy
import aplpy
from scipy.stats import scoreatpercentile
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle
from .image import open_image
import dbase


def image(dbimage, scale=0.9, plotsources=None, database=None):
    figure = Figure(figsize=(5, 5))
    canvas = FigureCanvasAgg(figure)
    image = aplpy.FITSFigure(dbimage['url'], figure=figure, auto_refresh=False)
    image.show_grayscale()
    image.tick_labels.set_font(size=5)
    if plotsources:
        ra = [source['ra'] for source in plotsources]
        dec = [source['decl'] for source in plotsources]
        image.show_markers(ra, dec, s=40, facecolor='none', edgecolor='green')
    memfig = StringIO.StringIO()
    canvas.print_figure(memfig, format='png', transparent=True)
    encoded_png = StringIO.StringIO()
    encoded_png.write('data:image/png;base64,\n')
    encoded_png.write(base64.b64encode(memfig.getvalue()))
    return encoded_png.getvalue()


def lightcurve(lc, T0=datetime.datetime(2010, 1, 1), response=None):
    T0 -= datetime.datetime(1970, 1, 1)
    T0 = (T0.microseconds + (T0.seconds + T0.days * 86400) * 1e6) / 1e6
    dates = matplotlib.dates.date2num([point[0] for point in lc])
    times = numpy.array([time.mktime(point[0].timetuple()) for point in lc]) - T0
    inttimes = [point[1]/2. for point in lc]
    fluxes = [point[2] for point in lc]
    errors = [point[3] for point in lc]
    figure = Figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.errorbar(x=times, y=fluxes, yerr=errors, xerr=inttimes, fmt='bo')
    axes.set_xlabel('Seconds since 2010-1-1T00:00:00')
    axes.set_ylabel('Flux (Jy)')
    canvas = FigureCanvasAgg(figure)
    if response:
       canvas.print_figure(response, format='png')
       return response
    memfig = StringIO.StringIO()
    canvas.print_figure(memfig, format='png')
    encoded_png = StringIO.StringIO()
    encoded_png.write('data:image/png;base64,\n')
    encoded_png.write(base64.b64encode(memfig.getvalue()))
    return encoded_png.getvalue()
