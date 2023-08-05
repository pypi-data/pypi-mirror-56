import json

import pytest

from starling.app import Scrapper
from starling.blueprint_action import BlueprintAction
from starling.blueprint_scrapper import BlueprintScrapper
from starling.types import ScrapperData, TaskData


class MyScrapper(BlueprintScrapper):
    def tasks(self, action):
        if action == 'tests.starling.test_app.MyAction1':
            return [
                TaskData(action=action, criteria={'from': '20191001', 'to': '20191031'}),
                TaskData(action=action, criteria={'from': '20191101', 'to': '20191130'})
            ]
        else:
            return [TaskData(action=action)]

    @property
    def actions(self):
        return [
            'tests.starling.test_app.MyAction1',
            'tests.starling.test_app.MyAction2',
            'tests.starling.test_app.MyAction3'
        ]

    def authenticate(self):
        pass


class MyAttributeErrorScrapper(BlueprintScrapper):
    @property
    def actions(self):
        return [
            'tests.starling.test_app.MyMyAction1'
        ]

    def authenticate(self):
        pass


class MyAction1(BlueprintAction):
    def fetch(self):
        return self.scrapper_data.candidate

    def interval(self):
        return 0


class MyAction2(BlueprintAction):
    def fetch(self):
        return self.scrapper_data.candidate


class MyAction3(BlueprintAction):
    def fetch(self):
        return self.scrapper_data.candidate


def test_scrapper():
    res = Scrapper.run(MyScrapper(ScrapperData('place', {'place_id': '123123'})), json_output=False)
    assert len(res.tasks) == 4
    assert res.tasks[0].criteria['from'] == '20191001'
    assert res.tasks[1].criteria['from'] == '20191101'


def test_scrapper_deny_actions():
    res = Scrapper.run(MyScrapper(ScrapperData('place', {'place_id': '123123'}),
                                  deny_actions=[
                                      'tests.starling.test_app.MyAction2',
                                      'tests.starling.test_app.MyAction3'
                                  ]), json_output=False)
    assert len(res.tasks) == 2


def test_scrapper_json_output():
    res = json.loads(Scrapper.run(MyScrapper(ScrapperData('place', {'place_id': '123123'})), json_output=True))
    assert len(res['tasks']) == 4


def test_scrapper_with_attribute_error():
    with pytest.raises(AttributeError) as e:
        Scrapper.run(MyAttributeErrorScrapper(ScrapperData('place', {'place_id': '123123'})))

    assert "module" in str(e.value)
