"""
Template matching for SEM zoom region detection.

Uses FFT-accelerated cross-correlation to find where a high-magnification
image corresponds to within a low-magnification overview.
"""

import numpy as np


def find_zoom_region(low_mag_img, high_mag_img, scale_range=(8, 12), steps=20):
    """
    Find where a high-magnification image is located within a low-magnification image.

    Uses gradient-based feature extraction and FFT-accelerated cross-correlation
    to detect the zoom region across different scales.

    Args:
        low_mag_img: Low magnification image (numpy array, 0-1 float)
        high_mag_img: High magnification image (numpy array, 0-1 float)
        scale_range: (min_scale, max_scale) to search. Default: (8, 12)
        steps: Number of scale steps to try. Default: 20

    Returns:
        dict: {
            'box': (x1, y1, x2, y2) bounding box in low_mag coordinates,
            'scale': detected scale factor,
            'correlation': peak correlation value,
            'center': (cx, cy) center of detected region
        }
    """
    # Extract gradient features (edges are consistent across magnifications)
    low_grad = _sobel_magnitude(low_mag_img)
    high_grad = _sobel_magnitude(high_mag_img)

    best_result = {
        'correlation': -1,
        'scale': None,
        'position': None,
    }

    scales = np.linspace(scale_range[0], scale_range[1], steps)

    for scale in scales:
        # Downsample high-mag to match expected size in low-mag
        downsampled = _downsample(high_grad, scale)

        if downsampled.shape[0] < 10 or downsampled.shape[1] < 10:
            continue

        # FFT-accelerated cross-correlation
        corr = _fft_correlate(low_grad, downsampled)

        # Find peak
        peak_val = np.max(corr)
        if peak_val > best_result['correlation']:
            peak_pos = np.unravel_index(np.argmax(corr), corr.shape)
            best_result = {
                'correlation': peak_val,
                'scale': scale,
                'position': peak_pos,
                'template_shape': downsampled.shape,
            }

    if best_result['scale'] is None:
        raise ValueError("Could not find zoom region - no correlation peak found")

    # Calculate bounding box
    y, x = best_result['position']
    h, w = best_result['template_shape']

    box = (
        int(x),
        int(y),
        int(x + w),
        int(y + h),
    )

    center = (
        int(x + w / 2),
        int(y + h / 2),
    )

    return {
        'box': box,
        'scale': best_result['scale'],
        'correlation': best_result['correlation'],
        'center': center,
    }


def _sobel_magnitude(img):
    """
    Compute Sobel gradient magnitude for edge detection.

    Args:
        img: Input image (2D array)

    Returns:
        Gradient magnitude image
    """
    try:
        from scipy.ndimage import sobel
        gx = sobel(img, axis=1)
        gy = sobel(img, axis=0)
        return np.sqrt(gx**2 + gy**2)
    except ImportError:
        # Simple gradient fallback
        gx = np.diff(img, axis=1, prepend=img[:, :1])
        gy = np.diff(img, axis=0, prepend=img[:1, :])
        return np.sqrt(gx**2 + gy**2)


def _downsample(img, factor):
    """
    Downsample image by a factor.

    Args:
        img: Input image
        factor: Downsampling factor

    Returns:
        Downsampled image
    """
    new_h = int(img.shape[0] / factor)
    new_w = int(img.shape[1] / factor)

    if new_h < 1 or new_w < 1:
        return img

    try:
        from skimage.transform import resize
        return resize(img, (new_h, new_w), anti_aliasing=True)
    except ImportError:
        # Simple block averaging fallback
        h, w = img.shape
        block_h = h // new_h
        block_w = w // new_w
        result = np.zeros((new_h, new_w))
        for i in range(new_h):
            for j in range(new_w):
                block = img[i*block_h:(i+1)*block_h, j*block_w:(j+1)*block_w]
                result[i, j] = np.mean(block)
        return result


def _fft_correlate(image, template):
    """
    FFT-accelerated normalized cross-correlation.

    O(n log n) instead of O(n^2) for direct correlation.

    Args:
        image: Large image to search in
        template: Small template to find

    Returns:
        Correlation map
    """
    from scipy.signal import correlate2d

    # Normalize template
    template = template - np.mean(template)
    template = template / (np.std(template) + 1e-8)

    # Normalize image
    image = image - np.mean(image)
    image = image / (np.std(image) + 1e-8)

    # Use scipy's correlate which uses FFT for large arrays
    try:
        corr = correlate2d(image, template, mode='valid')
    except Exception:
        # Fallback for very large images
        corr = _naive_correlate(image, template)

    return corr


def _naive_correlate(image, template):
    """
    Simple sliding window correlation (fallback).

    Args:
        image: Large image
        template: Small template

    Returns:
        Correlation map
    """
    th, tw = template.shape
    ih, iw = image.shape

    out_h = ih - th + 1
    out_w = iw - tw + 1

    if out_h <= 0 or out_w <= 0:
        return np.array([[0]])

    corr = np.zeros((out_h, out_w))

    template_flat = template.flatten()
    template_norm = np.sqrt(np.sum(template_flat**2))

    for i in range(out_h):
        for j in range(out_w):
            window = image[i:i+th, j:j+tw].flatten()
            window_norm = np.sqrt(np.sum(window**2))
            if window_norm > 0 and template_norm > 0:
                corr[i, j] = np.dot(window, template_flat) / (window_norm * template_norm)

    return corr


def validate_zoom_match(low_mag_img, high_mag_img, box, threshold=0.3):
    """
    Validate that a detected zoom region is correct.

    Args:
        low_mag_img: Low magnification image
        high_mag_img: High magnification image
        box: (x1, y1, x2, y2) detected bounding box
        threshold: Minimum correlation for valid match. Default: 0.3

    Returns:
        dict: {'valid': bool, 'correlation': float, 'message': str}
    """
    x1, y1, x2, y2 = box

    # Extract region from low-mag
    region = low_mag_img[y1:y2, x1:x2]

    if region.size == 0:
        return {
            'valid': False,
            'correlation': 0,
            'message': 'Empty region - box outside image bounds'
        }

    # Resize high-mag to match region size
    try:
        from skimage.transform import resize
        high_resized = resize(high_mag_img, region.shape)
    except ImportError:
        high_resized = _downsample(high_mag_img,
                                   high_mag_img.shape[0] / region.shape[0])

    # Compute correlation
    region_norm = (region - np.mean(region)) / (np.std(region) + 1e-8)
    high_norm = (high_resized - np.mean(high_resized)) / (np.std(high_resized) + 1e-8)

    correlation = np.mean(region_norm * high_norm)

    valid = correlation > threshold

    return {
        'valid': valid,
        'correlation': correlation,
        'message': 'Match validated' if valid else f'Correlation {correlation:.3f} below threshold {threshold}'
    }
