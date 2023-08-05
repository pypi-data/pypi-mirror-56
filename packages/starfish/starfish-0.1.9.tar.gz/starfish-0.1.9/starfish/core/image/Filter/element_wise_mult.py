from copy import deepcopy
from typing import Optional, Union

import numpy as np
import xarray as xr

from starfish.core.imagestack.imagestack import ImageStack
from starfish.core.types import Clip
from starfish.core.util.dtype import preserve_float_range
from ._base import FilterAlgorithm


class ElementWiseMultiply(FilterAlgorithm):
    """
    Perform element-wise multiplication on the image tensor. This is useful for
    performing operations such as image normalization or field flatness correction

    Parameters
    ----------
    mult_mat : xr.DataArray
        the image is element-wise multiplied with this array
    clip_method : Union[str, Clip]
        (Default Clip.CLIP) Controls the way that data are scaled to retain skimage dtype
        requirements that float data fall in [0, 1].
        Clip.CLIP: data above 1 are set to 1, and below 0 are set to 0
        Clip.SCALE_BY_IMAGE: data above 1 are scaled by the maximum value, with the maximum
        value calculated over the entire ImageStack
    """

    def __init__(
        self, mult_array: xr.DataArray, clip_method: Union[str, Clip] = Clip.CLIP
    ) -> None:

        self.mult_array = mult_array
        if clip_method == Clip.SCALE_BY_CHUNK:
            raise ValueError("`scale_by_chunk` is not a valid clip_method for ElementWiseMultiply")
        self.clip_method = clip_method

    _DEFAULT_TESTING_PARAMETERS = {
        "mult_array": xr.DataArray(
            np.array([[[[[1]]], [[[0.5]]]]]),
            dims=('r', 'c', 'z', 'y', 'x')
        )
    }

    def run(
            self,
            stack: ImageStack,
            in_place: bool = False,
            verbose: bool = False,
            n_processes: Optional[int] = None,
            *args,
    ) -> Optional[ImageStack]:
        """Perform filtering of an image stack

        Parameters
        ----------
        stack : ImageStack
            Stack to be filtered.
        in_place : bool
            if True, process ImageStack in-place, otherwise return a new stack
        verbose : bool
            if True, report on filtering progress (default = False)
        n_processes : Optional[int]
            Number of parallel processes to devote to applying the filter. If None, defaults to
            the result of os.cpu_count(). (default None)

        Returns
        -------
        ImageStack :
            If in-place is False, return the results of filter as a new stack.  Otherwise return the
            original stack.

        """
        # Align the axes of the multipliers with ImageStack
        mult_array_aligned: np.ndarray = self.mult_array.transpose(*stack.xarray.dims).values
        if not in_place:
            stack = deepcopy(stack)
            self.run(stack, in_place=True)
            return stack

        stack.xarray.values *= mult_array_aligned
        if self.clip_method == Clip.CLIP:
            stack.xarray.values = preserve_float_range(stack.xarray.values, rescale=False)
        else:
            stack.xarray.values = preserve_float_range(stack.xarray.values, rescale=True)
        return None
