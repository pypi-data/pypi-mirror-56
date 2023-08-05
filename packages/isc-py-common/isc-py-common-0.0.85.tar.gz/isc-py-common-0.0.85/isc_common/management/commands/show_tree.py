import json
import logging

from django.core.management import BaseCommand

from kaf_pas.ckk.models.item_view import Item_view

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int)
        parser.add_argument('--stmp1', type=str)
        parser.add_argument('--stmp2', type=str)

    def handle(self, *args, **options):
        json_str = ''' {
                            "componentId": "isc_TreeGrid_0",
                            "data": {
                                "_constructor": "AdvancedCriteria",
                                "criteria": [
                                    {
                                        "_constructor": "AdvancedCriteria",
                                        "criteria": [
                                            {
                                                "fieldName": "STMP_2__value_str",
                                                "operator": "iContains",
                                                "value": "К131.31.40.030"
                                            },
                                            {
                                                "fieldName": "ts",
                                                "operator": "equals",
                                                "value": 1572549067254
                                            }
                                        ],
                                        "operator": "and"
                                    },
                                    {
                                        "fieldName": "parent_id",
                                        "operator": "equals",
                                        "value": null
                                    }
                                ],
                                "operator": "and"
                            },
                            "dataPageSize": 200,
                            "dataSource": "isc_RestDataSourceSS_89",
                            "drawAheadRatio": 1.2,
                            "endRow": 200,
                            "oldValues": null,
                            "operationId": "isc_RestDataSourceSS_89_fetch",
                            "operationType": "fetch",
                            "sortBy": [
                                "STMP_1__value_str"
                            ],
                            "startRow": 0,
                            "textMatchStyle": "substring"
                        }'''
        _json = json.loads(json_str)

        # def get_range_rows(self, start=None, end=None, function=None, json=None, distinct_field_names=None, *args):
        start = _json.get('startRow')
        end = _json.get('endRow')
        for item in Item_view.objects.filter().get_range_rows(start=start, end=end, json=_json):
            print(item)
