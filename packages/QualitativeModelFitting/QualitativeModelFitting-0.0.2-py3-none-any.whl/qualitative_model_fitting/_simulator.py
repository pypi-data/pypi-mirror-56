import os
import yaml
import pandas as pd
import tellurium as te

from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib

try:
    matplotlib.use('TkAgg')
except ImportError:
    matplotlib.use('agg')
    
import seaborn as sns

import logging

logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
LOG = logging.getLogger(__name__)


class TimeSeries:
    """
    Wrapper around tellurium's ODE integration feature.
    """

    def __init__(self, ant_str: str, inputs: (dict, str),
                 start: int, stop: int, steps: int) -> None:
        """

        Args:
            ant_str: The model to integrate. Must be valid antimony model
            inputs: Nested dict. Contains details of how to configure model for integration (see docs)
            start: start time of integration
            stop:  end time of intergration
            steps: number of steps for integration
        """
        self.ant_str = ant_str
        self.inputs = inputs
        self.start = start
        self.stop = stop
        self.steps = steps
        self.model = self._load_model()

        nested_flag = False
        for k, v in self.inputs.items():
            if isinstance(v, dict):
                nested_flag = True
        self.nested_flag = nested_flag

    def _read_yaml(self):
        with open(self.inputs, 'r') as f:
            inputs = yaml.load(f, Loader=yaml.FullLoader)
        return inputs

    def _load_model(self):
        return te.loada(self.ant_str)

    def _update_initial_conditions(self, condition_inputs):
        for k, v in condition_inputs.items():
            if not hasattr(self.model, k):
                raise AttributeError('Model does not have attribute "{}"'.format(k))
            setattr(self.model, k, v)
        return self.model

    def simulate(self):
        if self.nested_flag:
            return self._simulate_nested()
        else:
            return self._simulate_non_nested()

    def _simulate_nested(self) -> dict:
        """
        _simulate_non_nested time series from nested input
        Returns:

        """
        for k, v in self.inputs.items():
            if not isinstance(v, dict):
                raise TypeError('Was expecting a nested dictionary that looks like this: '
                                '{condition_name: {S=1, I=1}}. Instead, got'
                                ' \n"{}"'.format(self.inputs))
        dct = OrderedDict()
        for condition_name, condition_vals in self.inputs.items():
            # always reset the model before simulating in a loop
            results = TimeSeries(self.ant_str, condition_vals, self.start, self.stop, self.steps).simulate()
            dct[condition_name] = results

        return dct

    def _simulate_non_nested(self) -> dict:
        # always reset the model before simulating in a loop
        self.model.reset()
        # set conditions
        self.model = self._update_initial_conditions(self.inputs)
        globals = dict(
            zip(
                self.model.getGlobalParameterIds(),
                self.model.getGlobalParameterValues()
            )
        )
        self.model.timeCourseSelections += list(globals.keys())
        results = self.model.simulate(self.start, self.stop, self.steps)
        colnames = [i.replace('[', '').replace(']', '') for i in results.colnames]
        results = pd.DataFrame(results, columns=colnames)
        results.set_index('time', inplace=True)
        return results


class _PlotterBase:

    def __init__(self, ts: TimeSeries, plot_selection: dict, conditions=None,
                 subplot_titles={}, savefig=False,
                 plot_dir=os.path.abspath(''), fname=None, ncols=3, wspace=0.25, hspace=0.3,
                 figsize=(12, 7), legend_fontsize=12,
                 legend_loc='best', subplots_adjust={}, seaborn_context='talk',
                 **kwargs):
        sns.set_context(context=seaborn_context)
        self.ts = ts
        self.plot_selection = plot_selection
        self.conditions = conditions
        self.subplot_titles = subplot_titles
        self.fname = fname
        self.savefig = savefig
        self.plot_dir = plot_dir
        self.legend_fontsize = legend_fontsize
        self.legend_loc = legend_loc
        self.ncols = ncols
        self.wspace = wspace
        self.hspace = hspace
        self.figsize = figsize
        self.subplots_adjust = subplots_adjust
        self.kwargs = kwargs

        self.data = self._simulate()

        if self.conditions is None:
            self.conditions = ['default_condition']
        elif isinstance(self.conditions, str):
            self.conditions = [self.conditions]
        elif isinstance(self.conditions, list):
            for i in self.conditions:
                if not isinstance(i, str):
                    raise TypeError('expecting list of strings for condition argument')

        if self.fname is None:
            self.fname = 'simulation.png'

        self._nplots = len(self.plot_selection)
        if self._nplots == 1:
            self.ncols = 1
        self._num_rows = int(self._nplots / ncols)
        self._remainder = self._nplots % ncols
        if self._remainder > 0:
            self._num_rows += 1

    def _simulate(self):
        return self.ts.simulate()

    def _savefig(self, fname):
        if not os.path.isdir(self.plot_dir):
            os.makedirs(self.plot_dir)

        fname = os.path.join(self.plot_dir, f'{fname}-{str(self.count).zfill(self.num_zeros_needed)}.png')
        plt.savefig(fname, dpi=300, bbox_inches='tight')
        LOG.info('saved to {}'.format(fname))
        return fname

    def animate(self, fname, ext='mp4', ovewrite=False, fps=8):
        if not hasattr(self, 'files_'):
            raise ValueError('must _simulate_non_nested files first')
        # files_str = "' '".join(self.files_)
        fname = f'{fname}.{ext}'

        if ovewrite:
            if os.path.isfile(fname):
                os.remove(fname)
        s = ''
        for f in self.files_:
            s += "file '{}'\n".format(f)
            tmp = os.path.join(self.plot_dir, 'tmp.txt')
        with open(tmp, 'w') as f:
            f.write(s)

        s = f"ffmpeg -f concat -safe 0 -r {fps} -i {tmp} {fname}"
        os.system(s)
        os.remove(tmp)


class TimeSeriesPlotter(_PlotterBase):

    def plot(self):
        fig = plt.figure(figsize=self.figsize)
        gs = GridSpec(self._num_rows, self.ncols, wspace=self.wspace, hspace=self.hspace)
        count = 0
        for k, v in self.plot_selection.items():
            ax = fig.add_subplot(gs[count])
            # for cond in self.conditions:
            #     print(cond)
            #     print(self.data)
            #     data = self.data[cond]
            for i in v:
                plt.plot(
                    self.data.index,
                    self.data[i],
                    # label=f'{cond}_{i}' if len(self.conditions) != 1 else f'{i}'
                )
            plt.title(k)
            plt.legend(loc=self.legend_loc, fontsize=self.legend_fontsize)
            sns.despine(fig, top=True, right=True)
            count += 1

        # # plt.suptitle(plot_suptitle)
        plt.subplots_adjust(**self.subplots_adjust)
        if self.savefig:
            if not os.path.isdir(self.plot_dir):
                os.makedirs(self.plot_dir)
            fname = os.path.join(self.plot_dir, self.fname)
            plt.savefig(fname, dpi=300, bbox_inches='tight')
            print('saved to {}'.format(fname))
            return fname
        else:
            plt.show()
