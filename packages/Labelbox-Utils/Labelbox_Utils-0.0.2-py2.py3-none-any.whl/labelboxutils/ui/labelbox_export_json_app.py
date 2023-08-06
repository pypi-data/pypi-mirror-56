# coding=utf-8

""" Processing for labelbox_export_json appliction. """

import os
import json
import urllib.request
import six
import cv2


def run_labelbox_json_export(json_file, output_dir, output_format):
    """
    Parses the Labelbox json file, and exports data.

    :param json_file: file name of json file
    :param output_dir: where to write to
    :param output_format: output image format, [grey|rgb|rgba (default)]
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(json_file) as file:
        data = file.read()
        decoded_data = json.loads(data)
        for sample in decoded_data:
            dataset_name = sample['Dataset Name']
            external_id = sample['External ID']
            basename = os.path.basename(external_id)
            filename_no_extension = os.path.splitext(basename)[0]
            objects = sample['Label']['objects']

            dir_name = os.path.join(output_dir, dataset_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            for obj in objects:
                instance_uri = obj['instanceURI']
                value = obj['value']
                file_name = os.path.join(dir_name,
                                         filename_no_extension
                                         + '_' + value + '.bmp')
                six.print_("writing to:" + file_name)

                urllib.request.urlretrieve(instance_uri, file_name)

                if output_format == 'grey':
                    image = cv2.imread(file_name)
                    grey = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
                    file_name = os.path.join(dir_name,
                                             filename_no_extension
                                             + '_' + value + '.png')
                    cv2.imwrite(file_name, grey)
                    six.print_("writing to:" + file_name)

                elif output_format == 'rgb':
                    image = cv2.imread(file_name)
                    rgb = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
                    file_name = os.path.join(dir_name,
                                             filename_no_extension
                                             + '_' + value + '.png')
                    cv2.imwrite(file_name, rgb)
                    six.print_("writing to:" + file_name)
