import yaml
from autoclass import autoclass
import os


@autoclass
class Config:
    def __init__(self,
                 project_dir: str,
                 customer: str,
                 src_lang: str,
                 tgt_lang: str,
                 flavor=None,
                 version=1,
                 processors=[],
                 tokenizer=None,
                 truecaser=None,
                 bpe=None,
                 trainer=None
                 ):
        pass

    @staticmethod
    def load(project_dir):
        with open(os.path.join(project_dir, 'config.yml'), "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return Config(project_dir,
                      data['customer'],
                      data['srcLang'],
                      data['tgtLang'],
                      data['flavor'],
                      data['version'],
                      data['processors'],
                      data['tokenizer'],
                      data['truecaser'],
                      data['bpe'],
                      data['trainer']
                      )

    def save(self):
        with open(os.path.join(self.project_dir, 'config.yml'), "w") as file:
            data = {'customer': self.customer,
                    'srcLang': self.src_lang,
                    'tgtLang': self.tgt_lang,
                    'flavor': self.flavor,
                    'version': self.version,
                    'processors': self.processors,
                    'tokenizer': self.tokenizer,
                    'truecaser': self.truecaser,
                    'bpe': self.bpe,
                    'trainer': self.trainer
                    }

            yaml.dump(data, file, sort_keys=False)

    @staticmethod
    def add_tokenizer(src_tokenizer, tgt_tokenizer, project_dir):
        with open(os.path.join(project_dir, 'config.yml'), "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            data['tokenizer'] = {
                'src': src_tokenizer,
                'tgt': tgt_tokenizer
            }

            total_data = {
                'customer': data['customer'],
                'srcLang': data['srcLang'],
                'tgtLang': data['tgtLang'],
                'flavor': data['flavor'],
                'version': data['version'],
                'processors': data['processors'],
                'tokenizer': data['tokenizer'],
                'truecaser': data['truecaser'],
                'bpe': data['bpe'],
                'trainer': data['trainer']
            }

            with open(os.path.join(project_dir, 'config.yml'), "w") as file2:
                yaml.dump(total_data, file2, sort_keys=False)
