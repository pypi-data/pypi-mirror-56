"""
ExcelConnector(): Connection between Excel and SQLite
"""

import logging
from typing import List, Dict

import openpyxl
import pandas as pd

logger = logging.getLogger('ExcelConnector')


class ExcelConnector:
    """
    - Extract Data from Excel and load to SQLite
    - Extract Data from SQLite and load to Excel
    """
    def __init__(self, dbconn):
        self.__dbconn = dbconn

    def create_tables(self, file_path: str) -> None:
        """
        Creates DB tables
        :param file_path: absolute path to the .sql file
        :return: None
        """
        ddl_sql = open(file_path, 'r').read()
        self.__dbconn.executescript(ddl_sql)

    def extract(self, file_path: str, table_name: str) -> None:
        """
        Extract data from Excel
        :param file_path: Absolute path of Fyle
        :param table_name: Table name in which data is to be stored
        :return: None
        """
        logger.info('Extracting excel file.')

        df = pd.read_excel(file_path)
        df.to_sql(table_name, self.__dbconn, if_exists='append', index=False)

        logger.info('Excel data stored to database')

    def load_worksheet(self, table_name, file_path) -> None:
        """
        Load single worksheet
        :param table_name: Name of the table
        :param file_path: Absolute path of the file
        :return: None
        """
        logger.info('Creating Excel File')

        df = pd.read_sql_query(sql='select * from {0}'.format(table_name), con=self.__dbconn)
        df.to_excel(file_path, index=False)

        logger.info('Excel file successfully created')

    def load_worksheets(self, file_path: str, data_frames: List[Dict]) -> None:
        """
        Load tables to worksheets
        :param file_path: Absolute path of the file
        :param data_frames: List of dicts with table name 'table' and worksheet name 'sheet_name'
        :return: None
        """
        logger.info('Creating Excel File')

        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

        for data_frame in data_frames:
            df = pd.read_sql_query(sql='select * from {0}'.format(data_frame['table']), con=self.__dbconn)
            df.to_excel(writer, sheet_name=data_frame['sheet_name'], index=False)

            logger.info('Excel file successfully created.')

        writer.save()

    @staticmethod
    def update_cell(file_path: str, cell: str, new_value: any) -> None:
        """
        Update a particular cell of google sheet
        :param file_path: path of the worksheet
        :param cell: cell to be updated
        :param new_value: new value of the cell
        :return: None
        """
        logger.info('Writing value %s to cell %s', new_value, cell)
        workbook = openpyxl.load_workbook(filename=file_path)
        worksheet = workbook.worksheets[0]
        worksheet[cell] = new_value
        workbook.save(file_path)

    @staticmethod
    def is_empty(file_path: str) -> bool:
        """
        Check if excel file is empty
        :param file_path: Absolute path of the file
        :return: True if empty and False if not empty
        """
        df_excel = pd.read_excel(file_path)

        if len(df_excel.index) > 0:
            return False
        return True
