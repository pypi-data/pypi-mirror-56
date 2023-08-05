import asyncio
import argparse
import os
from pangeamt_tea.project.project import Project

def main():
    asyncio.run(bootstrap())

async def bootstrap():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(description='Tea', dest="cmd")

    parser_init = subparser.add_parser("init")
    parser_init.add_argument('-parent_dir', type=str, default=None)
    parser_init.add_argument('-customer', type=str, default=None)
    parser_init.add_argument('-src_lang', type=str, default=None)
    parser_init.add_argument('-tgt_lang', type=str, default=None)
    parser_init.add_argument('-flavor', type=str, default=None)
    parser_init.add_argument('-version', type=str, default=None)

    parser_clean = subparser.add_parser("clean")
    args = parser.parse_args()

    # Get command
    cmd = args.cmd

    # Params
    params = vars(args)
    del(params['cmd'])

    # Run
    if cmd == 'init':
        await cmd_init(**params)

async def cmd_init(parent_dir=None, customer=None, src_lang=None, tgt_lang=None, flavor=None, version=None,):

    if parent_dir is None:
        parent_dir = os.getcwd()

    if customer is None:
        customer = input("Customer: ")

    if src_lang is None:
        src_lang = input("Source language: ")



    Project.create(parent_dir, customer, src_lang, tgt_lang, flavor, version)
    # customer = input("Customer: ")
    # src_lang = input("Source language: ")
    # tgt_lang = input("Target language: ")
    # flavor = input("Flavor: ")
    #
    # project_dir = customer + '_' + src_lang + '_' + tgt_lang
    # if flavor:
    #     project_dir += '_' + flavor
    # if os.path.isdir(project_dir):
    #     raise ValueError(f'Project {project_dir} already exist\'s')
    #
    # os.mkdir(project_dir)
    # print(f"run `cd {project_dir}`")


if __name__ == '__main__':
    main()