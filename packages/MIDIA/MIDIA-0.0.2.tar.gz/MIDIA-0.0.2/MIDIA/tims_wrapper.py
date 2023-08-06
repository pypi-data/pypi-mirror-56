"""Wrappers for TimsData with more DataScientistFriendly functions."""

from functools import lru_cache
from math import inf
import numpy as np
import pandas as pd
from timsdata import TimsData

from .sql import table2df
from .models import ParabolaModel


class AdvancedTims(TimsData):
    """TimsData that uses info about Frames."""
    def __init__(self, analysis_directory, use_recalibrated_state=False):
        """Contructor.

        Args:
            analysis_directory (str,Path): The '*.d' folder with the '*.tdf' files.
            use_recalibrated_state (bool): No idea yet.
        """
        super().__init__(analysis_directory, use_recalibrated_state=False)
        F = self.table2df('Frames').rename(columns={'Time':'rt',
                                                    'Id':'frame'}).set_index('frame')
        self.frames = F
        # WARNING: FRAMES id go from 0 to self.max_frame INCLUSIVE!!!
        self.min_frame = F.index.min()
        self.max_frame = F.index.max()
        self.min_scan = 0
        max_scan = F.NumScans.unique()
        if len(max_scan) != 1:
            raise RuntimeError("Number of TIMS pushes is not constant. This is not the class you want to instantiate on this data.")
        self.max_scan = max_scan[0]

    def frames_no(self):
        """Return the number of frames.

        Returns:
            int: Number of frames.
        """
        return len(self.frames)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.frames_no()} frames)"

    @lru_cache(maxsize=1)
    def global_TIC(self):
        """Get the Total Ion Current across the entire experiment.

        Returns:
            int: Total Ion Current value.
        """
        smin, smax = self.min_scan, self.max_scan
        fmin, fmax = self.min_frame, self.max_frame
        return sum(self.get_TIC(f, smin, smax, True) for f in range(fmin, fmax+1))

    @lru_cache(maxsize=1)
    def count_peaks(self):
        """Count all the peaks in the database.

        Returns:
            int: number of peaks.
        """
        smin, smax = self.min_scan, self.max_scan
        fmin, fmax = self.min_frame, self.max_frame
        return int(sum(self.count_peaks_per_frame_scanRange(f, smin, smax)
                       for f in range(fmin, fmax+1)))

    def get_mzIdx2mz_model(self, mz_min=0, mz_max=2000, mz_num=10000):
        """Get a model that translates mass indices (time) into mass to charge ratios.

        Args:
            mz_min (float): minimal mass over charge.
            mz_max (float): maximal mass over charge.
            mz_num (int): number of grid points between (and including) mz_min and mz_max.
    
        Return:
            ParabolicModel: It is a callable.
        """
        mz = np.linspace(mz_min, mz_max, mz_num)
        mz_idx = self.mzToIndex(1,mz)
        model = ParabolaModel()
        model.fit(mz_idx, mz)
        return model

    @lru_cache(maxsize=64)
    def table2df(self, name):
        """Retrieve a table with a given name from the '*.tdf' file.

        Args:
            name (str): The name of the table to retrieve.        
        """
        return table2df(self.conn, name)

    def mzIdx2mz(self, mz_idx, frame=1):
        """Translate mass indices (flight times) to mass over charge ratios.

        Args:
            mz_idx (int,iterable,np.array,pd.Series): mass indices.
            frame (integer): for which frame this calculations should be performed. These are very stable across
        """
        return self.indexToMz(frame, mz_idx)

    def scan2im(self, scan, frame=1):
        """Translate scan numbers to ion mobilities.

        Args:
            scan (int,iterable,np.array,pd.Series): scans.
            frame (integer): for which frame this calculations should be performed. These do not change accross the experiments actually.
        """
        return self.scanNumToOneOverK0(frame, scan)

    def frame_scan_mzIdx_I_df(self, frame, scan_begin, scan_end, scan_step=1):
        """Get a data frame with measurements for a given frame and scan region.

        The output data frame contains four columns: first repeats the frame number,
        second contains scan numbers, third contains mass indices, and the last contains intensities.
        
        Args:
            frame (int, iterable, slice): Frames to output.
            scan_begin (int): Lower scan.
            scan_end (int): Upper scan.
        Returns:
            pandas.DataFrame: four-columns data frame.
        """
        out = pd.DataFrame(self.frame_scan_mzIdx_I_array(frame,
                                                         scan_begin,
                                                         scan_end,
                                                         scan_step))
        out.columns = ('frame', 'scan', 'mz_idx','i')
        return out

    def iter_arrays(self, frames):
        """Iterate over arrays with TDF data.
        
        Args:
            frames (int,iterable,slice): Frames to restrict to.
            scans (int): Scans to restrict to.

        Yields:
            A flow of numpy arrays.
        """
        for f in np.r_[frames]:
            yield self.frame_scan_mzIdx_I_array(f, self.min_scan, self.max_scan)

    def __getitem__(self, x):
        return_array = False
        if isinstance(x, tuple):
            frames, array_or_df = x
            return_array = array_or_df == 'array'
        else:
            frames = x
        out_array = np.concatenate(list(self.iter_arrays(frames)), axis=0)
        if return_array:
            return out_array
        else:
            out_df = pd.DataFrame(out_array)
            out_df.columns = 'frame', 'scan', 'mz_idx', 'i'
            return out_df

    def array(self, frames=slice(None), filter_frames=''):
        """Return a numpy array with given data.

        Arguments like for 'self.get_frame_scanMin_scanMax'.

        Returns:
            np.array: an array with four columns: frame, scan, mass index (flight time), and intensity.
        """
        if filter_frames:
            frames = np.r_[self.frames.loc[frames].query(filter_frames).index.get_level_values('frame')]
        else:
            frames = np.r_[frames]
        if len(frames) == 0:
            return np.empty(shape=(0,4))
        else:
            return np.concatenate(list(self.iter_arrays(frames)), axis=0)

    def df(self, *args, **kwds):
        """Return a data frame with a selection of data.

        Arguments like for 'self.array'.

        Returns:
            pandas.DataFrame: with four columns: frame, scan, mass index (flight time), and intensity.
        """
        df = pd.DataFrame(self.array(*args,**kwds))
        df.columns = ('frame', 'scan', 'mz_idx', 'i')
        return df

    def iter_dfs(self, *args, **kwds):
        """Iterate over data frames with TDF data.
        
        Arguments like for 'self.get_frame_scanMin_scanMax'.

        Yields:
            A flow of numpy arrays.
        """
        for A in self.iter_arrays(*args, **kwds):
            F = pd.DataFrame(A)
            F.columns = ('frame', 'scan', 'mz_idx', 'i')
            yield F


class TimsDIA(AdvancedTims):
    """Data Independent Acquisition on TIMS."""
    def __init__(self, analysis_directory, use_recalibrated_state=False):
        """Construct TimsDIA.

        Basic information on frames and windows included.
        'self.frames' are indexed here both by frame and window group.

        Args:
            analysis_directory (str,Path): The '*.d' folder with the '*.tdf' files.
            use_recalibrated_state (bool): No idea yet.
        """
        super().__init__(analysis_directory, use_recalibrated_state=False)

        frame2windowGroup = self.table2df('DiaFrameMsMsInfo').set_index('Frame')
        frame2windowGroup.index.name = 'frame'
        frame2windowGroup.columns = ['window_gr']
        F = self.frames.merge(frame2windowGroup, on='frame', how='left')
        F.window_gr = F.window_gr.fillna(0).astype(int) 
        # window_gr == 0 <-> MS1 scan (quadrupole off)
        self.frames = F.reset_index().set_index(['frame', 'window_gr'])

        W = self.table2df('DiaFrameMsMsWindows')
        W['mz_left']   = W.IsolationMz - W.IsolationWidth/2.0
        W['mz_right']  = W.IsolationMz + W.IsolationWidth/2.0
        W = W.drop(columns=['IsolationMz', 'IsolationWidth', 'CollisionEnergy'])
        W.columns = 'group','scan_min','scan_max','mz_left','mz_right'
        self.min_scan = W.scan_min.min()
        self.max_scan = W.scan_max.max()
        MS1 = pd.DataFrame({'group':     0,
                            'scan_min':  self.min_scan,
                            'scan_max':  self.max_scan,
                            'mz_left' :  0,
                            'mz_right':  inf}, index=[0])
        W = MS1.append(W)
        W['win'] = W['window'] = range(len(W))
        W = W.set_index(['window', 'group'])
        W.index.names = 'window', 'window_gr'
        self.grid = sorted(list( set(W.mz_left) | set(W.mz_right) ))
        W['left'] = np.searchsorted(self.grid, W.mz_left)
        W['right'] = np.searchsorted(self.grid, W.mz_right)+1
        W['prev_left'] = [W.left[-1]]*2 + list(W.left[1:-1])
        W['prev_right'] = [W.right[-1]]*2 + list(W.right[1:-1])
        IM_windows = W[['scan_min','scan_max']].apply(lambda x: self.scanNumToOneOverK0(1,x))
        IM_windows.columns = 'IM_min', 'IM_max'
        W = pd.concat([W, IM_windows], axis=1)
        self.windows = W
        scan_lims = W.loc[1:].copy() # data only after quadrupole selection
        intervals = pd.IntervalIndex.from_arrays(scan_lims.scan_min,
                                                 scan_lims.scan_max,
                                                 closed='both')
        intervals.name = 'scan_limits'
        scan_lims = scan_lims.reset_index()
        scan_lims.index = intervals
        scan_lims = scan_lims.set_index('window_gr', append=True)
        self.scan_lims = scan_lims[['left','right','prev_left','prev_right']]
 
    def plot_windows(self, query=""):
        """Plot selection windows with 'plotnine'.

        Install plotnine separately.

        Args:
           query (str): a query used for subselection in "self.windows"
        Returns:
            ggplot: a plot with selection windows
        """
        from plotnine import ggplot, aes, geom_rect, theme_minimal, xlab, ylab, labs
        D = self.windows.reset_index().query(query) if query else self.windows[1:].reset_index()
        plot = (ggplot(aes(), data=D) + 
                geom_rect(aes(xmin='mz_left', xmax='mz_right',
                              ymin='IM_min',  ymax='IM_max',
                              fill='pd.Categorical(window_gr)'), 
                          alpha=.5, color='black')+
                theme_minimal() +
                xlab('mass/charge') +
                ylab('1/K0') +
                labs(fill='Window Group'))
        return plot

    def array(self, window_grs=slice(None), 
                    frames=slice(None),
                    windows=slice(None),
                    filter_frames=''):
        """Return a numpy array with given data.

        Arguments like for 'self.get_frame_scanMin_scanMax'.

        Returns:
            np.array: an array with four columns: frame, scan, mass index (flight time), and intensity.
        """
        if window_grs == slice(None) and windows==slice(None):
            return super().array(frames=frames, filter_frames=filter_frames)
        else:
            F = self.frames.loc[(frames, window_grs),:]
            if filter_frames:
                F = F.query(filter_frames)
            F = F.index.to_frame(index=False)
            if windows != slice(None):
                W = self.windows.loc[(windows, window_grs),['scan_min', 'scan_max']]
                F = F.merge(W, on='window_gr')
                F = F.drop(columns='window_gr')
                arrays = [self.frame_scan_mzIdx_I_array(f,s,S) for _,f,s,S in F.itertuples()]
            else:
                s = self.min_scan
                S = self.max_scan
                arrays = [self.frame_scan_mzIdx_I_array(f,s,S) for _,f,_ in F.itertuples()]
            return np.concatenate(arrays, axis=0)


class TimsDDA(AdvancedTims):
    """Data Dependent Acquisition on TIMS."""
    pass