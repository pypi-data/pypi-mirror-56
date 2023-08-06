import types
import json
import pandas as pd
import csv
import mockdata.functions as fx

class csv_mock():
    def __init__(self, csv, schema=""):
        self.file_name = csv
        self.schema_file = schema
    
    def to_json(self):
        record_list = []
        if self.schema_file != "":
            record_list = fx.extract_repeated_records(self.schema_file)
        df = pd.read_csv(self.file_name)
        df = df.where(pd.notnull(df), None)
        return fx.extract_list_dictionary(df, record_list)


class sheet_tag_mock():
    def __init__(self, googlesheet_id, sheet_name, schema):
        self.file_name = csv
        self.schema_file = schema
    
    def to_json(self):
        record_list = fx.extract_repeated_records(self.schema_file)
        df = pd.read_csv(self.file_name)
        df = df.where(pd.notnull(df), None)
        return fx.extract_list_dictionary(df, record_list)