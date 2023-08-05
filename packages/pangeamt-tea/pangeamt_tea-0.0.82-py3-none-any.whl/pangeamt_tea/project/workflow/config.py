import os
import json
from autoclass import autoclass
from pangeamt_tea.project.workflow.stage.init_stage import InitStage
from pangeamt_tea.project.workflow.stage.clean_stage import CleanStage
from pangeamt_tea.project.workflow.stage.prepare_stage import PrepareStage
from pangeamt_tea.project.workflow.stage.train_stage import TrainStage
from pangeamt_tea.project.workflow.stage.eval_stage import EvalStage
from pangeamt_tea.project.workflow.stage.publish_stage import PublishStage


@autoclass
class Config:
    STAGES = [
        InitStage.NAME,
        CleanStage.NAME,
        PrepareStage.NAME,
        TrainStage.NAME,
        EvalStage.NAME,
        PublishStage.NAME,
    ]

    def __init__(self,
        workflow_dir,
        init,
        clean,
        prepare,
        train,
        eval,
        publish):
        pass

    def get_runable_stage(self):
        i = 0
        for i, stage in enumerate(Config.STAGES):
            info = getattr(self, stage)
            if info is None:
                break
            if info['end'] is None:
                return None
        return Config.STAGES[i]

    @staticmethod
    def new(workflow_dir):
        config = Config(
            workflow_dir, None, None, None, None, None, None
        )
        config.save()
        return config

    @staticmethod
    def load(workflow_dir):
        config_file = Config.get_file(workflow_dir)
        with open(config_file, "r") as f:
            data = json.load(f)
        return Config(
            workflow_dir,
            data['init'],
            data['clean'],
            data['prepare'],
            data['train'],
            data['eval'],
            data['publish']
        )

    def set_stage(self, stage, value):
        setattr(self, stage, value)


    @staticmethod
    def get_file(worflow_dir):
        return os.path.join(worflow_dir, 'config.json')

    def save(self):
        config_file = Config.get_file(self.workflow_dir)
        data = {}
        data['init'] = self.init
        data['clean'] = self.clean
        data['prepare'] = self.prepare
        data['train'] = self.train
        data['eval'] = self.eval
        data['publish'] = self.publish
        with open(config_file, 'w',encoding='utf-8') as f:
            json.dump(data, f)


