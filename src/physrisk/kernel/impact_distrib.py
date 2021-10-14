import numpy as np
from typing import List, Union

from physrisk.kernel.exceedance_curve import ExceedanceCurve

class ImpactDistrib:
    """Impact distributions specific to an asset."""
    
    __slots__ = ["__event_type", "__impact_bins", "__prob"]
    
    def __init__(self,
        event_type: type,
        impact_bins: Union[List[float], np.ndarray],   
        prob: Union[List[float], np.ndarray]):
        """Create a new asset event distribution.
        Args:
            event_type: type of event
            impact_bins: non-decreasing impact bin bounds
            prob: probabilities with size [len(intensity_bins) - 1] 
        """
        self.__event_type = event_type
        self.__impact_bins = np.array(impact_bins) 
        self.__prob = np.array(prob)

    def impact_bins_explicit(self):
        return zip(self.__impact_bins[0:-1], self.__impact_bins[1:])

    def mean_impact(self):
        return np.sum((self.__impact_bins[:-1] + self.__impact_bins[1:]) * self.__prob / 2)

    def to_exceedance_curve(self):
        nz = np.asarray(self.__prob > 0).nonzero()
        fnz = nz[0][0] if len(nz[0]) > 0 else 0
        values = self.__impact_bins[fnz:]
        prob = self.__prob[fnz:]
        cum_prob = np.insert(np.cumsum(prob[::-1]), 0, 0.0)[::-1]
        return ExceedanceCurve(cum_prob, values)

    @property
    def impact_bins(self) -> np.ndarray:
        return self.__impact_bins

    @property
    def prob(self) -> np.ndarray:
        return self.__prob