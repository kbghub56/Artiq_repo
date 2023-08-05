from ndscan.experiment import *
from oitg.results import *
import oitg.fitting
import numpy as np
import matplotlib
# %matplotlib tk
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.optimize
import pylab as plt
from mpl_interactions import ioff, panhandler, zoom_factory
import matplotlib.ticker as mticker


class plotNScan(ExpFragment):
    def build_fragment(self):

        self.setattr_param("rids", StringParam, "INPUT LIST OF RIDs", default = None)

    def run_once(self):
        # extract data from hdf5 for exp 1
        lst_rids = list(self.rids.get().split(", "))
        with plt.ioff():  # for scrollwheel zoom functionality
            figure, axis = plt.subplots()
        for rid in lst_rids:
            dict_test = find_results("", rid=int(rid),
                                     root_path="C:/Artiq/artiq_new_installation/results")  # returns dict of results, used to find file path
            dict_hdf5 = load_hdf5_file(dict_test[int(rid)][0])  # returns file as dict
            dict_datasets = dict_hdf5["datasets"]  # dict key where all points are stored in a nested dict

            # assign data for exp 1 and switch point
            key_name_x = "ndscan.rid_" + rid + ".points.axis_0"  # key name for duration parameter points
            key_name_y = "ndscan.rid_" + rid + ".points.channel_result"  # key name for result parameter points
            key_name_err = "ndscan.rid_" + rid + ".points.channel_res_err"  # key name for error parameter points
            x_vals_1 = list(dict_datasets[key_name_x])
            y_vals_1 = list(dict_datasets[key_name_y])
            err_vals_1 = list(dict_datasets[key_name_err])
            plt.errorbar(x_vals_1, y_vals_1, yerr=err_vals_1, fmt="o")
            plt.scatter(x_vals_1, y_vals_1)

        disconnect_zoom = zoom_factory(axis)
        pan_handler = panhandler(figure)
        plt.xlabel('Time (μs)')  # Indicate that the x axis is in microseconds
        plt.ticklabel_format(style='sci', axis='x', scilimits=(-6, -6))
      #  plt.legend()
        plt.show()



PlotNScan = make_fragment_scan_exp(plotNScan)
