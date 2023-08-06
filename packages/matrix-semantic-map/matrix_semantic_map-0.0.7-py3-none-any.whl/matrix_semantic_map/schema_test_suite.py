import json
from jsonschema import Draft4Validator, RefResolver, SchemaError
import warnings
import subprocess
import os
import glob


def get_json_from_file(filename, warn = False):
    """Loads json from a file.
    Optionally specify warn = True to warn, rather than
    fail if file not found."""
    f = open(filename, 'r')
    fc = f.read()
    f.close()
    return json.loads(fc)


def get_validator(filename, base_uri = ''):
    """Load schema from JSON file;
    Check whether it's a valid schema;
    Return a Draft4Validator object.
    Optionally specify a base URI for relative path
    resolution of JSON pointers (This is especially useful
    for local resolution via base_uri of form file://{some_path}/)
    """
   
    schema = get_json_from_file(filename)
    try:
        # Check schema via class method call. Works, despite IDE complaining
        # However, it appears that this doesn't catch every schema issue.
        Draft4Validator.check_schema(schema)
        print("%s is a valid JSON schema" % filename)
    except SchemaError:
        raise
    if base_uri:
        resolver = RefResolver(base_uri = base_uri,
                               referrer = filename)
    else:
        resolver = None
    return Draft4Validator(schema = schema,
                           resolver = resolver)


def validate(validator, instance):
    """Validate an instance of a schema and report errors."""
    if validator.is_valid(instance):
        print("JSON schema validation Passes")
        return True
    else:
        es = validator.iter_errors(instance)
        recurse_through_errors(es)
        print("JSON schema validation Fails")
        return False


def recurse_through_errors(es, level = 0):
    """Recurse through errors posting message 
    and schema path until context is empty"""
    # Assuming blank context is a sufficient escape clause here.
    for e in es:
        warnings.warn(
            "***"*level + " subschema level " + str(level) + "\t".join([e.message,
            "Path to error:" + str(e.absolute_schema_path)]) + "\n")
        if e.context:
            level += 1
            recurse_through_errors(e.context, level = level)
            

def test_local(path_to_schema_dir, schema_file, test_dir):
    """Tests all instances in a test_folder against a single schema.
    Assumes all schema files in single dir.
    Assumes all *.json files in the test_dir should validate against the schema.
       * path_to_schema_dir:  Absolute or relative path to schema dir
       * schema_file: schema file name
       * test_dir: path to test directory (absolute or local to schema dir)
    """
    os.chdir(path_to_schema_dir)
    pwd = subprocess.check_output('pwd').decode("utf-8").rstrip()
    base_uri = "file://" + pwd + "/"
    sv = get_validator(schema_file, base_uri)
    test_files = glob.glob(pathname=test_dir + '/*.json')
    # print("Found test files: %s in %s" % (str(test_files), test_dir))
    for instance_file in test_files:
        i = get_json_from_file(instance_file)
        print("Testing: %s" % instance_file)
        validate(sv, i)
