import argparse
import os

from quicks import VERSION, process_project, parse_template


def main():
    arg_parser = argparse.ArgumentParser('Quicks', description='Project generator {}'.format(VERSION))
    arg_parser.add_argument('project', type=str)
    arg_parser.add_argument('template', type=str)
    arg_parser.add_argument('--path', '-p', type=str)
    args = arg_parser.parse_args()
    process_project(args.path or os.getcwd(), args.project, parse_template(args.template))


if __name__ == '__main__':
    main()
