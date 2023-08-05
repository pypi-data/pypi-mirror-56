"""
FeersumNLU Image Encoder: Encode image with Resnet.
"""

import binascii
from PIL import Image
import logging

import numpy as np
import torch
import torch.utils

from torchvision import models

from feersum_nlu.models import pytorch_utils
from feersum_nlu import image_utils
from feersum_nlu.models import image_encoder_base


class ImageEncoderResnet(image_encoder_base.ImageEncoderBase):
    """
    FeersumNLU Image Encoder: Encode image with Resnet.
    """
    torchvision_resnets = \
        {
            'resnet18': models.resnet18,
            'resnet34': models.resnet34,
            'resnet50': models.resnet50,
            'resnet101': models.resnet101,
            'resnet152': models.resnet152
        }

    def __init__(self, resnet_name: str = 'resnet152') -> None:
        super().__init__()

        # check if CUDA is available
        self._cuda_is_available = torch.cuda.is_available()

        torch.set_num_threads(4)  # pylint: disable=no-member

        self._is_created = False

        resnet = ImageEncoderResnet.torchvision_resnets.get(resnet_name, models.resnet152)

        self._model = resnet(pretrained=True)
        self._vect_dim = self._model.fc.in_features
        self._model.fc = pytorch_utils.IdentityHead()

        if self._model is not None:
            # Freeze the pre-trained layers of the pre-trained network.
            for param in self._model.parameters():
                param.requires_grad = False

            if self._cuda_is_available:
                self._model.cuda()

            self._is_created = True

    # ToDo: Add set and get state methods that prevent the resnet from being pickled with the object.

    def is_created(self) -> bool:
        """Return True if the encoder was instantiated properly."""
        return self._is_created

    def get_vect_dim(self) -> int:
        """Return the manifold dimension."""
        return self._vect_dim

    def calc_pil_image_vector(self, input_image: Image) -> np.array:
        if self._model is not None:
            # Normalise the image for the neural net.
            np_image = pytorch_utils.process_image(input_image)
            torch_image = torch.as_tensor(np_image).view((1, 3, 224, 224))  # pylint: disable=no-member

            # Set the model to eval/run mode.
            self._model.eval()

            if self._cuda_is_available:
                torch_image = torch_image.cuda()
                self._model.cuda()

            output = self._model(torch_image)

            if self._cuda_is_available:
                output = output.cpu()

            np_output = output.numpy()[0]

            return np_output
        else:
            return np.zeros(self._vect_dim)

    def calc_image_vector(self, input_image: str) -> np.array:
        try:
            # Decode the image - The code later on assumes the image is 256x256 RGB! Format ensured in service wrapper.
            pil_image = image_utils._base64_decode_to_pil_image(input_image)

            if pil_image is None:
                logging.error("image_encoder_resnet.calc_image_vector - pil_image is None.")
                return np.zeros(self._vect_dim)

            return self.calc_pil_image_vector(pil_image)
        except (UnicodeError, binascii.Error, IOError):
            return np.zeros(self._vect_dim)
