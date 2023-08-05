"""Class for centralizing CloudSql operations"""
import logging

from typing import List
from pydal import DAL, Field
from pydal.objects import Table


__all__ = ("CloudSqlModel",)


_LOG_PREFIX_ = "[CLOUDSQL]%s"


class CloudSqlModel:
    """
    Class for abstracting the model of the Mysql, Postgresql and SQLite
    on CloudSQL
    """

    session: DAL = None

    def __init__(self, uri: str, migrate: bool = False):
        """Constructor"""
        self.session = DAL(uri, migrate=migrate)

    @staticmethod
    def get_fields(columns: list) -> List[Field]:
        """Get list of pydal field objects"""
        logging.info(
            _LOG_PREFIX_, f"Get table fields {columns}"
        )
        return [Field(i) for i in columns]

    def get_table(self, table_name: str, columns: list) -> Table:
        """Get table of pydal"""
        logging.info(
            _LOG_PREFIX_, f"Generate table with {table_name}"
        )
        columns = self.get_fields(columns)
        if table_name not in self.session.tables:
            self.session.define_table(table_name, *columns)
        return self.session[table_name]
