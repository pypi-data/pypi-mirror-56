import types
import json
import pandas as pd
import csv

def exists(attr, obj):
    return True if attr.split(".")[0] in obj else False

def joiner(lst, separator="."):
    # initialize an empty string 
    str_res = ""  
    iterations=0
    # traverse in the string   
    for ele in lst:  
        if iterations==0:
            str_res += ele
        else: 
            str_res += ("." + ele)
        iterations=1
        
    # return string   
    return str_res  

def is_list(obj):
    return type(obj)==list

def is_dict(obj):
    return type(obj)==dict

def get_sub_field(field, position):
    return field.split('.')[position]

def is_leaf(field):
    return True if not "." in field else False

def add_leaf(obj, field, value={}):
    try:
        if value.is_integer():
            value = int(value)
    except:
        pass
    
    obj[field] = value
    
    return obj

def add_non_leaf(obj, field, record_list=[]):
    
    if field.split(".")[0] in record_list:
        obj[field] = [{}]
    else:
        obj[field] = {}

    return obj
            
def add_column(obj, field, value=None, record_list=[], row=[] ):
    if is_list(obj):
        if not(obj): 
            obj.append({})
        elif not(obj[0]) == {}:
            if is_repeated_record(row) and field.split(".")[0] == list(obj[-1].keys())[0]: #ß "" if  not(list(obj[-1].keys())) else list(obj[-1].keys())[0]:
                obj.append({})        
        add_column(obj[-1], field, value,  record_list, row)

    else:   
        if is_leaf(field):
            add_leaf(obj, field, value)
        elif not exists(field.split(".")[0], obj):
            add_non_leaf(obj, field.split(".")[0], record_list)
            
        if not is_leaf(field):
            if is_list(obj):
                add_column( obj[-1][field.split(".")[0]], joiner(field.split(".")[1:]) , value, record_list, row )  # iterate next key of the field and pass the last object in the list
            else:
                add_column( obj[field.split(".")[0]], joiner(field.split(".")[1:]) , value, record_list, row ) # iterate next key of the field and pass pass the object created

    return obj

def load_dictionary(dct, row, record_list):
    if is_repeated_record(row):
        d = dct[-1]
    else:
        dct.append({})
        d = dct[-1]
        
    for field, value in row.iteritems():
        if not(is_repeated_record(row)) or is_record_field(record_list, field.split(".")):
            add_column(d, field, value, record_list, row)
    return dct
       

def is_repeated_record(row, separator='.'):
    if type(row)==list:
        if not(row): 
            return False 
    else:
        primary_fields = [[k,v] for k, v in row.items() if separator not in k]
        for k,v in primary_fields:
            if str(v)!='nan' and v != None:
                return False
        return True

def is_record_field(l1, l2):
    for a in l1:
        for b in l2:
            if a==b:
                return True
    return False

def extract_list_dictionary(df, record_list):
    list_dictionary = []
    for index, row in df.iterrows():
        load_dictionary(list_dictionary, row, record_list)
    return list_dictionary


def iterate_obj(list_record, obj ):
    if isinstance(obj, list):
        for i in obj:
            iterate_obj(list_record, i)
    else:   
        # print("dictonary : {}".format(obj))
        field_mode = ""
        for k, v in obj.items():   
            if isinstance(v, list):
                iterate_obj(list_record, v)         
            if k.upper() == "NAME":
                field_name = v
            elif k.upper() == "MODE":
                field_mode = v
        if field_mode == "REPEATED":
            list_record.append(field_name)
    return list_record

def extract_repeated_records(schema_filename):
    list_record=[]
    with open(schema_filename) as json_file:
        schema = json.load(json_file)
    list_result = iterate_obj(list_record,schema)
    return list_result
