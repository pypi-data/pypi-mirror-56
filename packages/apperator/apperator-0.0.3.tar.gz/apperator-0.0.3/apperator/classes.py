import os

from jinja2 import Environment, FileSystemLoader, select_autoescape


class Apperator:
    def __init__(self, crd):
        self.crd = crd

    @property
    def labels(self):
        return {
            'apperator.simone.sh/app-name': self.crd['metadata']['name'],
        }
    @property
    def annotations(self):
        return {
            'apperator.simone.sh/app-name': self.crd['metadata']['name'],
        }

    @property
    def env(self):
        return Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), 'templates')
            ),
        )

    def template(self):
        template = self.env.get_template('apperator.jinja')
        return template.render(
            spec=self.crd['spec'],
            annotations=self.annotations,
            labels=self.labels,
            metadata=self.crd['metadata'],
        )
