import time


class AbstractStage:
    def __init__(self, workflow, name):
        self._workflow = workflow
        self._name = name
        self._start = None
        self._end = None

    async def run_with_time_report(self, *args, **kwargs):
        self._start = time.time()
        report = await self.run(*args, **kwargs)
        self._end = time.time()
        return {
            'start': self._start,
            'end': self._end,
            'report': report
        }

    async def run(self, *args, **kwargs):
        raise ValueError('This method should be')
        pass
