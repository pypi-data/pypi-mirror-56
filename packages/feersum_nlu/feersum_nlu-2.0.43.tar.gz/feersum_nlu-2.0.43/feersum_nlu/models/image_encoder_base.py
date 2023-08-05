"""
FeersumNLU Image Encoder: Base class.
"""

from abc import ABC, abstractmethod
import numpy as np
from PIL import Image


class ImageEncoderBase(ABC):
    """
    FeersumNLU Image Encoder: Base class.
    """

    def __init__(self) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.

    @abstractmethod
    def is_created(self) -> bool:
        """Return True if the encoder was instantiated properly."""
        pass

    @abstractmethod
    def get_vect_dim(self) -> int:
        """Return the encoded vector dimension."""
        pass

    @abstractmethod
    def calc_image_vector(self, input_image: str) -> np.array:
        pass

    @abstractmethod
    def calc_pil_image_vector(self, input_image: Image) -> np.array:
        pass

    # ===================================
    # === Common class helper methods ===
    # ===================================
    @staticmethod
    def get_nvect(vect: np.array):
        norm = np.linalg.norm(vect)

        if norm != 0.0:
            return vect / norm
        else:
            return np.zeros(vect.shape)

    @staticmethod
    def calc_cosine_dist(vect_a: np.array, vect_b: np.array) -> float:
        """ Return the cosine distance between vect_a and vect_b. returns vect_a.vect_b/(|vect_a|*|vect_b|)
        -1.0 = dissimilar, 1.0 = similar. """
        vect_a_length = np.linalg.norm(vect_a)
        vect_b_length = np.linalg.norm(vect_b)

        if vect_a_length != 0.0 and vect_b_length != 0.0:
            score = np.dot(vect_a, vect_b) / (vect_a_length * vect_b_length)
        else:
            score = 0.0

        return score

    @staticmethod
    def calc_l1_dist(vect_a: np.array, vect_b: np.array) -> float:
        """ Return the L1 distance between vect_a and vect_b. returns sum_reduce(abs(vect_a - vect_b))
        0.0 = similar, larger = dissimilar. """
        # return np.linalg.norm(vect_a - vect_b, ord=1)  # SLOWER; 150% the time of below version.
        return np.sum(np.abs(vect_a - vect_b))  # FASTER

    @staticmethod
    def calc_l2_dist(vect_a: np.array, vect_b: np.array) -> float:
        """ Return the L1 distance between vect_a and vect_b. returns |vect_a - vect_b|
        0.0 = similar, larger = dissimilar. """
        diff = vect_a - vect_b
        return np.dot(diff, diff)
