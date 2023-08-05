"""
FeersumNLU Image Regressor: Fully connected neural network regressor; Uses Feersum vision_model.
"""

from typing import Tuple, List, Union, Optional, Dict  # noqa # pylint: disable=unused-import

import binascii
import PIL
import logging

import numpy as np
import torch
import torch.utils
from torch.utils.data import DataLoader

from torch import nn
from torch import optim
from torchvision import transforms

from feersum_nlu.models.image_encoder_base import ImageEncoderBase
from feersum_nlu.models import image_regressor_base
from feersum_nlu.models import pytorch_utils
from feersum_nlu import image_utils


class ImageRegressorFCNN(image_regressor_base.ImageRegressorBase):
    """
    FeersumNLU Classifier: Fully connected neural network regressor.
    """
    # ToDo: Review https://www.cv-foundation.org/openaccess/content_iccv_2015_workshops/w11/papers/...
    #    Escalera_ChaLearn_Looking_at_ICCV_2015_paper.pdf
    # ToDo: Review https://www.vision.ee.ethz.ch/en/publications/papers/proceedings/eth_biwi_01229.pdf
    # Finetuning the entire network on the problem seems to get the e score (described in paper) down to 0.43. Without
    # fine-tuning I get around 0.5.

    def __init__(self, vision_model: Optional[ImageEncoderBase]) -> None:
        super().__init__(vision_model=vision_model)

        # check if CUDA is available
        self._cuda_is_available = torch.cuda.is_available()

        self._regressor_model = None  # type: Optional[pytorch_utils.RegressorHead]

    def __getstate__(self):
        """Do not pickle the _vision_model with this object!"""
        # ToDo: call base class' __getstate__
        state = self.__dict__.copy()  # ToDo: how much time is wasted in copying the vision model!?
        del state['_vision_model']
        return state

    def __setstate__(self, state):
        """_language_model_dict not pickled with the object!"""
        # ToDo: call base class' __setstate__
        self.__dict__.update(state)
        self._vision_model = None

    def train_online(self,
                     training_list: Union[List[Tuple[str, float]], List[Tuple[str, float, str]]],
                     testing_list: Union[List[Tuple[str, float]], List[Tuple[str, float, str]]],
                     report_progress: bool = False) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param training_list: List of samples with values (image, float). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of samples with values (image, float) to test accuracy & overfit during training.
        :param report_progress: Reports on the progress during training.
        :return: True if training was successful.
        """
        # Online training not supported yet.
        return False

    def train(self,
              training_list: Union[List[Tuple[str, float]], List[Tuple[str, float, str]]],
              testing_list: Union[List[Tuple[str, float]], List[Tuple[str, float, str]]],
              num_epochs: int) -> bool:
        """
        Reset and train the regressor with image-value pairs

        :param training_list: List of samples with values (image, float). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of samples with values (image, float) to test accuracy & overfit during training.
        :param num_epochs: The number of epochs to train the model for.
        :return: Boolean indicating whether or not the training was successful.
        """
        self._regressor_model = None

        vision_model = self.get_vision_model()

        if vision_model is None:
            logging.error("image_regressor_fcnn.train - vision_model is None.")
            return False

        if len(training_list) > 0:
            # === Load pretrained model ===
            torch.set_num_threads(4)  # pylint: disable=no-member

            # === Init datasets ===
            data_transforms = {'train': transforms.Compose([transforms.RandomHorizontalFlip(),
                                                            transforms.RandomVerticalFlip(),
                                                            transforms.RandomRotation(45.0, resample=PIL.Image.BILINEAR),
                                                            transforms.CenterCrop(224),
                                                            pytorch_utils.EncodeTransform(vision_model)]),
                               'valid': transforms.Compose([transforms.CenterCrop(224),
                                                            pytorch_utils.EncodeTransform(vision_model)])}

            datasets = {'train': pytorch_utils.VisionRegressDataset(transform=data_transforms['train']),
                        'valid': pytorch_utils.VisionRegressDataset(transform=data_transforms['valid'])}

            sample_lists = {'train': training_list,
                            'valid': testing_list if len(testing_list) > 0 else training_list}

            # === Update the datasets ===
            for sample_type in ['train', 'valid']:
                for sample in sample_lists[sample_type]:
                    try:
                        target_value = sample[1]

                        # Decode the image - assumes the image is 256x256 RGB.
                        pil_image = image_utils._base64_decode_to_pil_image(sample[0])
                        if pil_image is not None:
                            datasets[sample_type].add_image(target_value, pil_image)

                    except (UnicodeError, binascii.Error, IOError):
                        continue  # Ignore the sample.

            # === Create the data loaders ===
            batch_size = 32

            dataloaders = {'train': DataLoader(datasets['train'], batch_size=batch_size, shuffle=True),
                           'valid': DataLoader(datasets['valid'], batch_size=batch_size, shuffle=False)}

            # === Setup the model, loss function and the optimizer ===
            self._regressor_model = pytorch_utils.RegressorHead(vision_model.get_vect_dim(), 1)

            if self._cuda_is_available:
                self._regressor_model.cuda()

            # Specify loss function (mean squared error).
            criterion = nn.MSELoss()

            # Specify optimizer.
            # optimizer = optim.SGD(self._regressor_model.parameters(), lr=0.0001)
            # optimizer = optim.SGD(self._regressor_model.parameters(), lr=0.0001, momentum=0.5, weight_decay=0.0001)
            # optimizer = optim.SGD(self._regressor_model.parameters(), lr=0.0001, momentum=0.9, weight_decay=0.001)
            optimizer = optim.Adam(self._regressor_model.parameters(), lr=0.001, weight_decay=0.0001)

            # === Train loop ===
            valid_loss_min = np.Inf

            for epoch in range(1, num_epochs + 1):
                print(f"Epoch {epoch}:")

                # Training ...
                self._regressor_model.train()
                train_loss_sum = 0.0

                for batch_idx, (target_values, images) in enumerate(dataloaders['train']):
                    optimizer.zero_grad()

                    if self._cuda_is_available:
                        images, target_values = images.cuda(), target_values.cuda()

                    with torch.set_grad_enabled(True):
                        outputs = self._regressor_model(images).view(-1)
                        loss = criterion(outputs, target_values)
                        loss.backward()
                        optimizer.step()

                    train_loss_sum += loss.item() * images.size(0)

                train_loss = train_loss_sum / len(dataloaders['train'].dataset)
                print('   Training loss = {:.6f}'.format(train_loss), flush=True, end='')

                # Validation ...
                self._regressor_model.eval()
                valid_loss_sum = 0.0

                for batch_idx, (target_values, images) in enumerate(dataloaders['valid']):
                    if self._cuda_is_available:
                        images, target_values = images.cuda(), target_values.cuda()

                    with torch.set_grad_enabled(True):
                        outputs = self._regressor_model(images).view(-1)
                        loss = criterion(outputs, target_values)

                    valid_loss_sum += loss.item() * images.size(0)

                valid_loss = valid_loss_sum / len(dataloaders['valid'].dataset)
                print('   Validation loss = {:.6f}'.format(valid_loss), flush=True)

                if valid_loss < valid_loss_min:
                    print('     Validation loss decreased ({:.6f} --> {:.6f}). Saving model.'.format(valid_loss_min,
                                                                                                     valid_loss))
                    torch.save(self._regressor_model.state_dict(), 'state_dict_best_valid_loss.pt')
                    valid_loss_min = valid_loss

            # === Load the model that performed the best during training ===
            print("Loading the best performing model...", flush=True, end='')
            self._regressor_model.load_state_dict(torch.load('state_dict_best_valid_loss.pt'))
            print("done.")

            self._regressor_model.eval()

        return True

    def estimate(self, input_image: str) -> float:
        """ Run the regression model.

        :param input_image: The input image to the estimator model. Image formatted as utf8 encoded base64 string.
        :return: The model estimate.
        """
        if self._regressor_model is None:
            return 0.0

        vision_model = self.get_vision_model()

        if vision_model is None:
            logging.error("image_regressor_fcnn.estimate - vision_model is None.")
            return 0.0

        try:
            # Decode the image - The code later on assumes the image is 256x256 RGB! Format ensured in service wrapper.
            pil_image = image_utils._base64_decode_to_pil_image(input_image)

            if pil_image is None:
                return 0.0

            # Normalise the image for the neural net.
            np_vector = vision_model.calc_pil_image_vector(pil_image)

            torch_vector = torch.as_tensor(np_vector).view((1, vision_model.get_vect_dim()))  # pylint: disable=no-member

            # Run the model
            self._regressor_model.eval()

            if self._cuda_is_available:
                torch_vector = torch_vector.cuda()
                self._regressor_model.cuda()

            output = self._regressor_model(torch_vector).cpu()

            return output.item()
        except (UnicodeError, binascii.Error, IOError):
            return 0.0
