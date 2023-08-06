import os

from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator


class EnvironmentDecorator(StepDecorator):
    name = 'environment'
    defaults = {'vars': {}}

    def step_init(self, flow, graph, step, decos, environment, datastore, logger):
        os.environ.update(self.attributes['vars'].items())
