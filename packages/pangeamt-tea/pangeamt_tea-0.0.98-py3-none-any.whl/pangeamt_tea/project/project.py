import os
from typing import Optional
from autoclass import autoclass
from pangeamt_tea.project.workflow.workflow import Workflow
from pangeamt_tea.project.config import Config


@autoclass
class Project:
    def __init__(self, config: Config, workflow):
        pass

    @staticmethod
    def new(customer: str,
            src_lang: str,
            tgt_lang: str,
            parent_dir: str,
            version: int = 1,
            flavor: Optional[str] = None):

        # Create the project directory
        project_dir_name = f"{customer}_{src_lang}_{tgt_lang}"
        if flavor is not None:
            project_dir_name += f"_{flavor}"
        if version != 1:
            project_dir_name += f"_V{version}"

        if not os.path.isdir(parent_dir):
            raise ProjectNotFoundException(parent_dir, project_dir_name)

        project_dir = os.path.join(parent_dir, project_dir_name)
        if os.path.isdir(project_dir):
            raise ProjectAlreadyExistsException(project_dir)

        os.mkdir(project_dir)

        # Create the data directory
        data_dir = Project.get_data_dir(project_dir)
        os.mkdir(data_dir)

        # Create the config file
        config = Config(
            project_dir=project_dir,
            customer=customer,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
            flavor=flavor,
            version=version
        )
        config.save()

        return Project(config, None)

    @staticmethod
    def get_data_dir(project_dir):
        return os.path.join(project_dir, 'data')

    @staticmethod
    def load(project_dir):
        config = Config.load(project_dir)
        return Project(config, None)

    async def new_workflow(self, force):
        return await Workflow.new(self, force)


class ProjectAlreadyExistsException(Exception):
    def __init__(self, project_dir: str):
        super().__init__(f'`{project_dir}` already exists')


class ProjectNotFoundException(Exception):
    def __init__(self, parent_dir: str, project_dir: str):
        super().__init__(f'`{parent_dir}` not found can not create {project_dir}')
