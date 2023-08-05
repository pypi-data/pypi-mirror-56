"""
FeersumNLU Image Classifier: Fully connected neural network classifier; Uses Feersum vision_model.
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
from feersum_nlu.models import image_classifier_base
from feersum_nlu.models import pytorch_utils
from feersum_nlu import image_utils


class ImageClassifierFCNN(image_classifier_base.ImageClassifierBase):
    """
    FeersumNLU Classifier: Fully connected neural network classifier.
    """

    def __init__(self, vision_model: Optional[ImageEncoderBase]) -> None:
        super().__init__(vision_model=vision_model)

        # check if CUDA is available
        self._cuda_is_available = torch.cuda.is_available()

        self._next_label_idx = 0
        self._idx_to_label = {}  # type: Dict[int, str]
        self._classifier_model = None  # type: Optional[pytorch_utils.ClassifierHead]

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
                     training_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
                     testing_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
                     report_progress: bool = False) -> bool:
        """
        Provide online training samples that are used to immediately update the model.

        :param training_list: List of labelled samples (image, label). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of labelled samples (image, label) to test accuracy & overfit during training.
        :param report_progress: Reports on the progress during training.
        :return: True if training was successful.
        """
        # Online training not supported yet.
        return False

    def train(self,
              training_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
              testing_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
              num_epochs: int) -> bool:
        """
        Reset and train the classifier with image-label pairs

        :param training_list: List of labelled samples (image, label). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of labelled samples (image, label) to test accuracy & overfit during training.
        :param num_epochs: The number of epochs to train the model for.
        :return: Boolean indicating whether or not the training was successful.
        """
        self._labels.clear()
        self._label_to_idx.clear()

        self._next_label_idx = 0
        self._idx_to_label.clear()
        self._classifier_model = None

        vision_model = self.get_vision_model()

        if vision_model is None:
            logging.error("image_classifier_fcnn.train - _language_model_dict is None!")
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

            datasets = {'train': pytorch_utils.VisionClassDataset(transform=data_transforms['train']),
                        'valid': pytorch_utils.VisionClassDataset(transform=data_transforms['valid'])}

            sample_lists = {'train': training_list,
                            'valid': testing_list if len(testing_list) > 0 else training_list}

            # === Update the _labels set, the _label_to_idx mapping AND the datasets ===
            for sample_type in ['train', 'valid']:
                for sample in sample_lists[sample_type]:
                    try:
                        label = sample[1]
                        self._labels.add(label)
                        if self._label_to_idx.get(label) is None:
                            self._label_to_idx[label] = self._next_label_idx
                            self._next_label_idx += 1

                        # Decode the image - assumes the image is 256x256 RGB.
                        pil_image = image_utils._base64_decode_to_pil_image(sample[0])
                        if pil_image is not None:
                            datasets[sample_type].add_image(self._label_to_idx[label], pil_image)

                    except (UnicodeError, binascii.Error, IOError):
                        continue  # Ignore the sample.

            self._idx_to_label = {v: k for k, v in self._label_to_idx.items()}

            # === Create the data loaders ===
            batch_size = 32

            sample_weights = pytorch_utils.make_weights_for_balancing_classes(datasets['train'].data_samples,
                                                                              len(datasets['train'].label_idxs))
            balancing_sampler = torch.utils.data.WeightedRandomSampler(sample_weights,
                                                                       len(sample_weights))

            dataloaders = {'train': DataLoader(datasets['train'], batch_size=batch_size, sampler=balancing_sampler),
                           # 'train': DataLoader(datasets['train'], batch_size=batch_size, shuffle=True),
                           'valid': DataLoader(datasets['valid'], batch_size=batch_size, shuffle=False)}

            # === Setup the model, loss function and the optimizer ===
            self._classifier_model = pytorch_utils.ClassifierHead(vision_model.get_vect_dim(), len(self._labels))

            if self._cuda_is_available:
                self._classifier_model.cuda()

            # Specify loss function (categorical cross-entropy).
            criterion = nn.NLLLoss()

            # Specify optimizer.
            # optimizer = optim.SGD(self._classifier_model.parameters(), lr=0.001, momentum=0.9, weight_decay=0.001)
            optimizer = optim.Adam(self._classifier_model.parameters(), lr=0.001, weight_decay=0.0001)

            # === Train loop ===
            valid_loss_min = np.Inf
            valid_acc_max = 0.0

            for epoch in range(1, num_epochs + 1):
                print(f"Epoch {epoch}:")

                # Training ...
                self._classifier_model.train()
                train_loss_sum = 0.0
                train_correct_count = 0.0

                for batch_idx, (label_idxs, images) in enumerate(dataloaders['train']):
                    optimizer.zero_grad()

                    if self._cuda_is_available:
                        images, label_idxs = images.cuda(), label_idxs.cuda()

                    with torch.set_grad_enabled(True):
                        outputs = self._classifier_model(images)
                        loss = criterion(outputs, label_idxs)
                        loss.backward()
                        optimizer.step()

                    train_loss_sum += loss.item() * images.size(0)

                    _, predicted_label_idxs = torch.max(outputs, -1)  # pylint: disable=no-member
                    train_correct_count += (predicted_label_idxs == label_idxs).double().sum().item()

                train_loss = train_loss_sum / len(dataloaders['train'].dataset)
                print('   Training loss = {:.6f}'.format(train_loss), flush=True, end='')

                train_acc = train_correct_count / len(dataloaders['train'].dataset)
                print(' [acc = {:.2f}]'.format(train_acc), flush=True)

                # Validation ...
                self._classifier_model.eval()
                valid_loss_sum = 0.0
                valid_correct_count = 0.0

                for batch_idx, (label_idxs, images) in enumerate(dataloaders['valid']):
                    if self._cuda_is_available:
                        images, label_idxs = images.cuda(), label_idxs.cuda()

                    with torch.set_grad_enabled(True):
                        outputs = self._classifier_model(images)
                        loss = criterion(outputs, label_idxs)

                    valid_loss_sum += loss.item() * images.size(0)

                    _, predicted_label_idxs = torch.max(outputs, -1)  # pylint: disable=no-member
                    valid_correct_count += (predicted_label_idxs == label_idxs).double().sum().item()

                valid_loss = valid_loss_sum / len(dataloaders['valid'].dataset)
                print('   Validation loss = {:.6f}'.format(valid_loss), flush=True, end='')

                valid_acc = valid_correct_count / len(dataloaders['valid'].dataset)
                print(' [acc = {:.2f}]'.format(valid_acc), flush=True)

                if (valid_loss < valid_loss_min) or (
                        (valid_loss == valid_loss_min) and (valid_acc >= valid_acc_max)):
                    print('     Validation loss decreased ({:.6f} --> {:.6f}). Saving model.'.format(valid_loss_min,
                                                                                                     valid_loss))
                    torch.save(self._classifier_model.state_dict(), 'state_dict_best_valid_loss.pt')
                    valid_loss_min = valid_loss
                    valid_acc_max = valid_acc

            # === Load the model that performed the best during training ===
            print("Loading the best performing model...", flush=True, end='')
            self._classifier_model.load_state_dict(torch.load('state_dict_best_valid_loss.pt'))
            print("done.")

            self._classifier_model.eval()

        return True

    def classify(self, input_image: str,
                 weak_match_threshold: float,
                 top_n: int) -> List[Tuple[str, float]]:
        """ Find the n best matches to the input image.

        :param input_image: The image to classify. Image formatted as utf8 encoded base64 string.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number (i.e. k) of sorted matches to return.
        :return: Sorted list of scored labels [(str, float)].
        """
        if self._classifier_model is None:
            logging.error("image_classifier_fcnn.classify - _classifier_model is None!")
            return []

        vision_model = self.get_vision_model()

        if vision_model is None:
            logging.error("image_classifier_fcnn.classify - vision_model is None!")
            return []

        try:
            # Decode the image - The code later on assumes the image is 256x256 RGB! Format ensured in service wrapper.
            pil_image = image_utils._base64_decode_to_pil_image(input_image)

            if pil_image is None:
                logging.error("image_classifier_fcnn.classify - pil_image is None!")
                return []

            # Normalise the image for the neural net.
            np_vector = vision_model.calc_pil_image_vector(pil_image)

            torch_vector = torch.as_tensor(np_vector).view((1, vision_model.get_vect_dim()))  # pylint: disable=no-member

            # Run the model
            self._classifier_model.eval()

            if self._cuda_is_available:
                torch_vector = torch_vector.cuda()
                self._classifier_model.cuda()

            output = self._classifier_model(torch_vector).cpu()

            top_k = min(top_n, output.shape[1])
            output_tensor, labels_idxs_tensor = output.topk(top_k)

            probs = np.exp(output_tensor.view(top_k).detach().numpy()).tolist()
            class_idxs = labels_idxs_tensor.view(top_k).detach().numpy().tolist()
            class_labels = [self._idx_to_label[idx] for idx in class_idxs]

            return list(zip(class_labels, probs))
        except (UnicodeError, binascii.Error, IOError):
            return []
