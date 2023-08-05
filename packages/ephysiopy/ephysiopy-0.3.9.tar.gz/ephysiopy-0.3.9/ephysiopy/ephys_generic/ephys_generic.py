#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:04:38 2017

@author: robin
"""
import numpy as np
from scipy import signal
import matplotlib
import matplotlib.pylab as plt
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.transforms as transforms
from matplotlib.patches import Rectangle
from ephysiopy.ephys_generic import binning
from ephysiopy.dacq2py import tintcolours as tcols

class SpikeCalcsGeneric(object):
    '''
    Generic class for processing and analysis of spiking data

    Parameters
    ----------
    spike_times - list or numpy array of the times of 'spikes' in the trial
                    this should be all spikes as the cluster identity vector _spk_clusters
                    is used to pick out the right spikes
    waveforms - np.array - not sure on shape yet but will be something like a
                            a 4 x nSpikes x nSamples (4 for tetrode-based analysis)

    Notes
    -----
    Units for time are always in seconds
    '''
    def __init__(self, spike_times, waveforms=None, **kwargs):
        self.spike_times = spike_times
        self.waveforms = waveforms
        self._event_ts = None # the times that events occured i.e. the laser came on
        self._spk_clusters = None # vector of cluster ids, same length as spike_times
        self._event_window = np.array((-0.050, 0.100)) # window, in seconds, either side of the stimulus, to examine
        self._stim_width = None # the width, in ms, of the stimulus
        self._secs_per_bin = 0.001 # used to increase / decrease size of bins in psth

    @property
    def n_spikes(self):
        return len(self.spike_times)

    @property
    def event_ts(self):
        return self._event_ts

    @event_ts.setter
    def event_ts(self, value):
        self._event_ts = value

    @property
    def spk_clusters(self):
        return self._spk_clusters

    @spk_clusters.setter
    def spk_clusters(self, value):
        self._spk_clusters = value

    @property
    def event_window(self):
        return self._event_window

    @event_window.setter
    def event_window(self, value):
        self._event_window = value

    @property
    def stim_width(self):
        return self._stim_width

    @stim_width.setter
    def stim_width(self, value):
        self._stim_width = value

    @property
    def _secs_per_bin(self):
        return self.__secs_per_bin

    @_secs_per_bin.setter
    def _secs_per_bin(self, value):
        self.__secs_per_bin = value


    def calculatePSTH(self, cluster_id, **kwargs):
        '''
        Calculate the PSTH of event_ts against the spiking of a cell

        Parameters
        ----------
        cluster_id - int - the cluster to calculate the psth of
        '''
        if self._event_ts is None:
            raise Exception("Need some event timestamps! Aborting")
        if self._spk_clusters is None:
            raise Exception("Need cluster identities! Aborting")
        event_ts = self.event_ts
        event_ts.sort()
        if type(event_ts) == list:
            event_ts = np.array(event_ts)

        spike_times = self.spike_times[self.spk_clusters == cluster_id]
        irange = event_ts[:, np.newaxis] + self.event_window[np.newaxis, :]
        dts = np.searchsorted(spike_times, irange)
        x = []
        y = []
        for i, t in enumerate(dts):
            tmp = spike_times[t[0]:t[1]] - event_ts[i]
            x.extend(tmp)
            y.extend(np.repeat(i,len(tmp)))
        return x, y

    def plotPSTH(self, cluster, fig=None):
        '''
        Plots the PSTH for a cluster

        Parameters
        ----------
        cluster - int - the cluster to examine
        '''
        x, y = self.calculatePSTH(cluster)
        show = False # used below to show the figure or leave this to the caller
        if fig is None:
            fig = plt.figure(figsize=(4.0,7.0))
            show = True
        scatter_ax = fig.add_subplot(111)
        scatter_ax.scatter(x, y, marker='.', s=2, rasterized=False)
        divider = make_axes_locatable(scatter_ax)
        scatter_ax.set_xticks((self.event_window[0], 0, self.event_window[1]))
        scatter_ax.set_xticklabels((str(self.event_window[0]), '0', str(self.event_window[1])))
        hist_ax = divider.append_axes("top", 0.95, pad=0.2, sharex=scatter_ax,
                                      transform=scatter_ax.transAxes)
        scattTrans = transforms.blended_transform_factory(scatter_ax.transData,
                                                          scatter_ax.transAxes)
        if self.stim_width is not None:
            scatter_ax.add_patch(Rectangle((0, 0), width=self.stim_width, height=1,
                        transform=scattTrans,
                        color=[0, 0, 1], alpha=0.5))
            histTrans = transforms.blended_transform_factory(hist_ax.transData,
                                                             hist_ax.transAxes)
            hist_ax.add_patch(Rectangle((0, 0), width=self.stim_width, height=1,
                              transform=histTrans,
                              color=[0, 0, 1], alpha=0.5))
        scatter_ax.set_ylabel('Laser stimulation events', labelpad=-18.5)
        scatter_ax.set_xlabel('Time to stimulus onset(secs)')
        nStms = int(len(self.event_ts))
        scatter_ax.set_ylim(0, nStms)
        # Label only the min and max of the y-axis
        ylabels = scatter_ax.get_yticklabels()
        for i in range(1, len(ylabels)-1):
            ylabels[i].set_visible(False)
        yticks = scatter_ax.get_yticklines()
        for i in range(1, len(yticks)-1):
            yticks[i].set_visible(False)
        histColor = [192/255.0,192/255.0,192/255.0]
        histX = hist_ax.hist(x, bins=np.arange(self.event_window[0], self.event_window[1] + self._secs_per_bin, self._secs_per_bin),
                             color=histColor, alpha=0.6, range=self.event_window, rasterized=True, histtype='stepfilled')
        hist_ax.set_ylabel("Spike count", labelpad=-2.5)
        plt.setp(hist_ax.get_xticklabels(), visible=False)
        # Label only the min and max of the y-axis
        ylabels = hist_ax.get_yticklabels()
        for i in range(1, len(ylabels)-1):
            ylabels[i].set_visible(False)
        yticks = hist_ax.get_yticklines()
        for i in range(1, len(yticks)-1):
            yticks[i].set_visible(False)
        hist_ax.set_xlim(self.event_window)
        scatter_ax.set_xlim(self.event_window)
        if show:
            plt.show()
        yield cluster, 1

    def plotAllXCorrs(self, clusters, fig=None):
        '''
        Plots all scorrs in a single figure window
        '''
        from ephysiopy.dacq2py import spikecalcs
        SpkCalcs = spikecalcs.SpikeCalcs()
        if fig is None:
            fig = plt.figure(figsize=(10,20))

        nrows = np.ceil(np.sqrt(len(clusters))).astype(int)
        fig.subplots_adjust(wspace=0.25,hspace=0.25)
        for i, cluster in enumerate(clusters):
            cluster_idx = np.nonzero(self.spk_clusters == cluster)[0]
            cluster_ts = np.ravel(self.spike_times[cluster_idx])
            ax = fig.add_subplot(nrows,nrows,i+1)
            y = SpkCalcs.xcorr(cluster_ts.T / 30.)
            ax.hist(y[y != 0], bins=201, range=[-500, 500], color='k', histtype='stepfilled')
            ax.set_xlim(-500,500)
            ax.set_xticks((-500, 0, 500))
            ax.set_xticklabels((str(-500), '0', str(500)),fontweight='normal', size=8)
            ax.tick_params(axis='both', which='both', left=False, right=False,
                            bottom=False, top=False)
            ax.set_yticklabels('')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.xaxis.set_ticks_position('bottom')
            ax.set_title(cluster, fontweight='bold', size=10, pad=1)
        plt.show()



class EEGCalcsGeneric(object):
    '''
    Generic class for processing and analysis of EEG data

    Parameters
    ----------
    sig - 1D np.array of the LFP data
    fs  - float - sample rate
    '''
    def __init__(self, sig, fs):
        self.sig = sig
        self.fs = fs
        self.thetaRange = [6,12]
        self.outsideRange = [3,125]
        # for smoothing and plotting of power spectrum
        self.smthKernelWidth = 2
        self.smthKernelSigma = 0.1875
        self.sn2Width = 2
        self.maxFreq = 125
        self.maxPow = None

    def _nextpow2(self, val):
        '''calculates the next power of 2 that will hold val'''
        val = val - 1
        val = (val >> 1) | val
        val = (val >> 2) | val
        val = (val >> 4) | val
        val = (val >> 8) | val
        val = (val >> 16) | val
        val = (val >> 32) | val
        return np.log2(val + 1)

    def butterFilter(self, low, high, order=5):
        nyqlim = self.fs / 2
        lowcut = low / nyqlim
        highcut = high / nyqlim
        b, a = signal.butter(order, [lowcut, highcut], btype='band')
        return signal.filtfilt(b, a, self.sig)

    def calcEEGPowerSpectrum(self, **kwargs):
        nqlim = self.fs / 2
        origlen = len(self.sig)
        fftlen = 2 ** self._nextpow2(origlen).astype(int)
        freqs, power = signal.periodogram(self.sig, self.fs, return_onesided=True, nfft=fftlen)
        ffthalflen = fftlen / 2+1
        binsperhz = (ffthalflen-1) / nqlim
        kernelsigma = self.smthKernelSigma * binsperhz
        smthkernelsigma = 2 * int(4.0 * kernelsigma + 0.5) + 1
        gausswin = signal.gaussian(smthkernelsigma, kernelsigma)
        sm_power = signal.fftconvolve(power, gausswin, 'same')
        sm_power = sm_power / np.sqrt(len(sm_power))
        spectrummaskband = np.logical_and(freqs > self.thetaRange[0], freqs < self.thetaRange[1])
        bandmaxpower = np.max(sm_power[spectrummaskband])
        maxbininband = np.argmax(sm_power[spectrummaskband])
        bandfreqs = freqs[spectrummaskband]
        freqatbandmaxpower = bandfreqs[maxbininband]
        self.freqs = freqs
        self.power = power
        self.sm_power = sm_power
        self.bandmaxpower = bandmaxpower
        self.freqatbandmaxpower = freqatbandmaxpower

    def plotPowerSpectrum(self, **kwargs):
        # calculate
        self.calcEEGPowerSpectrum()
        # plotting
        import matplotlib.pylab as plt
        plt.figure()
        ax = plt.gca()
        freqs = self.freqs[0::50]
        power = self.power[0::50]
        sm_power = self.sm_power[0::50]
        ax.plot(freqs, power, alpha=0.5, color=[0.8627, 0.8627, 0.8627])
        ax.plot(freqs, sm_power)
        ax.set_xlim(0, self.maxFreq)
        if 'ylim' in kwargs.keys():
            ylim = kwargs['ylim']
        else:
            ylim = [0, self.bandmaxpower / 0.8]

        ax.set_ylim(ylim)
        ax.set_ylabel('Power')
        ax.set_xlabel('Frequency')
        ax.text(x=self.thetaRange[1] / 0.9, y=self.bandmaxpower, s=str(self.freqatbandmaxpower)[0:4], fontsize=20)
        from matplotlib.patches import Rectangle
        r = Rectangle((self.thetaRange[0],0), width=np.diff(self.thetaRange)[0], height=np.diff(ax.get_ylim())[0], alpha=0.25, color='r', ec='none')
        ax.add_patch(r)
        plt.show()

    def plotEventEEG(self, event_ts, event_window=(-0.05, 0.1), stim_width=0.01, sample_rate=3e4):
        '''
        Plots the mean eeg +- std. dev centred on event timestamps

        '''
        # bandpass filter the raw data first
        from scipy import signal
        nyq = sample_rate / 2
        highlim = 500 / nyq
        b, a = signal.butter(5, highlim, btype='lowpass')
        sig = signal.filtfilt(b, a, self.sig)

        event_idx = np.round(event_ts*sample_rate).astype(int)
        event_window = np.array(event_window)

        max_samples = np.ptp(event_window*sample_rate).astype(int)
        num_events = len(event_ts)
        eeg_array = np.zeros([num_events, max_samples])
        st = int(event_window[0]*sample_rate)
        en = int(event_window[1]*sample_rate)
        for i, eeg_idx in enumerate(event_idx):
            eeg_array[i, :] = sig[eeg_idx+st:eeg_idx+en]
        mn = np.mean(eeg_array, 0)
        se = np.std(eeg_array, 0) / np.sqrt(num_events)
        import matplotlib.pylab as plt
        # from mpl_toolkits.axes_grid1 import make_axes_locatable
        import matplotlib.transforms as transforms
        from matplotlib.patches import Rectangle
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.errorbar(np.linspace(event_window[0], event_window[1], len(mn)), mn, yerr=se, rasterized=False)
        ax.set_xlim(event_window)
        axTrans = transforms.blended_transform_factory(ax.transData,
                                                           ax.transAxes)
        ax.add_patch(Rectangle((0, 0), width=stim_width, height=1,
                             transform=axTrans,
                             color=[1, 1, 0], alpha=0.5))
        ax.set_ylabel('LFP ($\mu$V)')
        ax.set_xlabel('Time(s)')
        plt.show()

class PosCalcsGeneric(object):
    '''
    Generic class for post-processing of position data
    Uses numpys masked arrays for dealing with bad positions, filtering etc

    Parameters
    ----------
    x - 1 or 2D np.array of x positions. If 2D then 2-LED tracking was done
    y - same as x but for y positions
    ppm - int - pixels per metre
    cm - bool - whether everything is converted into cms or not
    jumpmax - int - jumps in position (pixel coords) greater than this are bad
    '''
    def __init__(self, x, y, ppm, cm=True, jumpmax=100):
        assert np.shape(x) == np.shape(y)
        self.xy = np.ma.MaskedArray([x, y])
        self.dir = np.ma.MaskedArray(np.zeros_like(x))
        self.speed = None
        self.ppm = ppm
        self.cm = cm
        self.jumpmax = jumpmax
        self.nleds = np.ndim(x)
        self.npos = len(x)
        self.tracker_params = None

    def postprocesspos(self, tracker_params, **kwargs):
        '''
        Post-process position data

        Parameters
        ----------
        tracker_params - dict - same dict as created in OEKiloPhy.Settings.parsePos
                                (from module openephys2py)

        '''
        xy = self.xy
        self.tracker_params = tracker_params
        xy[xy < 0] = np.ma.masked

        if 'LeftBorder' in tracker_params:
            min_x = tracker_params['LeftBorder']
            xy[:, xy[0,:] <= min_x] = np.ma.masked
        if 'TopBorder' in tracker_params:
            min_y = tracker_params['TopBorder'] # y origin at top
            xy[:, xy[1,:] <= min_y] = np.ma.masked
        if 'RightBorder' in tracker_params:
            max_x = tracker_params['RightBorder']
            xy[:, xy[0,:] >= max_x] = np.ma.masked
        if 'BottomBorder' in tracker_params:
            max_y = tracker_params['BottomBorder']
            xy[:, xy[1,:] >= max_y] = np.ma.masked
        if 'SampleRate' in tracker_params.keys():
            self.sample_rate = int(tracker_params['SampleRate'])
        else:
            self.sample_rate = 30

        xy = self.speedfilter(xy)
        xy = self.interpnans(xy)
        xy = self.smoothPos(xy)
        self.calcSpeed(xy)

        import math
        pos2 = np.arange(0, self.npos-1)
        xy_f = xy.astype(np.float)
        self.dir[pos2] = np.mod(((180/math.pi) * (np.arctan2(-xy_f[1, pos2+1] + xy_f[1,pos2],+xy_f[0,pos2+1]-xy_f[0,pos2]))), 360)
        self.dir[-1] = self.dir[-2]

        hdir = self.dir

        return xy, hdir

    def speedfilter(self, xy):
        maxppmsqd = self.jumpmax ** 2
        df = np.diff(xy)
        disp = np.hypot(df[0,:], df[1,:])
        disp = np.insert(disp, -1, 0)
        xy[:, disp > maxppmsqd] = np.ma.masked
        return xy

    def interpnans(self, xy):
        for i in range(0,len(xy), 2):
            missing = xy[i:i+2].mask.any(axis=0)
            ok = np.logical_not(missing)
            ok_idx = np.nonzero(np.ravel(ok))[0]#gets the indices of ok poses
            missing_idx = np.nonzero(np.ravel(missing))[0]#get the indices of missing poses
            good_data = xy.data[i,ok_idx]
            good_data1 = xy.data[i+1,ok_idx]
            xy.data[i,missing_idx] = np.interp(missing_idx,ok_idx,good_data)#,left=np.min(good_data),right=np.max(good_data)
            xy.data[i+1,missing_idx] = np.interp(missing_idx,ok_idx,good_data1)
        xy.mask = 0
        print("{} bad/ jumpy positions were interpolated over".format(len(missing_idx)))
        return xy

    def smoothPos(self, xy):
        '''
        Process position data
        TODO: make this synonomous with Axona's postprocesspos
        '''
        # Extract boundaries of window used in recording

        x = xy[0].astype(np.float64)
        y = xy[1].astype(np.float64)

        from ephysiopy.dacq2py import smoothdata
        # TODO: calculate window_len from pos sampling rate
        # 11 is roughly equal to 400ms at 30Hz (window_len needs to be odd)
        sm_x = smoothdata.smooth(x, window_len=11, window='flat')
        sm_y = smoothdata.smooth(y, window_len=11, window='flat')
        return np.array([sm_x, sm_y])

    def calcSpeed(self, xy):
        speed = np.sqrt(np.sum(np.power(np.diff(xy),2),0))
        speed = np.append(speed, speed[-1])
        self.speed = speed * (100 * self.sample_rate / self.ppm) # in cm/s now

    def upsamplePos(self, xy, upsample_rate=50):
        '''
        Upsampling for matching with Axona pos sampling rate
        NB Assumes that the pos is being upsampled from 30Hz
        '''
        from scipy import signal
        denom = np.gcd(upsample_rate, 30)
        new_xy = signal.resample_poly(xy, upsample_rate/denom, 30/denom)
        return new_xy

class MapCalcsGeneric(object):
    '''

    '''
    def __init__(self, xy, hdir, speed, pos_ts, spk_ts, plot_type='map', **kwargs):
        '''
        Parameters
        ----------
        xy - 2D numpy array
        hdir - 1D numpy array
        pos_ts - 1D numpy array; timestamps in seconds
        spk_ts - 1D numpy array; timestamps in seconds
        plot_type - str or list - any combination of ['map','path','hdir','sac', 'speed']
        '''
        if (np.argmin(np.shape(xy)) == 1):
            xy = xy.T
        self.xy = xy
        self.hdir = hdir
        self.speed = speed
        self.pos_ts = pos_ts
        if (spk_ts.ndim == 2):
            spk_ts = np.ravel(spk_ts)
        self.spk_ts = spk_ts
        self.plot_type = plot_type
        self.spk_pos_idx = self.__interpSpkPosTimes()
        self.__good_clusters = None
        self.__spk_clusters = None
        if ( 'ppm' in kwargs.keys() ):
            self.__ppm = kwargs['ppm']
        else:
            self.__ppm = 400
        if 'pos_sample_rate' in kwargs.keys():
            self.pos_sample_rate = kwargs['pos_sample_rate']
        else:
            self.pos_sample_rate = 30

    def __interpSpkPosTimes(self):
        '''
        Interpolates spike times into indices of position data
        NB Assumes pos times have been zeroed correctly - see comments in
        OEKiloPhy.OpenEphysNWB function __alignTimeStamps__()
        '''
        idx = np.searchsorted(self.pos_ts, self.spk_ts)
        idx[idx==len(self.pos_ts)] = len(self.pos_ts) - 1
        return idx

    @property
    def good_clusters(self):
        return self.__good_clusters

    @good_clusters.setter
    def good_clusters(self, value):
        self.__good_clusters = value

    @property
    def spk_clusters(self):
        return self.__spk_clusters

    @spk_clusters.setter
    def spk_clusters(self, value):
        self.__spk_clusters = value

    @property
    def ppm(self):
        return self.__ppm

    @ppm.setter
    def ppm(self, value):
        self.__ppm = value

    def plotAll(self):
        if 'all' in self.plot_type:
            what_to_plot = ['map','path','hdir','sac','speed', 'sp_hd']
            fig = plt.figure(figsize=(20,10))
        else:
            what_to_plot = list(self.plot_type)
            if len(what_to_plot) > 1:
                fig = plt.figure(figsize=(20,10))
            else:
                fig = plt.figure(figsize=(20,10))#, constrained_layout=True)
        if 'sac' in what_to_plot:
            from dacq2py import gridcell
            S = gridcell.SAC()
            print(gridcell.__file__)
        import matplotlib.gridspec as gridspec
        nrows = np.ceil(np.sqrt(len(self.good_clusters))).astype(int)
        outer = gridspec.GridSpec(nrows, nrows, figure=fig)

        inner_ncols = int(np.ceil(len(what_to_plot) / 2)) # max 2 cols
        if len(what_to_plot) == 1:
            inner_nrows = 1
        else:
            inner_nrows = 2
        first_sub_axis = what_to_plot[0]
        for i, cluster in enumerate(self.good_clusters):
            inner = gridspec.GridSpecFromSubplotSpec(inner_nrows,inner_ncols, subplot_spec=outer[i])
            for plot_type_idx, plot_type in enumerate(what_to_plot):
                if 'path' in plot_type:
                    ax = fig.add_subplot(inner[plot_type_idx])
                    self.makeSpikePathPlot(cluster, ax)
                if 'map' in plot_type:
                    ax = fig.add_subplot(inner[plot_type_idx])
                    rmap = self.makeRateMap(cluster, ax)
                if 'hdir' in plot_type:
                    ax = fig.add_subplot(inner[plot_type_idx],projection='polar')
                    self.makeHDPlot(cluster, ax, add_mrv=True)
                if 'sac' in plot_type:
                    ax = fig.add_subplot(inner[plot_type_idx])
                    rmap = self.makeRateMap(cluster)
                    nodwell = ~np.isfinite(rmap[0])
                    sac = S.autoCorr2D(rmap[0], nodwell)
                    d = S.getMeasures(sac)
                    S.show(sac,d,ax)
                if 'speed' in plot_type:
                    ax = fig.add_subplot(inner[plot_type_idx])
                    self.makeSpeedVsRatePlot(cluster, 0.0, 40.0, 3.0, ax)
                if 'sp_hd' in plot_type:
                    ax = fig.add_subplot(inner[plot_type_idx])
                    self.makeSpeedVsHeadDirectionPlot(cluster, ax)
                if first_sub_axis in plot_type: # label the first sub-axis only
                    ax = fig.add_subplot(inner[plot_type_idx])
                    ax.set_title(cluster, fontweight='bold', size=8)
        plt.show()

    def __iter__(self):
        if 'all' in self.plot_type:
            from dacq2py import gridcell
            S = gridcell.SAC()

        for cluster in self.good_clusters:
            print("Cluster {}".format(cluster))
            if 'map' in self.plot_type:
                fig = plt.figure()
                ax = plt.gca()
                self.makeRateMap(cluster, ax)
                fig.show()
            elif 'path' in self.plot_type:
                plt.figure()
                ax = plt.gca()
                self.makeSpikePathPlot(cluster, ax)
                plt.show()
            elif 'hdir' in self.plot_type:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='polar')
                self.makeHDPlot(cluster, ax)
                plt.show()
            elif 'both' in self.plot_type:
                fig, (ax1, ax0) = plt.subplots(1,2)
                # ratemap
                self.makeRateMap(cluster, ax0)
                # path / spikes
                self.makeSpikePathPlot(cluster, ax1)
                plt.show()
            elif 'speed' in self.plot_type:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                self.makeSpeedVsRatePlot(cluster, 0.0, 40.0, 3.0, ax)
            elif 'sp_hd' in self.plot_type:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                self.makeSpeedVsHeadDirectionPlot(cluster, ax)
            elif 'all' in self.plot_type:
                fig = plt.figure(figsize=[9.6, 6.0])
                fig.suptitle("Cluster {}".format(cluster))
                ax1 = fig.add_subplot(2, 3, 1)
                self.makeSpikePathPlot(cluster, ax1)
                ax0 = fig.add_subplot(2, 3, 2)
                rmap = self.makeRateMap(cluster, ax0)
                ax2 = fig.add_subplot(2, 3, 3)
                nodwell = ~np.isfinite(rmap[0])
                sac = S.autoCorr2D(rmap[0], nodwell)
                d = S.getMeasures(sac)
                S.show(sac,d,ax2)
                print("Gridscore: {:.2f}".format(d['gridness']))
                ax3 = fig.add_subplot(2, 3, 4, projection='polar')
                self.makeHDPlot(cluster, ax3, add_mrv=True)
                ax4 = fig.add_subplot(2, 3, 5)
                self.makeSpeedVsRatePlot(cluster, 0.0, 40.0, 3.0, ax4)
                ax5 = fig.add_subplot(2, 3, 6)
                self.makeSpeedVsHeadDirectionPlot(cluster, ax5)
                plt.show()
            yield cluster

    def makeRateMap(self, cluster, ax=None):
        pos_w = np.ones_like(self.pos_ts)
        mapMaker = binning.RateMap(self.xy, None, None, pos_w, ppm=self.ppm)
        spk_w = np.bincount(self.spk_pos_idx, self.spk_clusters==cluster, minlength=self.pos_ts.shape[0])
        # print("nSpikes: {}".format(np.sum(spk_w).astype(int)))
        rmap = mapMaker.getMap(spk_w)
        if ax is None:
            return rmap
        ratemap = np.ma.MaskedArray(rmap[0], np.isnan(rmap[0]), copy=True)
        x, y = np.meshgrid(rmap[1][1][0:-1], rmap[1][0][0:-1][::-1])
        vmax = np.max(np.ravel(ratemap))
        ax.pcolormesh(x, y, ratemap, cmap=cm.jet, edgecolors='face', vmax=vmax)
        ax.axis([x.min(), x.max(), y.min(), y.max()])
        ax.set_aspect('equal')
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        return rmap

    def makeSpikePathPlot(self, cluster, ax):
        ax.plot(self.xy[0], self.xy[1], c=tcols.colours[0], zorder=1)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        idx = self.spk_pos_idx[self.spk_clusters==cluster]
        spk_colour = tcols.colours[1]
        ax.plot(self.xy[0,idx], self.xy[1,idx],'s',ms=1, c=spk_colour,mec=spk_colour)
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

    def makeHDPlot(self, cluster, ax, **kwargs):
        pos_w = np.ones_like(self.pos_ts)
        mapMaker = binning.RateMap(self.xy, self.hdir, None, pos_w, ppm=self.ppm)
        spk_w = np.bincount(self.spk_pos_idx, self.spk_clusters==cluster, minlength=self.pos_ts.shape[0])
        rmap = mapMaker.getMap(spk_w, 'dir', 'rate')
        if rmap[0].ndim == 1:
            # polar plot
            if ax is None:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='polar')
            theta = np.deg2rad(rmap[1][0][1:])
            ax.clear()
            ax.plot(theta, rmap[0])
            ax.set_aspect('equal')
            ax.tick_params(axis='both', which='both', bottom=False, left=False, right=False, top=False, labelbottom=False, labelleft=False, labeltop=False, labelright=False)
            ax.set_rticks([])

            # See if we should add the mean resultant vector (mrv)
            if 'add_mrv' in kwargs.keys():
                from dacq2py import statscalcs
                S = statscalcs.StatsCalcs()
                angles = self.hdir[self.spk_pos_idx[self.spk_clusters==cluster]]
                r, th = S.mean_resultant_vector(np.deg2rad(angles))
                # print("Mean resultant vector:")
                # print('\tUnit vector length: {:.3f}\n\tVector angle: {:.2f}'.format(r,np.rad2deg(th)))
                ax.plot([th, th],[0, r*np.max(rmap[0])],'r')
            ax.set_thetagrids([0, 90, 180, 270])

    def makeSpeedVsRatePlot(self, cluster, minSpeed=0.0, maxSpeed=40.0, sigma=3.0, ax=None, **kwargs):
        '''
        Plots the instantaneous firing rate of a cell against running speed
        Also outputs a couple of measures as with Kropff et al., 2015; the
        Pearsons correlation and the depth of modulation (dom) - see below for
        details
        '''
        speed = np.ravel(self.speed)
        if np.nanmax(speed) < maxSpeed:
            maxSpeed = np.nanmax(speed)
        spd_bins = np.arange(minSpeed, maxSpeed, 1.0)
        # Construct the mask
        speed_filt = np.ma.MaskedArray(speed)
        speed_filt = np.ma.masked_where(speed_filt < minSpeed, speed_filt)
        speed_filt = np.ma.masked_where(speed_filt > maxSpeed, speed_filt)
        from dacq2py import spikecalcs
        S = spikecalcs.SpikeCalcs();
        x1 = self.spk_pos_idx[self.spk_clusters==cluster]
        spk_sm = S.smoothSpikePosCount(x1, self.pos_ts.shape[0], sigma, None)
        spk_sm = np.ma.MaskedArray(spk_sm, mask=np.ma.getmask(speed_filt))
        from scipy import stats
        result = stats.mstats.pearsonr(spk_sm, speed_filt)
        spd_dig  = np.digitize(speed_filt, spd_bins, right=True)
        mn_rate = np.array([np.ma.mean(spk_sm[spd_dig==i]) for i in range(0,len(spd_bins))])
        var = np.array([np.ma.std(spk_sm[spd_dig==i]) for i in range(0,len(spd_bins))])
        count = np.array([np.ma.sum(spk_sm[spd_dig==i]) for i in range(0,len(spd_bins))])
        # se = var / count
        if ax is not None:
            ax.errorbar(spd_bins, mn_rate * self.pos_sample_rate, yerr=var, color='k')
            ax.set_xlim(spd_bins[0], spd_bins[-1])
            plt.xticks([spd_bins[0], spd_bins[-1]], ['0', '{:.2g}'.format(spd_bins[-1])], fontweight='normal', size=6)
            plt.yticks([0,np.nanmax(mn_rate)*self.pos_sample_rate], ['0', '{:.2f}'.format(np.nanmax(mn_rate))], fontweight='normal', size=6)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')

    def makeSpeedVsHeadDirectionPlot(self, cluster, ax):
        idx = self.spk_pos_idx[self.spk_clusters==cluster]
        w = np.bincount(idx, minlength=self.speed.shape[0])
        dir_bins = np.arange(0,360,6)
        spd_bins = np.arange(0,30,1)
        h = np.histogram2d(self.hdir, self.speed, [dir_bins,spd_bins],weights=w)
        b = binning.RateMap()
        im = b.blurImage(h[0],5,ftype='gaussian')
        im = np.ma.MaskedArray(im);
        # mask low rates...
        im = np.ma.masked_where(im<=1, im)
        # ... and where less than 0.5% of data is accounted for
        # all_sp_x_hd_binned = np.histogram2d(self.hdir, self.speed, [dir_bins,spd_bins])[0]
        # im = np.ma.masked_where(all_sp_x_hd_binned < (len(self.speed) * 0.005), im)
        x,y = np.meshgrid(dir_bins, spd_bins)
        ax.pcolormesh(x,y,im.T);
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.xticks([90,180,270], fontweight='normal', size=6)
        plt.yticks([10,20], fontweight='normal', size=6)

