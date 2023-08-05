"""
FeersumNLU Image Reader: Base class.
"""

from abc import ABC
# from abc import abstractmethod

from typing import Dict, Tuple, List, Optional, Set  # noqa # pylint: disable=unused-import
# import uuid
import os
import logging

from feersum_nlu import image_utils
from feersum_nlu import nlp_engine_data

import cv2
import numpy as np


def load_templates(data_path: str):
    directory = os.fsencode(data_path)

    template_list = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.lower().endswith((".jpg", ".jpeg", ".j2k", ".j2p", ".jpx", ".png", ".bmp")):
            image = cv2.imread(data_path + "/" + filename)  # pylint: disable=no-member
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # pylint: disable=no-member

            height, width = image.shape[:2]
            resized_height = 32
            resized_width = 32  # int((resized_height / height) * width)

            image = cv2.resize(image, (resized_width, resized_height),  # pylint: disable=no-member
                               interpolation=cv2.INTER_LINEAR)  # pylint: disable=no-member

            label = filename[:filename.find('_')]

            template_list.append((image, label))

    return template_list


def segment_lines(image, y0: int, y1: int) -> List[Tuple[int, int]]:
    im_heigh, im_width = image.shape[:2]
    filt_window_size = 40

    line_sum_list = []  #

    for y in range(y0, y1):
        line_sum = 0.0

        for x in range(-im_width//3, im_width//3):
            line_sum += image[y, x + im_width//2]

        line_sum_list.append(line_sum)

    line_list = []  # type: List[Tuple[int, int]]
    above_threshold = True
    line_start = 0

    for h in range(y0+filt_window_size, y1-filt_window_size):
        window_max = max(line_sum_list[h - filt_window_size: h + filt_window_size])

        if above_threshold and (line_sum_list[h] < window_max*0.95):
            line_start = h
            above_threshold = False
        elif (not above_threshold) and (line_sum_list[h] > window_max*0.95):
            line_list.append((line_start, h))
            above_threshold = True

    return line_list


def segment_chars(image, y0: int, y1: int) -> List[Tuple[int, int]]:
    im_heigh, im_width = image.shape[:2]
    filt_window_size = 20

    col_sum_list = []

    for x in range(0, im_width):
        col_sum = 0.0

        for y in range(y0, y1):
            col_sum += image[y, x]

        col_sum_list.append(col_sum)

    char_list = []  # type: List[Tuple[int, int]]
    above_threshold = True
    char_start = 0

    for w in range(0+filt_window_size, im_width-filt_window_size):
        window_max = max(col_sum_list[w - filt_window_size: w + filt_window_size])

        if above_threshold and (col_sum_list[w] < window_max*0.95):
            char_start = w
            above_threshold = False
        elif (not above_threshold) and (col_sum_list[w] > window_max*0.95):
            char_list.append((char_start, w))
            above_threshold = True

    return char_list


character_template_list = load_templates(nlp_engine_data.get_path() + "/vision/char_templates")


class ImageReaderBase(ABC):
    """
    FeersumNLU Image Reader: Base class.
    """

    def __init__(self) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.
        # REMEMBER to add new attributes to __getstate__ and __setstate__ !!!

    def __getstate__(self):
        state = {
            'uuid': self.uuid,
        }
        return state

    def __setstate__(self, state):
        self.uuid = state['uuid']

    @staticmethod
    def read_text(input_image: str) -> List[Dict]:
        """ Read the text in the input image.

        :param input_image: The expression to look for in the expression set. Image formatted as utf8 encoded base64 string.
        :return: The list of extracted text [{"text": "...", "lang_code": "..."}].
        """
        text_list = []  # type: List[Dict]

        pil_image = image_utils._base64_decode_to_pil_image(input_image)

        if pil_image is None:
            logging.error("image_duo_encoder_classifier_resnet.read_text - pil_image is None.")
            return []

        pil_image.save(fp="image_reader_base_input.jpg")

        opencv_image = np.array(pil_image)
        opencv_image = opencv_image[:, :, ::-1].copy()  # Convert RGB to BGR

        # Denoise the image a bit.
        # opencv_image = cv2.GaussianBlur(opencv_image, (3, 3), 0)  # pylint: disable=no-member

        height, width = opencv_image.shape[:2]

        print(f"{width} x {height}")

        target_size = 800

        if width > height:
            resized_height = target_size
            resized_width = int((target_size / height) * width)
        else:
            resized_height = int((target_size / width) * height)
            resized_width = target_size

        print(f"{resized_width} x {resized_height}")

        resized_image = \
            cv2.resize(opencv_image, (resized_width, resized_height),  # pylint: disable=no-member
                       interpolation=cv2.INTER_LINEAR)  # pylint: disable=no-member

        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)  # pylint: disable=no-member
        thresholded_image = cv2.adaptiveThreshold(gray_image, 255,  # pylint: disable=no-member
                                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # pylint: disable=no-member
                                                  cv2.THRESH_BINARY,  # pylint: disable=no-member
                                                  ((target_size//20)//2)*2+1, 20)  # pylint: disable=no-member

        cv2.imwrite("image_reader_base_thresholded.jpg", thresholded_image)  # pylint: disable=no-member

        line_list = segment_lines(thresholded_image, 0, resized_height)

        segmented_image = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR)  # pylint: disable=no-member

        # run_id = uuid.uuid4()
        # char_num = 0

        for line_start, line_end in line_list:
            cv2.line(segmented_image,  # pylint: disable=no-member
                     (0, line_start),  # pylint: disable=no-member
                     (resized_width, line_start), (255, 0, 0), 1)  # pylint: disable=no-member
            cv2.line(segmented_image,  # pylint: disable=no-member
                     (0, line_end),  # pylint: disable=no-member
                     (resized_width, line_end), (255, 0, 0), 1)  # pylint: disable=no-member

            text = ""
            char_list = segment_chars(thresholded_image, line_start, line_end)

            for char_start, char_end in char_list:
                cv2.line(segmented_image,  # pylint: disable=no-member
                         (char_start, line_start),  # pylint: disable=no-member
                         (char_start, line_end), (255, 0, 0), 1)  # pylint: disable=no-member
                cv2.line(segmented_image,  # pylint: disable=no-member
                         (char_end, line_start),  # pylint: disable=no-member
                         (char_end, line_end), (255, 0, 0), 1)  # pylint: disable=no-member

                char_image = thresholded_image[(line_start-1):(line_end+1), (char_start-1):(char_end+1)]

                # Save the char image.
                # cv2.imwrite(f"images/{run_id}_{char_num}.jpg", char_image)

                char_height, char_width = char_image.shape[:2]
                resized_char_height = 32
                resized_char_width = 32  # int((resized_char_height / char_height) * char_width)

                char_image = cv2.resize(char_image, (resized_char_width, resized_char_height),  # pylint: disable=no-member
                                        interpolation=cv2.INTER_LINEAR)  # pylint: disable=no-member

                # char_num += 1

                min_template_error = np.inf
                min_template_idx = 0

                # Find the closest template
                for template_idx, template in enumerate(character_template_list):

                    template_error = \
                        (np.abs(np.array(char_image, np.float32) - np.array(template[0], np.float32))).mean(axis=None)

                    if template_error < min_template_error:
                        min_template_idx = template_idx
                        min_template_error = template_error

                if min_template_error < 20.0:
                    char_value = character_template_list[min_template_idx][1]
                    text = text + str(char_value)

            if text != "":
                text_list.append({"text": text})

        cv2.imwrite("image_reader_base_segmented.jpg", segmented_image)  # pylint: disable=no-member

        return text_list
