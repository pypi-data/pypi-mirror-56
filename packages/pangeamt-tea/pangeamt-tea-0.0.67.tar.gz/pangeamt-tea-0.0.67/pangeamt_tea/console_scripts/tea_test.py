import os
import asyncclick as click
import multiprocessing
import os
import asyncio

from pangeamt_tea.project.workflow.stage.clean_stage import clean as clean2

@click.group(invoke_without_command=True)
async def tea_test():
    pass

# New Project
@tea_test.command()
async def clean():
    os.environ['PYTHONASYNCIODEBUG'] = "1"
    total = 100
    data_generator = ((i, f'Hello {i}', f'Hola {i}') for i in range(total))
    max_workers = 2

    multiprocessing_manager = multiprocessing.Manager()
    await clean2(
        multiprocessing_manager,
        data_generator,
        max_workers,
        total)

    click.echo("xxxxxxxxx")

def main():
    tea_test(_anyio_backend="asyncio")  # or asyncio, or curio