import re

def validate_id(id):
    return type(id) == int and id > 0

def validate_name(name):
    return type(name) == str and len(name) > 0

def validate_datetime(datetime):
    match = re.fullmatch(r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}', datetime)

    return bool(match)

def validate_department(d):
    #validating the existance of every field
    fields = ['id', 'department']

    for field in fields:
        if not field in d.keys():
            return False

    return validate_id(d['id']) and validate_name(d['department'])

def validate_job(d):
    fields = ['id', 'job']

    for field in fields:
        if not field in d.keys():
            return False

    return validate_id(d['id']) and validate_name(d['job'])

def validate_employee(d):
    fields = ['id', 'name', 'datetime', 'department_id', 'job_id']

    for field in fields:
        if not field in d.keys():
            return False

    return validate_id(d['id']) and validate_name(d['name']) and \
           validate_datetime(d['datetime']) and validate_id(d['department_id']) and \
           validate_id(d['job_id'])