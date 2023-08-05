from pangeamt_tea.project.workflow.stage.base_stage import BaseStage


class PrepareStage(BaseStage):
    NAME = 'prepare'

    def __init__(self, workflow):
        super().__init__(workflow, self.NAME)

    async def run(self):
        return {

        }