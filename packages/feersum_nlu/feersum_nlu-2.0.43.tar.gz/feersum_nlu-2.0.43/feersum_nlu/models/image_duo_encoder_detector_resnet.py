"""
FeersumNLU Detector: Torchvision Resnet encoder & detector; NOT using Feersum vision_model.
"""

from typing import Tuple, List, Dict, Optional  # noqa # pylint: disable=unused-import

import binascii
import logging

from PIL import Image
import numpy as np
import torch
import torch.utils
from torch.utils.data import DataLoader

import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from feersum_nlu.models.torchvision_references.detection import transforms
from feersum_nlu.models.torchvision_references.detection import engine
from feersum_nlu.models.torchvision_references.detection import utils

from feersum_nlu.models import image_detector_base
from feersum_nlu.models import pytorch_utils
from feersum_nlu import image_utils


# Some references:
# https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html
# https://github.com/matterport/Mask_RCNN/issues/387
# https://towardsdatascience.com/r-cnn-fast-r-cnn-faster-r-cnn-yolo-object-detection-algorithms-36d53571365e
# https://arxiv.org/abs/1703.06870
# https://arxiv.org/abs/1506.01497
# https://arxiv.org/pdf/1311.2524.pdf
# https://arxiv.org/pdf/1506.02640v5.pdf


class ImageDuoEncoderDetectorResnet(image_detector_base.ImageDetectorBase):
    """
    FeersumNLU Image Detector: Torchvision Resnet encoder & detector.
    """

    def __init__(self) -> None:
        super().__init__()

        # check if CUDA is available
        self._cuda_is_available = torch.cuda.is_available()

        self._next_label_idx = 0
        self._idx_to_label = {}  # type: Dict[int, str]
        self._model = None  # type: Optional[torchvision.models.detection.fasterrcnn_resnet50_fpn]
        # REMEMBER to add new attributes to __getstate__ and __setstate__ !!!

    def __getstate__(self):
        """ For pickling super & child states without 'model', but with 'model's box & mask predictors'. """
        super_state = super().__getstate__()

        if self._model is not None:
            model_box_predictor_state_dict = self._model.roi_heads.box_predictor.state_dict()
            model_mask_predictor_state_dict = self._model.roi_heads.mask_predictor.state_dict()
        else:
            model_box_predictor_state_dict = None
            model_mask_predictor_state_dict = None

        child_state = {
            '_next_label_idx': self._next_label_idx,
            '_idx_to_label': self._idx_to_label,
            'model_box_predictor_state_dict': model_box_predictor_state_dict,
            'model_mask_predictor_state_dict': model_mask_predictor_state_dict
        }

        return super_state, child_state

    def __setstate__(self, state):
        """ For unpickling super & child states without 'model', but with 'model's box & mask predictors'. """
        super_state, child_state = state
        super().__setstate__(super_state)

        # check if CUDA is available
        self._cuda_is_available = torch.cuda.is_available()

        self._next_label_idx = child_state['_next_label_idx']
        self._idx_to_label = child_state['_idx_to_label']

        if (child_state['model_box_predictor_state_dict'] is not None) and \
                (child_state['model_mask_predictor_state_dict'] is not None):
            # Load pretrained model.
            self._model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

            # Freeze the pre-trained layers of the network.
            # for param in self._model.parameters():
            #     param.requires_grad = False

            in_features = self._model.roi_heads.box_predictor.cls_score.in_features
            self._model.roi_heads.box_predictor = FastRCNNPredictor(in_features, len(self._labels))
            self._model.roi_heads.box_predictor.load_state_dict(child_state['model_box_predictor_state_dict'])

            in_features_mask = self._model.roi_heads.mask_predictor.conv5_mask.in_channels
            hidden_layer = 256
            self._model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                                     hidden_layer,
                                                                     len(self._labels))
            self._model.roi_heads.mask_predictor.load_state_dict(child_state['model_mask_predictor_state_dict'])

            self._model.eval()
        else:
            self._model = None

    def train_online(self,
                     # training_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
                     # testing_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
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
              # training_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
              # testing_list: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
              num_epochs: int) -> bool:
        """
        Reset and train the detector with ... Still to build the data loaders.

        :param num_epochs: The number of epochs to train the model for.
        :return: Boolean indicating whether or not the training was successful.
        """
        self._labels.clear()
        self._label_to_idx.clear()

        self._next_label_idx = 0
        self._idx_to_label.clear()
        self._model = None

        if True:  # len(training_list) > 0:
            # === Load pretrained model ===
            torch.set_num_threads(4)  # pylint: disable=no-member

            self._model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

            if self._model is not None:
                # === Init datasets ===
                data_transforms = {'train': transforms.Compose([transforms.ToTensor(),
                                                                transforms.RandomHorizontalFlip(0.5)]),
                                   'valid': transforms.Compose([transforms.ToTensor()])}

                data_root = '/content/feersum-nlu-sdk/PennFudanPed/'

                datasets: Dict[str, torch.utils.data.Dataset]

                datasets = {'train': pytorch_utils.PennFudanDataset(data_root, transform=data_transforms['train']),
                            'valid': pytorch_utils.PennFudanDataset(data_root, transform=data_transforms['valid'])}

                # Shuffle and subsample datasets into good non-overlapping train and valid sets.
                indices = torch.randperm(len(datasets['train'])).tolist()  # pylint: disable=no-member
                datasets['train'] = torch.utils.data.Subset(datasets['train'], indices[:-50])
                datasets['valid'] = torch.utils.data.Subset(datasets['valid'], indices[-50:])

                # Set labels and label_to_idx for the two class dataset.
                self._labels.add('background')
                self._label_to_idx['background'] = 0
                self._labels.add('person')
                self._label_to_idx['person'] = 1
                self._next_label_idx = 2

                # sample_lists = {'train': training_list,
                #                 'valid': testing_list if len(testing_list) > 0 else training_list}
                #
                # # === Update the _labels set, the _label_to_idx mapping AND the datasets ===
                # for sample_type in ['train', 'valid']:
                #     for sample in sample_lists[sample_type]:
                #         try:
                #             label = sample[1]
                #             self._labels.add(label)
                #             if self._label_to_idx.get(label) is None:
                #                 self._label_to_idx[label] = self._next_label_idx
                #                 self._next_label_idx += 1
                #
                #             # Decode the image - assumes the image is 256x256 RGB.
                #             pil_image = image_utils._base64_decode_to_pil_image(sample[0])
                #             if pil_image is not None:
                #                 datasets[sample_type].add_image(self._label_to_idx[label], pil_image)
                #
                #         except (UnicodeError, binascii.Error, IOError):
                #             continue  # Ignore the sample.

                self._idx_to_label = {v: k for k, v in self._label_to_idx.items()}

                # === Create the data loaders ===
                # batch_size = 32

                # sample_weights = pytorch_utils.make_weights_for_balancing_classes(datasets['train'].data_samples,
                #                                                                   len(datasets['train'].label_idxs))
                # balancing_sampler = torch.utils.data.WeightedRandomSampler(sample_weights,
                #                                                            len(sample_weights))

                dataloaders = {  # 'train': DataLoader(datasets['train'], batch_size=batch_size, sampler=balancing_sampler),
                    'train': DataLoader(datasets['train'], batch_size=2, shuffle=True, collate_fn=utils.collate_fn),
                    'valid': DataLoader(datasets['valid'], batch_size=1, shuffle=False, collate_fn=utils.collate_fn)}

                # === Setup the model, loss function and the optimizer ===
                in_features = self._model.roi_heads.box_predictor.cls_score.in_features
                self._model.roi_heads.box_predictor = FastRCNNPredictor(in_features, len(self._labels))

                in_features_mask = self._model.roi_heads.mask_predictor.conv5_mask.in_channels
                hidden_layer = 256
                self._model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                                         hidden_layer,
                                                                         len(self._labels))

                # Specify loss function (categorical cross-entropy).
                # criterion = nn.NLLLoss()

                # Freeze the pre-trained layers of the pre-trained network.
                # for param in self._model.parameters():
                #     param.requires_grad = False

                # Specify optimizer.
                params = [param for param in self._model.parameters() if param.requires_grad]
                optimizer = torch.optim.SGD(params, lr=0.005,
                                            momentum=0.9, weight_decay=0.0005)
                # optimizer = optim.SGD(self._model.parameters(), lr=0.001, momentum=0.9, weight_decay=0.001)
                # optimizer = optim.Adam(self._model.parameters(), lr=0.001, weight_decay=0.0001)

                lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                               step_size=3,
                                                               gamma=0.1)

                # === Train loop ===
                # valid_loss_min = np.Inf
                # valid_acc_max = 0.0

                # if self._cuda_is_available:
                #     self._model.cuda()

                device = torch.device('cuda') if torch.cuda.is_available() \
                    else torch.device('cpu')  # pylint: disable=no-member
                self._model.to(device)

                for epoch in range(num_epochs):
                    # train for one epoch, printing every 10 iterations
                    engine.train_one_epoch(self._model, optimizer, dataloaders['train'], device, epoch, print_freq=10)
                    # update the learning rate
                    lr_scheduler.step(epoch=None)
                    # evaluate on the test dataset
                    engine.evaluate(self._model, dataloaders['valid'], device=device)

                    # valid_loss = valid_loss_sum / len(dataloaders['valid'].dataset)
                    # print('   Validation loss = {:.6f}'.format(valid_loss), flush=True, end='')
                    #
                    # valid_acc = valid_correct_count / len(dataloaders['valid'].dataset)
                    # print(' [acc = {:.2f}]'.format(valid_acc), flush=True)
                    #
                    # if (valid_loss < valid_loss_min) or (
                    #         (valid_loss == valid_loss_min) and (valid_acc >= valid_acc_max)):
                    #     print('     Validation loss decreased ({:.6f} --> {:.6f}). Saving model.'.format(valid_loss_min,
                    #                                                                                      valid_loss))
                    #     torch.save(self._model.state_dict(), 'state_dict_best_valid_loss.pt')
                    #     valid_loss_min = valid_loss
                    #     valid_acc_max = valid_acc

                # === Load the model that performed the best during training ===
                # print("Loading the best performing model...", flush=True, end='')
                # self._model.load_state_dict(torch.load('state_dict_best_valid_loss.pt'))
                # print("done.")

                self._model.eval()

            return True
        else:
            return False

    def process_image(self, image: Image):
        # w, h = image.size

        # # crop to 224 x 224
        # image = image.crop((w // 2 - 112,
        #                     h // 2 - 112,
        #                     w // 2 + 112,
        #                     h // 2 + 112))

        # Make the image float 32.
        np_image = np.array(image, np.float32)
        np_image /= 255.0

        # Transpose channels as required by the model.
        return np_image.transpose((2, 0, 1))

    def detect(self, input_image: str,
               weak_match_threshold: float,
               top_n: int) -> List[Tuple[str, float]]:
        """ Find the n best detections. Only return the labels for now. Still need to define the bounding boxes.

        :param input_image: The image to classify. Image formatted as utf8 encoded base64 string.
        :param weak_match_threshold: The threshold above which matches are weak; 0.7 culls much; 1.1 culls less, etc.
        :param top_n: The max number (i.e. k) of sorted matches to return.
        :return: Sorted list of scored labels [(str, float)].
        """
        if self._model is not None:
            try:
                pil_image = image_utils._base64_decode_to_pil_image(input_image)

                if pil_image is None:
                    logging.error("image_duo_encoder_detector_resnet.detect - pil_image is None.")
                    return []

                w, h = pil_image.size

                np_image = self.process_image(pil_image)

                torch_image = torch.as_tensor(np_image)  # pylint: disable=no-member
                # print(torch_image)

                # data_root = '/content/feersum-nlu-sdk/PennFudanPed/'
                # dataset = pytorch_utils.PennFudanDataset(data_root, transform=transforms.Compose([transforms.ToTensor()]))
                # torch_image, _ = dataset[0]
                # print(torch_image)

                # Set the model to eval/run mode.
                self._model.eval()

                device = torch.device('cuda') if torch.cuda.is_available() \
                    else torch.device('cpu')  # pylint: disable=no-member
                self._model.to(device)
                torch_image = torch_image.to(device)

                # if self._cuda_is_available:
                #     torch_image = torch_image.cuda()
                #     self._model.cuda()

                with torch.no_grad():
                    output_list = self._model([torch_image])

                print(output_list)

                output_idxs = output_list[0]['labels']
                output_idxs = output_idxs.cpu().numpy()
                class_labels = [self._idx_to_label[idx] for idx in output_idxs]

                probs = output_list[0]['scores']
                probs = probs.cpu().numpy()

                return list(zip(class_labels, probs))
            except (UnicodeError, binascii.Error, IOError):
                return []
        else:
            return []
