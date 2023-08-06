"""
Big query migration data
"""
import logging

from typing import List
from google.cloud import bigquery

__all__ = ("BigQuery",)

_LOG_PREFIX_ = '[BIGQUERY]%s'


class BigQuery:
    """
    Big Query Dynamic Class
    """
    def __init__(self):
        self.client = bigquery.Client()

    @staticmethod
    def get_filter_with_operator(field: str, value: (str, int), operator:
                                 str = "=") -> str:
        """ Generate filter with operator"""

        if isinstance(value, int):
            query = f"{field}{operator}{value}"
        else:
            query = f"{field}{operator}'{value}'"
        return query

    def get_values(self, values: dict) -> str:
        """ Get values to update"""

        values_list = []
        for key, value in values.items():
            query = self.get_filter_with_operator(key, value)
            if query:
                values_list.append(query)
        return ", ".join(values_list)

    def get_filters(self, filters: List[dict]) -> str:
        """Get filters"""

        filters_list = []
        for filter_obj in filters:
            query = self.get_filter_with_operator(**filter_obj)
            if query:
                filters_list.append(query)
        # TODO: Create for all conditionals
        filters = " AND ".join(filters_list)
        if filters:
            return f"WHERE {filters}"
        return ""

    def update(self, dataset: str, table: str, values: dict,
               filters: List[dict]) -> list:
        """ Update registers on bigquery dynamically """

        _values = self.get_values(values)
        _filters = self.get_filters(filters)

        # Validate.
        self._validate(dataset, _values, table)
        query = f"UPDATE {dataset}.{table} SET {_values} {_filters}"

        # Try to execute query on bq
        errors = [i for i in self.client.query(query)]

        if errors:
            raise Exception(str(errors))

        logging.info(_LOG_PREFIX_, '[UPDATE] {} registers was '
                                   'update on Table {}'
                     .format(len(values), '{}.{}'.format(dataset, table)))

        return errors

    @staticmethod
    def _validate(dataset, values, table):
        """
        Validate data before try to save on bigquery
        :param dataset:
        :param values:
        :param table:
        :return:
        """
        if not dataset or not table:
            raise Exception('Missing table component '
                            'Dataset -> {} :: Table -> {}.'
                            .format(dataset, table))
        if not values:
            raise ValueError('Missing values to be stored.')