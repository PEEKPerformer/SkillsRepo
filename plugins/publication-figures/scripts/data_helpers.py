"""
Data loading and processing helpers for scientific figure generation.

Provides utilities for CSV loading, signal processing, and statistical analysis.
"""

import numpy as np
import pandas as pd


def load_csv(filepath, skiprows=0, clean=True):
    """
    Load a CSV file with automatic type conversion and cleaning.

    Args:
        filepath: Path to CSV file
        skiprows: Number of rows to skip. Default: 0
        clean: Whether to clean data (remove quotes, convert types). Default: True

    Returns:
        pandas DataFrame
    """
    df = pd.read_csv(filepath, skiprows=skiprows)

    if clean:
        # Clean string values and convert to numeric
        for col in df.columns:
            if df[col].dtype == 'object':
                # Remove quotes and whitespace
                df[col] = df[col].str.replace('"', '').str.strip()
            # Try to convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with all NaN values
        df = df.dropna(how='all')

    return df


def savgol_smooth(data, window=501, order=3, mode='interp'):
    """
    Apply Savitzky-Golay filter for smoothing time series data.

    Args:
        data: 1D array of data to smooth
        window: Window length (must be odd). Default: 501
        order: Polynomial order. Default: 3
        mode: Boundary mode. Default: 'interp'

    Returns:
        numpy array: Smoothed data
    """
    from scipy.signal import savgol_filter

    data = np.asarray(data)

    # Ensure window is odd
    if window % 2 == 0:
        window += 1

    # Window can't be larger than data
    if window > len(data):
        window = len(data) if len(data) % 2 == 1 else len(data) - 1

    return savgol_filter(data, window, order, mode=mode)


def compute_fft(data, dt, return_bpm=False):
    """
    Compute FFT of time series data.

    Args:
        data: 1D time series data
        dt: Sampling interval (seconds)
        return_bpm: Convert frequency to beats per minute. Default: False

    Returns:
        tuple: (frequencies, power spectrum)
    """
    from scipy.fft import fft, fftfreq

    data = np.asarray(data)
    n = len(data)

    # Compute FFT
    yf = fft(data)
    xf = fftfreq(n, dt)

    # Take positive frequencies only
    positive_mask = xf >= 0
    freq = xf[positive_mask]
    power = 2.0 / n * np.abs(yf[positive_mask])

    if return_bpm:
        freq = freq * 60  # Convert Hz to BPM

    return freq, power


def find_signal_peaks(data, distance=None, prominence=None, height=None):
    """
    Find peaks in signal data.

    Args:
        data: 1D array of signal data
        distance: Minimum distance between peaks
        prominence: Minimum prominence of peaks
        height: Minimum height of peaks

    Returns:
        tuple: (peak_indices, peak_properties dict)
    """
    from scipy.signal import find_peaks

    data = np.asarray(data)

    kwargs = {}
    if distance is not None:
        kwargs['distance'] = distance
    if prominence is not None:
        kwargs['prominence'] = prominence
    if height is not None:
        kwargs['height'] = height

    peaks, properties = find_peaks(data, **kwargs)
    return peaks, properties


def calculate_statistics(data, axis=None):
    """
    Calculate common statistics for data.

    Args:
        data: Array of data values
        axis: Axis along which to compute. Default: None (flatten)

    Returns:
        dict: Statistics including mean, std, sem, min, max, median
    """
    data = np.asarray(data)

    return {
        'mean': np.nanmean(data, axis=axis),
        'std': np.nanstd(data, axis=axis),
        'sem': np.nanstd(data, axis=axis) / np.sqrt(np.sum(~np.isnan(data), axis=axis)),
        'min': np.nanmin(data, axis=axis),
        'max': np.nanmax(data, axis=axis),
        'median': np.nanmedian(data, axis=axis),
        'n': np.sum(~np.isnan(data), axis=axis),
    }


def linear_fit(x, y):
    """
    Perform linear regression and return fit parameters.

    Args:
        x: X data
        y: Y data

    Returns:
        dict: Fit results including slope, intercept, r_squared, p_value
    """
    from scipy import stats

    x = np.asarray(x)
    y = np.asarray(y)

    # Remove NaN values
    mask = ~(np.isnan(x) | np.isnan(y))
    x = x[mask]
    y = y[mask]

    result = stats.linregress(x, y)

    return {
        'slope': result.slope,
        'intercept': result.intercept,
        'r_squared': result.rvalue ** 2,
        'p_value': result.pvalue,
        'std_err': result.stderr,
    }


def interpolate_data(x_old, y_old, x_new, kind='linear'):
    """
    Interpolate data to new x values.

    Useful for aligning time series with different sampling rates.

    Args:
        x_old: Original x values
        y_old: Original y values
        x_new: New x values to interpolate to
        kind: Interpolation kind. Default: 'linear'

    Returns:
        numpy array: Interpolated y values
    """
    from scipy.interpolate import interp1d

    f = interp1d(x_old, y_old, kind=kind, bounds_error=False, fill_value=np.nan)
    return f(x_new)


def detect_cycles(data, method='peaks', **kwargs):
    """
    Detect cycles in periodic data (e.g., mechanical cycling, oscillations).

    Args:
        data: 1D signal data
        method: Detection method ('peaks' or 'troughs'). Default: 'peaks'
        **kwargs: Arguments passed to find_signal_peaks

    Returns:
        tuple: (cycle_indices, num_cycles)
    """
    data = np.asarray(data)

    if method == 'troughs':
        # Find troughs by finding peaks of inverted signal
        indices, _ = find_signal_peaks(-data, **kwargs)
    else:
        indices, _ = find_signal_peaks(data, **kwargs)

    num_cycles = len(indices) - 1 if len(indices) > 0 else 0

    return indices, num_cycles


def normalize_data(data, method='minmax'):
    """
    Normalize data using various methods.

    Args:
        data: Data to normalize
        method: Normalization method ('minmax', 'zscore', 'max'). Default: 'minmax'

    Returns:
        numpy array: Normalized data
    """
    data = np.asarray(data, dtype=float)

    if method == 'minmax':
        dmin = np.nanmin(data)
        dmax = np.nanmax(data)
        return (data - dmin) / (dmax - dmin)
    elif method == 'zscore':
        return (data - np.nanmean(data)) / np.nanstd(data)
    elif method == 'max':
        return data / np.nanmax(np.abs(data))
    else:
        raise ValueError(f"Unknown method: {method}")


def detrend_data(data, window=None, order=3):
    """
    Remove trend from time series data.

    Args:
        data: 1D time series data
        window: Savitzky-Golay window for trend estimation. Default: len(data)//10
        order: Polynomial order. Default: 3

    Returns:
        tuple: (detrended_data, trend)
    """
    data = np.asarray(data)

    if window is None:
        window = max(len(data) // 10, 11)
        if window % 2 == 0:
            window += 1

    trend = savgol_smooth(data, window, order)
    detrended = data - trend

    return detrended, trend
