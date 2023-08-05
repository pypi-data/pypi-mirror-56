import os
import asyncclick as click
import multiprocessing
import os
import asyncio


from pangeamt_tea.project.workflow.stage.clean_stage import clean

@click.group(invoke_without_command=True)
@click.pass_context
async def tea_test(ctx, interactive):
    pass

# New Project
@tea_test.command()
@click.option("--customer", "-c", help="Customer name")
@click.option("--src_lang", "-s", help="Source language")
@click.option("--tgt_lang", "-t", help="Target language")
@click.option("--flavor", "-f", default=None, help="Flavor")
@click.option("--version", "-v", default=1, type=click.INT, help="Version")
@click.option("--dir", "-d", "parent_dir", default=None, help="Directory where the project is created")
async def clean():

        os.environ['PYTHONASYNCIODEBUG'] = "1"
        total = 100
        data_generator = ((i, f'Hello {i}', f'Hola {i}') for i in range(total))
        max_workers = 2

        multiprocessing_manager = multiprocessing.Manager()
        asyncio.run(clean(
            multiprocessing_manager,
            data_generator,
            max_workers,
            total)
        )

def main():
    tea_test(_anyio_backend="asyncio")  # or asyncio, or curio