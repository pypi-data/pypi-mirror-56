import os
import asyncclick as click
import multiprocessing
import os
import asyncio

from pangeamt_tea.project.workflow.stage.clean_stage import MultiprocessingCleaner

@click.group(invoke_without_command=True)
async def tea_test():
    pass

# New Project
@tea_test.command()
async def clean():
    os.environ['PYTHONASYNCIODEBUG'] = "1"
    data_generator_len = 100
    data_generator = ((i, f'Hello {i}', f'Hola {i}') for i in range(data_generator_len))
    max_workers = 2

    multiprocessing_manager = multiprocessing.Manager()

    multiprocessing_cleaner = MultiprocessingCleaner.new(
        data_generator,
        data_generator_len,
        max_workers,
        multiprocessing_manager)

    async for dones in multiprocessing_cleaner.clean():
        click.echo(dones)



def main():
    tea_test(_anyio_backend="asyncio")  # or asyncio, or curio