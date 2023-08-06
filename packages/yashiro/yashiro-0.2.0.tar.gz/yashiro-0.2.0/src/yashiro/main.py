import argparse
import json

import jinja2

from . import __version__


class Parser:
    def __init__(self, template_path, json_path):
        with open(template_path) as file:
            self.template = jinja2.Template(file.read())
        with open(json_path) as file:
            self.json = json.load(file)

    def __call__(self):
        return self.template.render(self.json)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="yashiro",
        description="A utility to manage testing and migrating a database",
    )
    parser.add_argument("-j", "--json", help="The path to the json file")
    parser.add_argument("-t", "--template", help="The path to the template")
    parser.add_argument(
        "-V", "--version", action="store_true", help="Print the version and exit"
    )

    return parser.parse_args()


def get_output():
    args = parse_args()
    if args.version is True:
        return f"Yashiro {__version__}"
    parser = Parser(args.template, args.json)
    return parser()


def write_output():
    print(get_output())
