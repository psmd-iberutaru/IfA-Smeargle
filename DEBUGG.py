import astropy as ap
import astropy.io.fits as ap_fits
import astropy.modeling as ap_mod
import copy
import gc
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.optimize as sp_opt
import scipy.stats as sp_stat

import IfA_Smeargle as ifa


# Finding the data files
fits_file_list = glob.glob('./**/SAPHIRA_Comparison_Fits/**/*.fits',recursive=True)
print(len(fits_file_list))
names = fits_file_list[0].split('\\')[-1]
print(names[:-5] + '.pdf')

print(fits_file_list[0][:-5] + '.pdf')


counter = 0
# List of figures.\n",
for filedex in fits_file_list[counter:]:
    counter += 1

    # Extract.\n",
    fits,header,data = ifa.hotel.open_fits_file(filedex)
    
    # Histogram parameters, desires 1 ADU wide bins.
    bin_list = np.arange(data.min() - 1,data.max() + 1,1)
    
    plot_hist_parameters = {}
    histogram_plot_paramters = {'bins':bin_list, 'range':None}
    plot_hist_parameters['histogram_plot_paramters'] = histogram_plot_paramters
    plot_hist_parameters['fit_gaussian'] = False
    
    # And plot\n",
    temp_figure = ifa.hotel.plot_single_heatmap_and_histogram(data,plot_histogram_parameters=plot_hist_parameters)
    
    title = filedex.split('\\')[-1]
    temp_figure.suptitle(title)

    # Plots with log axis.
    plot_histlog_parameters = {}
    histogramlog_plot_paramters = {'bins':bin_list, 'range':None, 'log':True}
    plot_histlog_parameters['histogram_plot_paramters'] = histogramlog_plot_paramters
    temp_figure_log = \
        ifa.hotel.plot_single_heatmap_and_histogram(data,plot_histogram_parameters=plot_histlog_parameters)
    title_log = filedex.split('\\')[-1] + "__LOG"
    temp_figure_log.suptitle(title_log)
    
    # And save the plot file. We're just saving it in the same place as the actual fits file.
    temp_figure.savefig(filedex[:-5] + '.pdf')
    temp_figure_log.savefig(filedex[:-5] + '__LOG.pdf')
    ###

    plt.close(temp_figure)
    plt.close(temp_figure_log)
    del temp_figure, temp_figure_log

    print(" A figure has been saved. Count {cnt}".format(cnt=counter))
    
    
