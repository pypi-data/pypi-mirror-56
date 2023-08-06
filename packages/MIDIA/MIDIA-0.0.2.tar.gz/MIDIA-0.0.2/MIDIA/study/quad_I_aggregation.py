import pandas as pd
import numpy as np

def get_quadrupole_I(D, F):
    """Get the aggregate intensities for different windows for a given set of frames.

    Args:
        D (TimsDataMatteo): The data object.
        F (pd.DataFrame): subselected data

    Returns:
        pd.DataFrame: A data frame with intensities in each window and scan. column 'total' collects the integrated intensity, 'current_window' collects the intensity within the m/z selection window performed by the quadrupole, 'prev_window' shows the intensity in the previous window, 'IM' is ion mobility. Columns 'mz_left' and 'mz_right' provide the limits of m/z-selection windows. Note that some scans are missing, as there was no data contained within them.
    """
    F['mass_bin'] = np.digitize(D.mzIdx2mz(F.mz_idx), D.grid)
    F['window_gr'] = np.mod(F.frame - 1, 22) # specific for this data set
    F = F.groupby(['window_gr','scan','mass_bin']).i.sum()
    F = F.loc[1:] # data only after quadrupole selection
    F = F.reset_index().set_index(['scan','window_gr'])
    F = pd.concat([F, D.scan_lims.loc[F.index]], axis=1) # maybe some merge could have solved that quicker???
    F = F.reset_index()

    I_quad_window = F.query('mass_bin > left and mass_bin <= right').groupby(['window_gr','scan']).i.sum()
    I_prev_quad_window = F.query('mass_bin > prev_left and mass_bin <= prev_right').groupby(['window_gr','scan']).i.sum()
    I_total = F.groupby(['window_gr','scan']).i.sum()

    I = pd.concat([I_total, I_quad_window, I_prev_quad_window], axis=1).fillna(0)
    I.columns = ['total','current_window','prev_window']
    I = I.reset_index()
    I['IM'] = D.scan2im(I.scan)
    assert np.all(I.total >= I.current_window + I.prev_window), "too much intensity on the RHS"

    scanWindowGr2window = pd.Series(range(1,D.windows.shape[0]), D.scan_lims.index)
    I['window'] = I.set_index(['scan','window_gr']).index.map(scanWindowGr2window)
    I = I.merge(D.windows[['mz_left','mz_right']], on='window')
    return I
