import os

import asyncclick as click

from pangeamt_tea.project.config import Config
from pangeamt_tea.project.project import Project, ProjectAlreadyExistsException, ProjectNotFoundException
from pangeamt_tea.project.workflow.workflow import WorkflowAlreadyExists

global prompting
prompting = False


def callback_test(ctx, param, value):
    global prompting
    prompting = value


@click.group(invoke_without_command=True)
@click.option("--interactive", "-i", default=False, type=click.BOOL, help="Interactive mode", callback=callback_test)
@click.pass_context
async def tea(ctx, interactive):
    pass


# New Project
@tea.command()
@click.option("--customer", "-c", help="Customer name")
@click.option("--src_lang", "-s", help="Source language")
@click.option("--tgt_lang", "-t", help="Target language")
@click.option("--flavor", "-f", default=None, help="Flavor")
@click.option("--version", "-v", default=1, type=click.INT, help="Version")
@click.option("--dir", "-d", "parent_dir", default=None, help="Directory where the project is created")
async def new(parent_dir, customer, src_lang, tgt_lang, flavor, version):
    parent_dir = parent_dir if parent_dir is not None else os.getcwd()
    parent_dir = os.path.abspath(parent_dir)
    if prompting:
        if customer is None:
            while customer is None or customer == "":
                customer = input("Customer is required. Please enter customer: ")
            if customer == '':
                customer = None
        if src_lang is None:
            while src_lang is None or src_lang == "":
                src_lang = input("Source lang is required. Please enter source lang: ")
            if src_lang == '':
                src_lang = None
        if tgt_lang is None:
            while tgt_lang is None or tgt_lang == "":
                tgt_lang = input("Target lang is required. Please enter target lang: ")
            if tgt_lang == '':
                tgt_lang = None
        if flavor is None:
            flavor = input("Please enter flavor: ")
            if flavor == '':
                flavor = None
        if 1 == version:
            version = input("Please enter version:")
            version = int(version) if version != "" else 1
    else:
        if customer is None:
            raise RequireOptionExpcetion("-c", "customer")

        if src_lang is None:
            raise RequireOptionExpcetion("-s", "source lang")

        if tgt_lang is None:
            raise RequireOptionExpcetion("-t", "target lang")
    try:
        Project.new(customer, src_lang, tgt_lang, parent_dir, version=version, flavor=flavor)
    except (ProjectAlreadyExistsException, ProjectNotFoundException) as e:
        click.echo(f'Error: {e}')


# Add tokenizer
@tea.command()
@click.option("--src", "-s", help="Source tokenizer", type=click.Choice(['moses', 'mecab'], case_sensitive=False))
@click.option("--tgt", "-t", help="Target tokenizer", type=click.Choice(['moses', 'mecab'], case_sensitive=False))
@click.option('--project', '-p', 'project_dir')
@click.pass_context
def tokenizer(ctx, src, tgt, project_dir):
    ctx.ensure_object(dict)
    if project_dir is None:
        project_dir = os.getcwd()

    try:
        Config.add_tokenizer(src, tgt, project_dir)
    except ProjectNotFoundException as e:
        click.echo(f'Error: {e}')


# Add tokenizer
@tea.command()
@click.option("--src", "-s", help="Source truecaser", type=click.Choice(['enabled', 'disabled'], case_sensitive=False))
@click.option("--tgt", "-t", help="Target truecaser", type=click.Choice(['enabled', 'disabled'], case_sensitive=False))
@click.option('--project', '-p', 'project_dir')
@click.pass_context
def truecaser(ctx, src, tgt, project_dir):
    ctx.ensure_object(dict)
    if project_dir is None:
        project_dir = os.getcwd()

    try:
        Config.add_truecaser(src, tgt, project_dir)
    except ProjectNotFoundException as e:
        click.echo(f'Error: {e}')


# Workflow group
@tea.group(invoke_without_command=True)
@click.option('--project', '-p', 'project_dir')
@click.pass_context
async def workflow(ctx, project_dir):
    ctx.ensure_object(dict)
    if project_dir is None:
        project_dir = os.getcwd()
    project_dir = os.path.abspath(project_dir)
    ctx.obj['project'] = Project.load(project_dir)


# Init
@workflow.command()
@click.option('--force', '-f', default=False)
@click.pass_context
async def new(ctx, force):
    '''
    Init the workflow.
    '''
    project = ctx.obj['project']
    try:
        await project.new_workflow(force)
    except WorkflowAlreadyExists as e:
        click.echo(f'Error: {e}')
    click.echo(ctx.obj['project'])
    click.echo('---> Done')


# Clean
@workflow.command()
@click.option("--project", "-p", "project_dir", help="The project directory. Default: the current working directory")
@click.pass_context
async def clean(ctx, project_dir):
    '''
    Clean the data.
    '''
    click.echo(ctx.obj['project'])
    click.echo('---> Done')


def main():
    tea(_anyio_backend="asyncio")  # or asyncio, or curio


class RequireOptionExpcetion(Exception):
    def __init__(self, command: str, variable: str):
        super().__init__(f'Error: {command} {variable} is required')


if __name__ == "__main__":
    main()
