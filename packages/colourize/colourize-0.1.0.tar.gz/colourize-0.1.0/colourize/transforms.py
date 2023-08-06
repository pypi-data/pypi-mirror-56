import colour
import numpy as np

from skimage.color import rgb2hed
from colour.utilities import from_range_int, suppress_warnings
import torchvision.transforms.functional as F


class ConvertColorspace():
    """Convert RGB image to a given colorspace.

    Scales image to value range [0, 1].
    """
    def __init__(self, tospace, fromspace='sRGB'):
        self.fromspace = fromspace.lower()
        self.tospace = tospace.lower()

    def __call__(self, img):
        """
        Args:
            img (NumPy array):

        Returns:
        """
        if self.tospace == 'hed':
            img = rgb2hed(img)
        else:
            with colour.domain_range_scale('1'):
                img = from_range_int(img)
                with suppress_warnings(colour_usage_warnings=True):
                    img = colour.convert(img, self.fromspace, self.tospace)
        return np.float32(img)

    def __repr__(self):
        return self.__class__.__name__  # FIXME + '(p={})'.format(self.p)


class ToArray():
    """Convert a PIL Image to a NumPy array.
    """
    def __call__(self, img):
        return np.asarray(img)


class ToTensor():
    """Convert a ``PIL Image`` or ``numpy.ndarray`` to tensor.

    Converts a PIL Image or numpy.ndarray (H x W x C) in the range
    [0, 255] to a torch.FloatTensor of shape (C x H x W) in the range
    [0.0, 1.0] if the PIL Image belongs to one of the modes
    (L, LA, P, I, F, RGB, YCbCr, RGBA, CMYK, 1) or if the numpy.ndarray
    has dtype = np.uint8

    In the other cases, tensors are returned without scaling.
    """
    def __call__(self, img):
        """
        Args:
            img(PIL Image or numpy.ndarray): Image to be converted to tensor.

        Returns:
            Tensor: Converted image.
        """
        return F.to_tensor(img)

    def __repr__(self):
        return self.__class__.__name__ + '()'
