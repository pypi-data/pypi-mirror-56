import anyio
import asyncclick as click


@click.group(invoke_without_command=True)
@click.pass_context
async def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)


@cli.command()
@click.option("--dir", default=None, help="Directory where the project is created")
@click.option("--customer", "-c", help="Customer name", required=True)
@click.option("--src_lang", help="Source language", required=True)
@click.option("--tgt_lang", help="Target language", required=True)
@click.option("--flavor", default=None, help="Flavor")
@click.option("--version", default=1, type=int, help="Version")
async def new(dir, customer, src_lang, tgt_lang, flavor, version):
    '''
    Create a new project
    '''
    print(dir, customer, src_lang, tgt_lang, flavor, version)
    click.echo('The subcommand')

@cli.command()
@click.option("--dir", default=None, help="Directory where the project is created")
async def clean(dir):
    '''
    Workflow initialization. Use this command when the project is ready
    '''
    print(dir)
    click.echo('The subcommand')


def main():
    cli(_anyio_backend="asyncio")  # or asyncio, or curio
