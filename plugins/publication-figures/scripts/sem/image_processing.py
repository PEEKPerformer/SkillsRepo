"""
SEM image loading and enhancement functions.

Provides utilities for loading TIFF images and applying contrast enhancements
suitable for publication-quality SEM figures.
"""

import numpy as np


def load_sem_tiff(filepath, crop_info_bar=True, crop_y=875):
    """
    Load an SEM TIFF image and optionally crop the info bar.

    SEM images typically have an info bar at the bottom containing
    metadata (scale bar, magnification, etc.). This function can
    automatically crop it.

    Args:
        filepath: Path to TIFF file
        crop_info_bar: Whether to crop the info bar. Default: True
        crop_y: Y coordinate to crop at. Default: 875 (for 1024x943 images)

    Returns:
        numpy array: Image data (grayscale, 0-1 float)
    """
    from PIL import Image

    img = Image.open(filepath)
    img_array = np.array(img, dtype=np.float32)

    # Normalize to 0-1
    if img_array.max() > 1:
        img_array = img_array / 255.0

    if crop_info_bar and crop_y < img_array.shape[0]:
        img_array = img_array[:crop_y, :]

    return img_array


def apply_gamma(img, gamma=0.85):
    """
    Apply gamma correction to lift shadows.

    Gamma < 1 brightens dark areas (shadow lift).
    Gamma > 1 darkens the image.

    Args:
        img: Image array (0-1 float)
        gamma: Gamma value. Default: 0.85 (slight shadow lift)

    Returns:
        numpy array: Gamma-corrected image
    """
    img = np.asarray(img, dtype=np.float32)
    img = np.clip(img, 0, 1)
    return np.power(img, gamma)


def apply_clahe(img, clip_limit=0.02, grid_size=(8, 8)):
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE).

    CLAHE enhances local contrast without over-amplifying noise.
    Useful for revealing detail under bright particles on dark backgrounds.

    Args:
        img: Image array (0-1 float)
        clip_limit: Clipping limit for contrast limiting. Default: 0.02
        grid_size: Size of grid for histogram equalization. Default: (8, 8)

    Returns:
        numpy array: CLAHE-enhanced image
    """
    try:
        from skimage.exposure import equalize_adapthist
        return equalize_adapthist(img, clip_limit=clip_limit)
    except ImportError:
        # Fallback: simple histogram equalization
        print("Warning: skimage not available, using simple histogram equalization")
        from PIL import Image
        img_uint8 = (img * 255).astype(np.uint8)
        pil_img = Image.fromarray(img_uint8)
        # Simple equalization as fallback
        return np.array(pil_img) / 255.0


def enhance_sem_image(img, method='auto', **kwargs):
    """
    Automatically enhance an SEM image for publication.

    Args:
        img: Image array (0-1 float)
        method: Enhancement method ('gamma', 'clahe', 'auto', 'none')
        **kwargs: Additional arguments for the enhancement function

    Returns:
        numpy array: Enhanced image
    """
    if method == 'none':
        return img

    # Analyze image statistics
    mean_val = np.mean(img)
    std_val = np.std(img)

    if method == 'auto':
        # High contrast (bright particles): use CLAHE
        if std_val > 0.25:
            method = 'clahe'
        # Dark image: use gamma
        elif mean_val < 0.4:
            method = 'gamma'
        else:
            return img  # No enhancement needed

    if method == 'gamma':
        gamma = kwargs.get('gamma', 0.85)
        return apply_gamma(img, gamma)
    elif method == 'clahe':
        clip_limit = kwargs.get('clip_limit', 0.02)
        return apply_clahe(img, clip_limit)
    else:
        return img


def get_image_info(filepath):
    """
    Get metadata about an SEM image file.

    Args:
        filepath: Path to image file

    Returns:
        dict: Image information (size, dtype, min, max, mean)
    """
    from PIL import Image

    img = Image.open(filepath)
    img_array = np.array(img)

    return {
        'size': img.size,  # (width, height)
        'shape': img_array.shape,
        'dtype': str(img_array.dtype),
        'min': float(img_array.min()),
        'max': float(img_array.max()),
        'mean': float(img_array.mean()),
        'mode': img.mode,
    }
