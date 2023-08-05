import json
import time

from starling.config import CONFIG
from starling.exception import RetryTaskExitError, RetryTaskError, RetryTaskSkipAuthError
from starling.helper import retry_task, EnhancedJSONEncoder
from starling.types import ScrapperData, TaskData
from .blueprint_scrapper import BlueprintScrapper


class Scrapper:
    @staticmethod
    def _run_task(task: TaskData, scrapper_data: ScrapperData):
        package_name, classname = task.action.rsplit('.', 1)
        blueprint = getattr(__import__(package_name, fromlist=[package_name]), classname)(scrapper_data, task)
        fetched_data = blueprint.fetch()
        time.sleep(blueprint.interval())
        return fetched_data

    @staticmethod
    @retry_task()
    def _run(scrapper: BlueprintScrapper, is_auth=True):
        if is_auth:
            scrapper.authenticate()
        for task in [task for task in scrapper.data.tasks if task.fetched_data is None]:
            task.fetched_data = Scrapper._run_task(task, scrapper.data)

    @staticmethod
    def run(scrapper: BlueprintScrapper, json_output=True, **kwargs):
        CONFIG.update(kwargs)
        try:
            Scrapper._run(scrapper)
        except (RetryTaskExitError, RetryTaskError, RetryTaskSkipAuthError) as e:
            scrapper.data.is_valid = False
            scrapper.data.error_message = e.message
            scrapper.data.error_extra = e.extra
        return json.dumps(scrapper.data, cls=EnhancedJSONEncoder) if json_output else scrapper.data
