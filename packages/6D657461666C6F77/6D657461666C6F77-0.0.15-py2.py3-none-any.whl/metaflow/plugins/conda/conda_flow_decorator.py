from metaflow.decorators import FlowDecorator
from metaflow.environment import InvalidEnvironmentException


class CondaFlowDecorator(FlowDecorator):
    name = 'conda_base'
    defaults = {'libraries': {},
                'python': None,
                'disabled': None}

    def flow_init(self, flow, graph, environment, datastore, logger):
        if environment.TYPE != 'conda':
            raise InvalidEnvironmentException('The *@conda* decorator requires '
                                              '--environment=conda')