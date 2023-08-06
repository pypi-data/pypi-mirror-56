from metaflow.decorators import StepDecorator
from metaflow.exception import MetaflowException
from metaflow.metaflow_config import MAX_ATTEMPTS


class RetryDecorator(StepDecorator):
    name = 'retry'
    defaults = {'times': '3',
                'minutes_between_retries': '2'}

    def step_init(self, flow, graph, step, decos, environment, datastore, logger):
        # The total number of attempts must not exceed MAX_ATTEMPTS.
        # attempts = normal task (1) + retries (N) + @catch fallback (1)
        if int(self.attributes['times']) + 2 > MAX_ATTEMPTS:
            raise MetaflowException('The maximum number of retries is '
                                    '@retry(times=%d).' % (MAX_ATTEMPTS - 2))

    def step_task_retry_count(self):
        return int(self.attributes['times']), 0
