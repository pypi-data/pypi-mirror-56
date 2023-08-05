from typing import List, Tuple, Any, Set  # noqa # pylint: disable=unused-import
import os

from feersum_nlu.models.image_encoder_base import ImageEncoderBase

import numpy as np
from PIL import Image

import torch
from torch import nn
from torch.nn import functional
import torch.utils.data
from torch.utils.data import Dataset


def process_image(image: Image):
    w, h = image.size

    # crop to 224 x 224
    image = image.crop((w // 2 - 112,
                        h // 2 - 112,
                        w // 2 + 112,
                        h // 2 + 112))

    # Make the image float 32.
    np_image = np.array(image, np.float32)

    # Normalise image pixel values.
    norm_mean = [0.485, 0.456, 0.406]  # ImageNet norm.
    norm_std = [0.229, 0.224, 0.225]  # ImageNet std.

    np_image /= 255.0
    np_image -= norm_mean
    np_image /= norm_std

    # Transpose channels as required by the model.
    return np_image.transpose((2, 0, 1))


# === Custom classification dataset handlers ===
def make_weights_for_balancing_classes(sample_list: List[Tuple[int, Any]],  # List[Tuple[label_idx, Any]]
                                       num_classes: int) -> List[float]:
    count_per_class = [0.0] * num_classes

    # Counts per class
    for sample in sample_list:
        label_idx, _ = sample
        count_per_class[label_idx] += 1.0

    weight_per_class = [0.0] * num_classes
    num_samples = len(sample_list)

    # super-sample the smaller classes.
    for label_idx in range(num_classes):
        weight_per_class[label_idx] = num_samples / count_per_class[label_idx]

    weight_per_sample = [0.0] * num_samples

    # Calculate a weight per sample.
    for sample_idx, sample in enumerate(sample_list):
        label_idx, _ = sample
        weight_per_sample[sample_idx] = weight_per_class[label_idx]

    return weight_per_sample  # Need not sum to 1.0


class VisionClassDataset(Dataset):
    """
    Custom image dataset. Returns (image, label_idx) samples.
    """

    def __init__(self, transform=None):
        self.transform = transform
        self.data_samples = []  # type: List[Tuple[int, np.array]]
        self.label_idxs = set()  # type: Set[int]

    def add_image(self, label_idx: int, image: Image):
        self.data_samples.append((label_idx, image))
        self.label_idxs.add(label_idx)

    def __len__(self):
        return len(self.data_samples)

    def __getitem__(self, idx):
        data_sample = self.data_samples[idx]
        label_idx = data_sample[0]
        image = data_sample[1]

        if self.transform:
            image = self.transform(image)

        return label_idx, image


# === Custom regression dataset handlers ===
class VisionRegressDataset(Dataset):
    """
    Custom image dataset. Returns (image, target_value) samples.
    """

    def __init__(self, transform=None):
        self.transform = transform
        self.data_samples = []  # type: List[Tuple[float, np.array]]

    def add_image(self, target_value: float, image: Image):
        self.data_samples.append((target_value, image))

    def __len__(self):
        return len(self.data_samples)

    def __getitem__(self, idx):
        data_sample = self.data_samples[idx]
        target_value = data_sample[0]
        image = data_sample[1]

        if self.transform:
            image = self.transform(image)

        return np.float32(target_value), image


# === Custom network heads ===
class IdentityHead(nn.Module):
    """
    Identity layer - Needed to get encoder layer to expected output layer.
    """

    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x


class ClassifierHead(nn.Module):
    """
    Fully connected reshaping head of classification model.
    """

    def __init__(self, in_features, out_features):
        super().__init__()
        self.fc1 = nn.Linear(in_features, out_features)

    def forward(self, x):
        x = self.fc1(x)
        x = functional.log_softmax(x, dim=1)
        return x


class RegressorHead(nn.Module):
    """
    Fully connected regression head.
    """

    def __init__(self, input_dim, output_dim):
        super().__init__()
        # hidden_dim = (input_dim + output_dim) // 2
        # self.fc1 = nn.Linear(input_dim, hidden_dim)
        # self.fc2 = nn.Linear(hidden_dim, output_dim)
        # self.drop = nn.Dropout(0.5)
        self.fc = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        # x = self.fc1(x)
        # x = self.drop(x)
        # x = self.fc2(x)
        x = self.fc(x)
        return x


# Custom image transform to encode image using an ImageEncoderBase
class EncodeTransform(object):
    def __init__(self, vision_model: ImageEncoderBase):
        self._vision_model = vision_model

    def __call__(self, img):
        np_vector = self._vision_model.calc_pil_image_vector(img)
        torch_vector = torch.as_tensor(np_vector)  # pylint: disable=no-member
        return torch_vector

    def __repr__(self):
        return self.__class__.__name__ + '_' + self._vision_model.__class__.__name__


# ============================
# https://www.dlology.com/blog/how-to-create-custom-coco-data-set-for-instance-segmentation/
class PennFudanDataset(torch.utils.data.Dataset):
    def __init__(self, root, transform=None):
        self.root = root
        self.transform = transform

        # Load all image files, sorting them to ensure that they are aligned.
        self.imgs = list(sorted(os.listdir(os.path.join(root, "PNGImages"))))
        self.masks = list(sorted(os.listdir(os.path.join(root, "PedMasks"))))

    def __getitem__(self, idx):
        # Load images and masks.
        img_path = os.path.join(self.root, "PNGImages", self.imgs[idx])
        mask_path = os.path.join(self.root, "PedMasks", self.masks[idx])
        img = Image.open(img_path).convert("RGB")

        # Each mask colour corresponds to a different class instance with 0 being background!
        mask = Image.open(mask_path)
        mask = np.array(mask)
        obj_ids = np.unique(mask)

        # Remove the background/first id is the background, so remove it
        obj_ids = obj_ids[1:]

        # Split the color-encoded mask into a set of binary masks.
        masks = mask == obj_ids[:, None, None]

        # Get bounding box coordinates for each mask.
        num_objs = len(obj_ids)
        boxes = []  # type: List[List[Any]]
        for i in range(num_objs):
            pos = np.where(masks[i])
            xmin = np.min(pos[1])
            xmax = np.max(pos[1])
            ymin = np.min(pos[0])
            ymax = np.max(pos[0])
            boxes.append([xmin, ymin, xmax, ymax])

        boxes_tensor = torch.as_tensor(boxes, dtype=torch.float32)  # pylint: disable=no-member

        # there is only one class in this case!!!
        labels = torch.ones((num_objs,), dtype=torch.int64)  # pylint: disable=no-member
        masks = torch.as_tensor(masks, dtype=torch.uint8)  # pylint: disable=no-member

        image_id = torch.tensor([idx])  # pylint: disable=no-member, not-callable
        area = (boxes_tensor[:, 3] - boxes_tensor[:, 1]) * (boxes_tensor[:, 2] - boxes_tensor[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)  # pylint: disable=no-member

        target = {}
        target["boxes"] = boxes_tensor
        target["labels"] = labels
        target["masks"] = masks
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transform is not None:
            img, target = self.transform(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)
