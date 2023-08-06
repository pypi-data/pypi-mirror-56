# -*- coding: utf-8 -*-
#
# Copyright © 2019 Stephan Seitz <stephan.seitz@fau.de>
#
# Distributed under terms of the GPLv3 license.

"""

"""

import glob
import warnings
from os.path import join, splitext

import natsort
import numpy as np
import pydicom
from tqdm import tqdm


def natglob(pattern, recursive=True) -> list:
    """natglob

    :param pattern:
    :param recursive:
    :rtype: list
    """
    return natsort.natsorted(glob.glob(pattern, recursive=recursive))


def dicomdir2vol(dicom_dir, filter_type=None, series_filter=None, frame_of_reference_filter=None, report_progress=True):
    """Reads a DICOM directory to a volume

    Args:
        dicom_dir (str): Path to directory
        filter_type (str, optional): Only DICOMs with this sub string in ImageType are regarded
        series_filter (int, optional): Find a specific index in DICOM stack
        frame_of_reference_filter (str, optional): Enter a specific DICOM file that should be regarded
                                                   as reference filter
        report_progress (bool, optional): Show a progress bar while reading the files
    """

    dicom_dir_files = natglob(join(dicom_dir, "*"))
    dicom_dir_files = list(filter((lambda x: splitext(x.lower())[1] in ['.dcm', '.ima']), dicom_dir_files))
    if not dicom_dir_files:
        return None, None, None, None

    spacing = None
    origin = None
    orientation = None

    last_image_idx = -1
    arrays = []

    for file in tqdm(dicom_dir_files) if report_progress else dicom_dir_files:
        try:
            dc = pydicom.read_file(file)

            if filter_type and not str.lower(filter_type) in str.lower(str(dc.ImageType)):
                continue
            if series_filter and dc.SeriesNumber != series_filter:
                continue
            if frame_of_reference_filter and frame_of_reference_filter not in dc[0x20, 0x52].value:
                continue
            if not dc[0x20, 0x13]:
                continue
            cur_image_idx = dc[0x20, 0x13].value
            if cur_image_idx <= last_image_idx:
                continue

            # print("Loading dicom slice %i" % cur_image_idx)
            arrays.append(dc.pixel_array)
            last_image_idx = cur_image_idx

            if not spacing:
                spacing = [float(dc.SliceThickness), float(dc.PixelSpacing[1]), float(dc.PixelSpacing[0])]
            if not origin:
                try:
                    origin = [float(dc.ImagePositionPatient[2]),
                              float(dc.ImagePositionPatient[1]),
                              float(dc.ImagePositionPatient[0])]
                except Exception:
                    pass
            if not orientation:
                try:
                    orientation = [float(dc.PatientOrientationPatient[2]),
                                   float(dc.PatientOrientationPatient[1]),
                                   float(dc.PatientOrientationPatient[0])]
                    if orientation and not np.allclose(orientation, np.zeros(3)):
                        warnings.warn("Patient orientation is not 0,0,0!!!")
                except Exception:
                    pass

        except Exception as e:
            print(e)

    if arrays:
        vol = np.stack(arrays)
        return vol, spacing, origin, orientation
    else:
        warnings.warn('Could not match any DICOMs with the filtered type')
        return None, None, None, None
