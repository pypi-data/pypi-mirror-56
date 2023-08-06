# coding=utf-8

""" Command line processing for labelbox_export_json. """

import argparse
from labelboxutils import __version__
from labelboxutils.ui.labelbox_export_json_app import run_labelbox_json_export


def main(args=None):
    """ Entry point for labelbox_export_json application. """
    parser = argparse.ArgumentParser(description='LabelBox JSON Export')
    parser.add_argument("-j", "--json",
                        required=True,
                        type=str,
                        help="JSON file exported from Labelbox.")

    parser.add_argument("-o", "--output",
                        required=True,
                        type=str,
                        help="Output directory.")

    parser.add_argument("-f", "--format",
                        required=False,
                        type=str,
                        default='rgba',
                        help="Format, one of [grey|rgb] as default is rgba")

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='labelbox_export_json version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_labelbox_json_export(args.json,
                             args.output,
                             args.format)
