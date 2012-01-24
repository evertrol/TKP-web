import StringIO
import base64
import datetime
import time
import numpy
from scipy.stats import scoreatpercentile
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .image import open_image
import dbase


def image(url, scale=0.9):
    image = open_image(url)
    flat_data = image.data.flatten()
    low = scoreatpercentile(flat_data, per=50-scale*50)
    high = scoreatpercentile(flat_data, per=50+scale*50)
    figure = Figure(figsize=(5, 5))
    axes = figure.add_subplot(1, 1, 1)
    axes.imshow(image.data, cmap=matplotlib.cm.get_cmap('gray'),
                norm=matplotlib.colors.Normalize(low, high, clip=True))
    canvas = FigureCanvasAgg(figure)
    memfig = StringIO.StringIO()
    canvas.print_figure(memfig, format='png', transparent=True)
    encoded_png = StringIO.StringIO()
    encoded_png.write('data:image/png;base64,\n')
    encoded_png.write(base64.b64encode(memfig.getvalue()))
    return encoded_png.getvalue()


def lightcurve(srcid, T0=datetime.datetime(2010, 1, 1), response=None):
    lc = dbase.lightcurve(srcid)
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
