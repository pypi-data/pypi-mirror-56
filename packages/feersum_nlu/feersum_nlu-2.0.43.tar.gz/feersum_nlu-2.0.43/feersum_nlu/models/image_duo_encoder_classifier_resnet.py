"""
FeersumNLU Classifier: Torchvision Resnet encoder & classifier; NOT using Feersum vision_model.
"""

from typing import Tuple, List, Dict, Union, Optional  # noqa # pylint: disable=unused-import

import binascii
import PIL
import logging

import numpy as np
import torch
import torch.utils
from torch.utils.data import DataLoader

from torch import nn
from torch import optim
from torchvision import transforms, models

from feersum_nlu.models import image_classifier_base
from feersum_nlu.models import pytorch_utils
from feersum_nlu import image_utils


class ImageDuoEncoderClassifierResnet(image_classifier_base.ImageClassifierBase):
    """
    FeersumNLU Image Classifier: Torchvision Resnet encoder & classifier.
    """

    def __init__(self) -> None:
        super().__init__()

        # check if CUDA is available
        self._cuda_is_available = torch.cuda.is_available()

        self._next_label_idx = 0
        self._idx_to_label = {}  # type: Dict[int, str]
        self._model = None  # type: Optional[models.ResNet]
        # REMEMBER to add new attributes to __getstate__ and __setstate__ !!!

    def __getstate__(self):
        """ For pickling super & child states without 'model', but with 'model.fc'. """
        super_state = super().__getstate__()

        if self._model is not None:
            model_fc_state_dict = self._model.fc.state_dict()
        else:
            model_fc_state_dict = None

        child_state = {
            '_next_label_idx': self._next_label_idx,
            '_idx_to_label': self._idx_to_label,
            'model_fc_state_dict': model_fc_state_dict
        }

        return super_state, child_state

    def __setstate__(self, state):
        """ For unpickling super & child states without 'model', but with 'model.fc'. """
        super_state, child_state = state
        super().__setstate__(super_state)

        # check if CUDA is available
        self._cuda_is_available = torch.cuda.is_available()

        self._next_label_idx = child_state['_next_label_idx']
        self._idx_to_label = child_state['_idx_to_label']

        if child_state['model_fc_state_dict'] is not None:
            # Load pretrained model.
            self._model = models.resnet152(pretrained=True)

            # Freeze the pre-trained layers of the pre-trained network.
            for param in self._model.parameters():
                param.requires_grad = False

            self._model.fc = pytorch_utils.ClassifierHead(self._model.fc.in_features, len(self._labels))
            self._model.fc.load_state_dict(child_state['model_fc_state_dict'])

            self._model.eval()
        else:
            self._model = None

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
        Reset and train the classifier with expression-label pairs

        :param training_list: List of labelled samples (image, label). Image formatted as utf8 encoded base64 string.
        :param testing_list: List of labelled samples (image, label) to test accuracy & overfit during training.
        :param num_epochs: The number of epochs to train the model for.
        :return: Boolean indicating whether or not the training was successful.
        """
        self._labels.clear()
        self._label_to_idx.clear()

        self._next_label_idx = 0
        self._idx_to_label.clear()
        self._model = None

        if len(training_list) > 0:
            # === Load pretrained model ===
            torch.set_num_threads(4)  # pylint: disable=no-member

            self._model = models.resnet152(pretrained=True)

            if self._model is not None:
                # Freeze the pre-trained layers of the pre-trained network.
                for param in self._model.parameters():
                    param.requires_grad = False

                # === Init datasets ===
                norm_mean = [0.485, 0.456, 0.406]  # ImageNet norm.
                norm_std = [0.229, 0.224, 0.225]  # ImageNet std.

                data_transforms = {'train': transforms.Compose([transforms.RandomHorizontalFlip(),
                                                                transforms.RandomVerticalFlip(),
                                                                transforms.RandomRotation(45.0, resample=PIL.Image.BILINEAR),
                                                                transforms.CenterCrop(224),
                                                                transforms.ToTensor(),
                                                                transforms.Normalize(norm_mean, norm_std)]),
                                   'valid': transforms.Compose([transforms.CenterCrop(224),
                                                                transforms.ToTensor(),
                                                                transforms.Normalize(norm_mean, norm_std)])}

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
                self._model.fc = pytorch_utils.ClassifierHead(self._model.fc.in_features, len(self._labels))

                if self._cuda_is_available:
                    self._model.cuda()

                # Specify loss function (categorical cross-entropy).
                criterion = nn.NLLLoss()

                # Specify optimizer.
                # optimizer = optim.SGD(self._model.parameters(), lr=0.001, momentum=0.9, weight_decay=0.001)
                optimizer = optim.Adam(self._model.parameters(), lr=0.001, weight_decay=0.0001)

                # === Train loop ===
                valid_loss_min = np.Inf
                valid_acc_max = 0.0

                for epoch in range(1, num_epochs + 1):
                    print(f"Epoch {epoch}:")

                    # Training ...
                    self._model.train()
                    train_loss_sum = 0.0
                    train_correct_count = 0.0

                    for batch_idx, (label_idxs, images) in enumerate(dataloaders['train']):
                        optimizer.zero_grad()

                        if self._cuda_is_available:
                            images, label_idxs = images.cuda(), label_idxs.cuda()

                        with torch.set_grad_enabled(True):
                            outputs = self._model(images)
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
                    self._model.eval()
                    valid_loss_sum = 0.0
                    valid_correct_count = 0.0

                    for batch_idx, (label_idxs, images) in enumerate(dataloaders['valid']):
                        if self._cuda_is_available:
                            images, label_idxs = images.cuda(), label_idxs.cuda()

                        with torch.set_grad_enabled(True):
                            outputs = self._model(images)
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
                        torch.save(self._model.state_dict(), 'state_dict_best_valid_loss.pt')
                        valid_loss_min = valid_loss
                        valid_acc_max = valid_acc

                # === Load the model that performed the best during training ===
                print("Loading the best performing model...", flush=True, end='')
                self._model.load_state_dict(torch.load('state_dict_best_valid_loss.pt'))
                print("done.")

                self._model.eval()

            return True
        else:
            return False

    def classify(self, input_image: str,
                 weak_match_threshold: float,
                 top_n: int) -> List[Tuple[str, float]]:
        """ Find the n best matches to the input image.

        :param input_image: The image to classify. Image formatted as utf8 encoded base64 string.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number (i.e. k) of sorted matches to return.
        :return: Sorted list of scored labels [(str, float)].
        """
        if self._model is not None:
            try:
                # Decode the image - The code later on assumes the image is 256x256 RGB! Format ensured in service wrapper.
                pil_image = image_utils._base64_decode_to_pil_image(input_image)

                if pil_image is None:
                    logging.error("image_duo_encoder_classifier_resnet.classify - pil_image is None.")
                    return []

                # Normalise the image for the neural net.
                np_image = pytorch_utils.process_image(pil_image)

                torch_image = torch.as_tensor(np_image).view((1, 3, 224, 224))  # pylint: disable=no-member

                # Set the model to eval/run mode.
                self._model.eval()

                if self._cuda_is_available:
                    torch_image = torch_image.cuda()
                    self._model.cuda()

                output = self._model(torch_image).cpu()

                top_k = min(top_n, output.shape[1])
                output_tensor, labels_idxs_tensor = output.topk(top_k)

                probs = np.exp(output_tensor.view(top_k).detach().numpy()).tolist()
                class_idxs = labels_idxs_tensor.view(top_k).detach().numpy().tolist()
                class_labels = [self._idx_to_label[idx] for idx in class_idxs]

                return list(zip(class_labels, probs))
            except (UnicodeError, binascii.Error, IOError):
                return []
        else:
            return []
