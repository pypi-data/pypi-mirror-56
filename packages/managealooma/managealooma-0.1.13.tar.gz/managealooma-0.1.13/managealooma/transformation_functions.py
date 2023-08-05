import json
import re
import ast
from copy import deepcopy


def add_column_based_on_null(event, field, new_field, new_value_if_null, new_value_if_not_null):
    """ Checks and adds a value to a new field based on NULL

    :param event: A dictionary
    :param field: The name of the field to check
    :param new_field: The name of the new field
    :param new_value_if_null: The value for the new_field if field IS NULL
    :param new_value_if_not_null: The value for the new_field if field IS NOT NULL
    :return: An altered dictionary

    Examples:

    .. code-block:: python

        # Example #1
        event = {'do i have digits?': '1234'}
        event = add_column_based_on_null(event, field='do i have digits?', new_field='digits', new_value_if_null='N', new_value_if_not_null='Y')
        event = {'digits': 'Y',
                'do i have digits?': '1234'}

        # Example #2
        event = {'do i have digits?': None}
        event = add_column_based_on_null(event, field='do i have digits?', new_field='digits', new_value_if_null='N', new_value_if_not_null='Y')
        event = {'digits': 'N',
                'do i have digits?': None}

    """
    if field in event:
        if event[field] is None:
            event[new_field] = new_value_if_null
        else:
            event[new_field] = new_value_if_not_null

    return event


def add_columns_with_default(event, field_and_default_dict):
    """ Adds a column with the default value to every event where it's not already present

    :param event: A dictionary
    :param field_and_default_dict: A dictionary with keys and default values {field_1: default_for_field_1, field_2: default_for_field_2}
    :return: An altered dictionary

    Examples:

    .. code-block:: python

        # Example #1
        event = {'an existing column': 'some value'}
        event = add_columns_with_default(event, field_and_default_dict={"new column 1": 'my default of 1', "new column two": 2})
        event = {'an existing column': 'some value',
                'new column 1': 'my default of 1',
                'new column two': 2}

        # Example #2
        event = {'an existing column': 'some value'}
        event = add_columns_with_default(event, field_and_default_dict={"mark_for_delete": False})
        event = {'an existing column': 'some value',
                'mark_for_delete': False}

    """

    for k, v in field_and_default_dict.items():
        if k not in event:
            event[k] = v
    return event


def add_composite_key(event, field_list, key_name):
    """ Creates a composite key to be used for a unique ID.

    :param event: A dictionary
    :param field_list: A list of fields to combine to make the key
    :param key_name: The name of the new key field
    :return: An altered dictionary

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': 1234,
                'a_second_field': '2019-01-01',
                'a_third_field': 'abc'}
        event = add_composite_key(event, field_list=['a_field', 'a_second_field', 'a_third_field'], key_name='my_derived_key')
        event = {'a_field': 1234,
                'a_second_field': '2019-01-01',
                'a_third_field': 'abc',
                'my_derived_key':
                '1234-2019-01-01-abc'}

    """

    key_list = []
    for field in field_list:
        key_list.append(event[field])

    if None in key_list:
        raise Exception('Missing values in composite key')
    else:
        key_list = [str(x) for x in key_list]
        event[key_name] = '-'.join(key_list)
    return event


def add_duplicate_fields(event, field_name, suffix_or_suffix_list, keep_original=False):
    """ Add duplicate values of a field with a suffix

    :param event: A dictionary
    :param field_name: The name of the field to duplicate
    :param suffix_or_suffix_list: A single or list of suffixes to add to the field_name in the duplicates
    :param keep_original: True to keep the original field also
    :return: An altered dictionary

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': 'a_value'}
        event = add_duplicate_fields(event, field_name='a_field', suffix_or_suffix_list='my_suffix', keep_original=False)
        event = {'a_field_my_suffix': 'a_value'}

        # Example #2
        event = {'a_field': 'a_value'}
        event = add_duplicate_fields(event, field_name='a_field', suffix_or_suffix_list='my_suffix', keep_original=True)
        event = {'a_field': 'a_value',
                'a_field_my_suffix': 'a_value'}

        # Example #3
        event = {'a_field': 'a_value'}
        event = add_duplicate_fields(event, field_name='a_field', suffix_or_suffix_list=['my_suffix','my_second_suffix'], keep_original=False)
        event = {'a_field_my_second_suffix': 'a_value',
                'a_field_my_suffix': 'a_value'}

    """

    if type(suffix_or_suffix_list) is not list:
        suffix_or_suffix_list = [suffix_or_suffix_list]

    if field_name in event:
        for suffix in suffix_or_suffix_list:
            event[field_name + '_' + suffix] = event[field_name]

    if not keep_original:
        del event[field_name]

    return event


def add_suffix(event, fields, suffix, separator='_'):
    """ Adds a suffix to a field or list of fields

    :param event: A dict with the entire event
    :param field_or_field_list: A single field or list of fields for which to add a suffix
    :param suffix: The suffix to add to the fields
    :param separator: The character to place between the name and the suffix
    :return: An altered event with the altered field names

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': 'a_value'}
        event = add_suffix(event, fields='a_field', suffix='an_ending')
        event = {'a_field_an_ending': 'a_value'}

        # Example #2
        event = {'a_field': 'a_value'}
        event = add_suffix(event, fields='a_field', suffix='an_ending', separator='---')
        event = {'a_field---an_ending': 'a_value'}

        # Example #3
        event = {'a_field': 'a_value',
                'another_field': 'another_value'}
        event = add_suffix(event, fields=['a_field', 'another_field'], suffix='an_ending')
        event = {'a_field_an_ending': 'a_value',
                'another_field_an_ending': 'another_value'}

    """

    if type(fields) is not list:
        fields = [fields]

    for k, v in event.items():
        if k in fields:
            event[k + separator + suffix] = event[k]
            del event[k]

    return event


def convert_all_event_fields_to_snake_case(event):
    """ Converts all keys in an event to snake case.
    If a key is Partially_SnakeCase we'll get 2 underscores where there is currently one like partially__snake_case

    :param event: An Alooma event
    :return: A transformed event with all the keys in snake_case

    Examples:

    .. code-block:: python

        # Example #1
        event = {'_metadata': {},
                'TitleCase': 'to_snake_case',
                'camelCase': 'to_snake_case',
                'snake_case': 'to_snake_case'}
        event = convert_all_event_fields_to_snake_case(event)
        event = {'_metadata': {},
                'camel_case': 'to_snake_case',
                'snake_case': 'to_snake_case',
                'title_case': 'to_snake_case'}


    """

    new_event = {}

    for k, v in event.items():
        new_event[convert_string_to_snake_case(k).replace(' ', '_')] = v

    new_event['_metadata'] = deepcopy(event['_metadata'])
    return new_event


def convert_dictionary_fields_to_string(event, field_or_field_list):
    """ Dumps a list of fields to a string to keep Alooma from auto-parsing

    :param event: A dict with the entire event
    :param field_or_field_list: A single field or list of fields to json.dumps to keep Alooma from doing infinte de-nesting
    :return: A new event

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_dict': {'field_one': 1,
                'field_two': 2}}
        event = convert_dictionary_fields_to_string(event, field_or_field_list='a_dict')
        event = {'a_dict': '{"field_one": 1, "field_two": 2}'}

        # Example #2
        event = {'a_dict': {'field_one': 1,
                            'field_two': 2},
                'a_second_dict': {'field_one': 1,
                                'field_two': 2}}
        event = convert_dictionary_fields_to_string(event, field_or_field_list=['a_dict', 'a_second_dict'])
        event = {'a_dict': '{"field_one": 1, "field_two": 2}',
                'a_second_dict': '{"field_one": 1, "field_two": 2}'}

    """

    if type(field_or_field_list) is not list:
        field_or_field_list = [field_or_field_list]

    for field in field_or_field_list:
        if field in event and event[field] is not None:
            try:
                event[field] = json.dumps(event[field])
            except:
                pass

    return event


def convert_null_to_zero(event, field_or_field_list):
    """ Converts the value in a field or field list from None to 0

    :param event: a dict with the event
    :param field_or_field_list: A single field or list of fields to convert to 0 if null
    :return: the updated event

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': None}
        event = convert_null_to_zero(event, field_or_field_list='a_field')
        event = {'a_field': 0}

        # Example #2
        event = {'a_field': None,
                'another_field': None}
        event = convert_null_to_zero(event, field_list=['a_field', 'another_field'])
        event = {'a_field': 0,
                'another_field': 0}

    """

    if type(field_or_field_list) is str:
        field_or_field_list = [field_or_field_list]

    for field in field_or_field_list:
        if field in event and event[field] is None:
            event[field] = 0

    return event


def convert_spaces_and_special_characters_to_underscore(name):
    """ Converts spaces and special characters to underscore so 'Thi$ i# jun&' becomes 'thi__i__jun_'

    :param name: A string
    :return: An altered string

    Example use case:
    - A string might have special characters at the end when they are really the same field such as  My_Field$ and My_Field#
    - We use this to covert the names to "my_field" to combine the values so the events will be easily grouped together

    Examples:

    .. code-block:: python

        # Example #1
        input_string = '$Scr "get-rid^-of-the@" special #characters%&space'
        output_string = convert_spaces_and_special_characters_to_underscore(input_string)
        output_string = '_scr__get_rid__of_the___special__characters__space'

    """

    clean_name = re.sub(r'[\W_]', '_', name)
    return clean_name.lower()


def convert_string_to_snake_case(name):
    """ Converts a string to Snake Case

    :param name: A string
    :return: A string in snake case

    Example use case:
    - Events from might have custom properties in camelCase like userId, and userEmail
    - Use this to rename keys to user_id and user_email for better ease of reading in the database

    Examples:

    .. code-block:: python

        # Example #1
        input_string = 'MakeThisSnakeCase'
        output_string = convert_string_to_snake_case(input_string)
        output_string = 'make_this_snake_case'

        # Example #2
        input_string = 'Make This Snake Case'
        output_string = convert_string_to_snake_case(input_string)
        output_string = 'make_this_snake_case'

        # Example #3
        input_string = 'keep_this_snake_case'
        output_string = convert_string_to_snake_case(input_string)
        output_string = 'keep_this_snake_case'

    """

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    sl = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return sl.replace(' ', '')


def convert_values_to_none(event, field_or_field_list, field_values=None):
    """ Changes a field to None. If a field value is specified then only that value will be changed to None

    :param event: A dictionary
    :param field_or_field_list: A single field or list of fields  to convert to None
    :param field_values: The value to convert to None. If specified only these values are converted to None
    :return: An altered dictionary

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': 'a_value'}
        event = convert_values_to_none(event, field_or_field_list='a_field')
        event = {'a_field': None}

        # Example #2
        event = {'a_field': 'a_value',
                'another_field': 'another_value'
        event = convert_values_to_none(event, field_or_field_list=['a_field', 'another_field'])
        event = {'a_field': None,
                'another_field': None}

        # Example #3
        event = {'a_field': 'a_value',
                'another_field': 'another_value'
        event = convert_values_to_none(event, fields=['a_field', 'another_field'], field_values='a_value')
        event = {'a_field': None,
                'another_field': 'another_value'}

        # Example #4
        event = {'a_field': 'a_value',
                'another_field': 'another_value'
        event = convert_values_to_none(event, fields=['a_field', 'another_field'], field_values=['a_value', 'another_value'])
        event = {'a_field': None,
                'another_field': None}

    """

    if type(field_or_field_list) is not list:
        field_or_field_list = [field_or_field_list]

    if field_values is not None:
        if type(field_values) is not list:
            field_values = [field_values]

    for field in field_or_field_list:
        if field in event and field_values is None:
            event[field] = None
        elif field in event and event[field] in field_values:
            event[field] = None

    return event


def convert_empty_value_to_none(event, key_name):
    """ Changes an empty string of "" or " ", and empty list of [] or an empty dictionary of {} to None so it will be NULL in the database

    :param event: A dictionary
    :param key_name: The key for which to check for empty strings
    :return: An altered dictionary

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': ' '}
        event = convert_empty_value_to_none(event, key_name='a_field')
        event = {'a_field': None}

        # Example #2
        event = {'a_field': '{}'}
        event = convert_empty_value_to_none(event, key_name='a_field')
        event = {'a_field': None}

        # Example #3
        event = {'a_field': {}}
        event = convert_empty_value_to_none(event, key_name='a_field')
        event = {'a_field': None}

    """

    if key_name in event:
        if type(event[key_name]) == str and (event[key_name] == '' or event[key_name].strip() == '' or event[key_name] == '{}' or event[key_name] == '[]'):
            event[key_name] = None

        # Converts an empty list or dictionary to None
        if not event[key_name]:
            event[key_name] = None

    return event


def convert_event_type_case(event, case_force_upper=False):
    """ Forces upper of lower case for event types at the end of the code engine.  For Snowfalke force UPPER and for Redshift force lower.

    :param event: A dict with the entire event
    :param case_force_upper: True to for upper case.
    :return: An event with the case altered in event_type

    Examples:

    .. code-block:: python

        # Example #1
        event = {'_metadata': {'event_type': 'My_SCHEMA.my_table'}}
        event = convert_event_type_case(event)
        event = {'_metadata': {'event_type': 'my_schema.my_table'}}

        # Example #2
        event = {'_metadata': {'event_type': 'My_SCHEMA.my_table'}}
        event = convert_event_type_case(event, case_force_upper=True)
        event = {'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'}}

    """

    if case_force_upper:
        if type(event) == list:
            for each_event in event:
                if 'event_type' in each_event['_metadata']:
                    each_event['_metadata']['event_type'] = each_event['_metadata']['event_type'].upper()
        else:
            if 'event_type' in event['_metadata']:
                event['_metadata']['event_type'] = event['_metadata']['event_type'].upper()
    else:
        if type(event) == list:
            for each_event in event:
                if 'event_type' in each_event['_metadata']:
                    each_event['_metadata']['event_type'] = each_event['_metadata']['event_type'].lower()
        else:
            if 'event_type' in event['_metadata']:
                event['_metadata']['event_type'] = event['_metadata']['event_type'].lower()

    return event


def flatten_json(event, field_or_field_list, levels, keep_original=False, dump_to_string=False):
    """ Flattens a list of fields from a dictionary n levels

    :param event: the event that you want to pass through the function (formatted as a dictionary)
    :param field_or_field_list: A field or list of the fields that you want to flatten N levels deep
    :param levels: The number of levels that you want to parse the fields
    :param keep_original: True if you want to keep the original field in the event, false if you want to delete it
    :return:  The transformed event

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_dict': {'field_one': 1,
                            'field_two': 2}}
        event = flatten_json(event, field_or_field_list='a_dict', levels=1)
        event = {'a_dict_field_one': 1,
                'a_dict_field_two': 2}

        # Example #2
        event = {'a_dict': {'field_one': 1,
                            'field_two': 2},
                'a_second_dict': {'field_one': {'one more': 1.1,
                                                'one more again': 1.2},
                                'field_two': 2}}
        event = flatten_json(event, field_or_field_list=['a_dict','a_second_dict'], levels=1)
        event = {'a_dict_field_one': 1,
                'a_dict_field_two': 2,
                'a_second_dict_field_one': {'one more': 1.1, 'one more again': 1.2},
                'a_second_dict_field_two': 2}

        # Example #3
        event = {'a_dict': {'field_one': 1,
                            'field_two': 2},
                'a_second_dict': {'field_one': {'one more': 1.1,
                                                'one more again': 1.2},
                                'field_two': 2}}
        event = flatten_json(event, field_or_field_list=['a_dict','a_second_dict'], levels=2)
        event = {'a_dict_field_one': 1,
                'a_dict_field_two': 2,
                'a_second_dict_field_one_one more': 1.1,
                'a_second_dict_field_one_one more again': 1.2,
                'a_second_dict_field_two': 2}

    """

    # Turns a single field into a list
    if type(field_or_field_list) is str:
        field_or_field_list = [field_or_field_list]

    for field in field_or_field_list:
        field = field.lower()
        if field in event.keys():

            # make a copy of the original event to be adding back to event if specified
            original_copy = event[field]

            counter = 0
            pre_fix_list = []
            pre_fix_list.append(field)

            while counter < levels:

                next_level_pre_fix_list = []
                for pre_fix in pre_fix_list:
                    pre_fix_underscore = pre_fix.lower() + '_'

                    event = flatten_json_1_level(event, field_name=pre_fix, field_name_underscore=pre_fix_underscore, dump_to_string=dump_to_string)
                    next_level_pre_fix_list.append(pre_fix_underscore)

                for n in next_level_pre_fix_list:
                    for k in event.keys():

                        if str(k).startswith(n):
                            pre_fix_list.append(k)

                    pre_fix_list = [p for p in pre_fix_list if p != n[:-1]]

                counter += 1

            if keep_original:
                if type(original_copy) is dict and original_copy != {} and dump_to_string:
                    event[field] = json.dumps(original_copy)
                elif dump_to_string:
                    event[field] = original_copy
                else:
                    try:
                        event[field] = json.loads(original_copy)
                    except:
                        try:
                            event[field] = ast.literal_eval(original_copy)
                        except:
                            event[field] = original_copy

    return event


def flatten_json_1_level(event, field_name, field_name_underscore, dump_to_string):
    """ Flattens a JSON field 1 level. This function is used in flatten JSON

    :param event: A dictionary
    :param field_name: The field name to flatten
    :param field_name_underscore: The field name with an underscore appended
    :param dump_to_string: If true any remaining dictionaries will be converted to a string with json.dumps
    :return: An event with the field flattened

    Examples:

    .. code-block:: python

        # Example #1
        event = {'my_field': "{\"a\": None, \"b\"}"}
        event = flatten_json_1_level(event=input_event, field_name='my_field', field_name_underscore='my_field_', dump_to_string=True)
        output_event = {'my_field_a': None,
                        'my_field_b': 2}

    """

    # Load strings to JSON when possible, otherwise return the event
    if type(event[field_name]) is not dict:
        try:
            event[field_name] = json.loads(event[field_name])
        except:
            try:
                event[field_name] = ast.literal_eval(event[field_name])
            except:
                return event

    # iterate through the dictionary and flatten a single level
    try:
        for k, v in event[field_name].items():
            if type(v) is dict and dump_to_string:
                event[field_name_underscore + k.lower()] = json.dumps(v)
            else:
                event[field_name_underscore + k.lower()] = v

        del event[field_name]

    except:
        return event

    return event


def map_key_in_dictionary_to_value(event, mapping_dict, existing_column, new_column, allow_nulls):
    """ Adds a column mapping using a dictionary

    :param event: A dictionary
    :param mapping_dict: A mapping dict such as {1: 'product A', 2: 'product B'}
    :param existing_column:  The column that matches the keys in the mapping dict
    :param new_column: The name of the column to put the values from the mapping dict
    :param allow_nulls: True if the function should let a NULL value in the existing_column pass through. False to throw an error when the existing column has NULL.
    :return: An event with the new_column k, v added

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': 1,
                '_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'}}
        event = map_key_in_dictionary_to_value(event, mapping_dict={1: 'one', 2: 'two'}, existing_column='a_field', new_column='a_mapped_field', allow_nulls=False)
        event = {'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'},
                'a_field': 1,
                'a_mapped_field': 'one'}

        # Example #2
        event = {'a_field': 3,
                '_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'}}
        event = map_key_in_dictionary_to_value(event, mapping_dict={1: 'one', 2: 'two'}, existing_column='a_field', new_column='a_mapped_field', allow_nulls=False)
        Exception: Missing enum transform MY_SCHEMA.MY_TABLE a_field

        # Example #3
        event = {'a_field': None,
                '_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'}}
        event = map_key_in_dictionary_to_value(event, mapping_dict={1: 'one', 2: 'two'}, existing_column='a_field', new_column='a_mapped_field', allow_nulls=True)
        event = {'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'},
                'a_field': None,
                'a_mapped_field': None}

    """

    func_name = 'enum transform ' + event['_metadata']['event_type'] + ' ' + existing_column

    existing_column_value = None

    if existing_column in event:
        existing_column_value = event[existing_column]

    if allow_nulls and (existing_column_value == None or existing_column_value in mapping_dict.keys()):
        event[new_column] = mapping_dict.get(existing_column_value, None)

    elif not allow_nulls and event[existing_column] in mapping_dict.keys():
        event[new_column] = mapping_dict.get(existing_column_value, None)

    else:
        raise Exception('Missing %s' % func_name)

    return event


def map_value_in_list_to_dictionary_key(event, mapping_dict_with_lists, existing_column, new_column, allow_nulls, passthrough):
    """  Maps a value from a list back to the key. Useful to map values to categories.

    :param event: A dictionary
    :param mapping_dict_with_lists:  A mapping dict with lists in the values such as {"baked good": ["cake", "croissant"]}
    :param existing_column: The column with the existing data
    :param new_column: The name of the new column for the added data
    :param allow_nulls: True if the existing column can have NULL. If set to False NULLs will throw an error
    :param passthrough: True if we should pass through a value of the existing column when there is no mapping value in the list
    :return: An altered event

    Examples:

    .. code-block:: python

        # Example #1
        event = {'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'},
                'a_field': 1}
        event = map_value_in_list_to_dictionary_key(event, mapping_dict_with_lists={'1-3': [1, 2, 3], '4-6': [4, 5, 6]}, existing_column='a_field', new_column='a_mapped_field', allow_nulls=False, passthrough=False)
        event = {'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'},
                'a_field': 1,
                'a_mapped_field': '1-3'}

        # Example #2
        event = {'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'},
                'a_field': 7}
        event = map_value_in_list_to_dictionary_key(event, mapping_dict_with_lists={'1-3': [1, 2, 3], '4-6': [4, 5, 6]}, existing_column='a_field', new_column='a_mapped_field', allow_nulls=False, passthrough=False)
        Exception: Missing map_list transform MY_SCHEMA.MY_TABLE a_field

    """

    func_name = 'map_list transform ' + event['_metadata']['event_type'] + ' ' + existing_column

    existing_column_value = event[existing_column]
    event[new_column] = None

    for k, v in mapping_dict_with_lists.items():
        if existing_column_value in v:
            event[new_column] = k

    if event[new_column] is not None:
        return event
    elif passthrough:
        event[new_column] = existing_column_value
    elif allow_nulls:
        return event
    else:
        raise Exception('Missing %s' % func_name)

    return event


def mark_for_delete(event):
    """ We created database triggers in our database to write all rows to a polymorphic deleted records table upon hard delete.
    We log the table_name, the time it was deleted, and the row_to_json
    This function creates a new row that looks like a soft delete came from the database

    :param event: A dictionary that includes the Alooma _metadata dictionary
    :return: A dictionary that looks like a soft deleted row
    
    Examples:

    .. code-block:: python

        # Example #1
        event = {'id': 1,
                'table_name': 'alooma_test',
                'primary_key': '123',
                'old_row_json': '{"id":6, "created_at":"2019-01-01"}',
                '_metadata': {'event_type': 'test'}}
        event = mark_for_delete(event)
        event = {'_metadata': {'event_type': 'alooma_test',
                                'table': 'alooma_test'},
                'created_at': '2019-01-01',
                'id': 6,
                'mark_for_delete': True}

    """

    event['_metadata']['event_type'] = event['table_name']
    event['mark_for_delete'] = True

    # Adds a column with the timestamp of when the row was hard deleted
    if 'created_at' in event:
        event['hard_deleted_at'] = event['created_at']
        del event['created_at']

    # Turns the old_row_json into the fields for the normal event
    for k, v in json.loads(event['old_row_json']).items():
        event[k] = v

    event['_metadata']['table'] = event['table_name']
    del event['old_row_json']
    del event['primary_key']
    del event['table_name']

    return event


def parse_list_of_json_and_concat(event, field_name, keep_original, field_to_keep):
    """ Iterates through a dictionary and creates a single field with a list of values from the field Output is similar to group_concat and listagg in SQL

    :param event: A dictionary
    :param field_name: The name of the field to extract data from
    :param keep_original: True to keep the original field.  False to delete the original field and only keep the parsed data.
    :param field_to_keep: The name of the field from within the dictionary
    :return: An altered dictionary

    Examples:

    .. code-block:: python

        # Example #1
        event = {'list_of_dicts': [{'key_to_concat': 123, 'key_to_ignore': 'abc'},
                                    {'key_to_concat': 456, 'key_to_ignore': 'def'},
                                    {'key_to_concat': 789, 'key_to_ignore': 'ghi'}]}
        event =  parse_list_of_json_and_concat(input_event, field_name='list_of_dicts', keep_original=True, field_to_keep='key_to_concat')
        event = {'list_of_dicts': [{'key_to_concat': 123, 'key_to_ignore': 'abc'},
                                    {'key_to_concat': 456, 'key_to_ignore': 'def'},
                                    {'key_to_concat': 789, 'key_to_ignore': 'ghi'}],
                'list_of_dicts_key_to_concats': [123, 456, 789]}

    """

    if field_name in event:
        temp = []
        for element in event[field_name]:
            for k, v in element.items():
                if k == field_to_keep:
                    field_name_underscore = field_name + '_'
                    if type(v) is dict:
                        temp.append(json.dumps(v))
                    else:
                        temp.append(v)

                    event[field_name_underscore + k + 's'] = temp

        if keep_original is False:
            del event[field_name]
    return event


def remove_duplicate_field(event, field_to_keep, field_to_discard):
    """ Remove a field when both fields are present

    :param event:  A dictionary
    :param field_to_keep: The field to keep if both keys are present and the value is not None
    :param field_to_discard: The field to discard if the field_to_keep is not None
    :return: An event with a single bundle ID

    Examples:

    .. code-block:: python

        # Example #1
        event = {'A_Field': 'another_value', 'a_field': 'a_value '}
        event = remove_duplicate_field(event, field_to_keep='a_field', field_to_discard='A_Field')
        event = {'a_field': 'a_value '}

    """

    if field_to_keep in event and field_to_discard in event:
        if event[field_to_keep] is not None:
            del event[field_to_discard]
        else:
            del event[field_to_keep]

    return event


def remove_outer_key(event, key_name):
    """ Removes the outer key from an event

    :param event: A dict with the entire event
    :param key_name: The key to remove from the dictionary
    :return: An event with the outer key for the specified dictionary removed

    Examples:

    .. code-block:: python

        # Example #1
        event = {'outer_dict': {'a_field': 'a_value ',
                                'another_field': 'another_value'}}
        event = remove_outer_key(event, key_name='outer_dict')
        event = {'a_field': 'a_value ',
                'another_field': 'another_value'}

    """

    # Removes the metrics key so we don't have every field prefixed with metrics_
    # if key_name in event and event[key_name] is dict:
    if key_name in event and isinstance(event[key_name], dict):
        event.update(event[key_name])
        del event[key_name]

    return event


def remove_starting_characters_from_keys(event, starting_characters, field_with_json=None):
    """ Removes the specified starting characters from all keys in an event

    :param event: A dict with the entire event
    :param starting_characters: The characters to remove from the beginning of the key
    :param field_with_json: A specific field with nested json from which to remove the characters from its keys
    :return: a modified event

    Examples:

    .. code-block:: python

        # Example #1
        event = {'_metadata': {},
                '$a_field': 'a_value',
                '$another_field': 'another_value'}
        event = remove_starting_characters_from_keys(event, starting_characters='$')
        event = {'_metadata': {},
                'another_field': 'another_value',
                'field': 'a_value'}

        # Example #2
        event = {'_metadata': {},
                'a_dict': {'$a_field': 'a_value',
                            '$another_field': 'another_value'},
                '$outer_field': 'some value'}
        event = remove_starting_characters_from_keys(event, starting_characters='$', field_with_json='a_dict')
        event = {'$outer_field': 'some value',
                '_metadata': {},
                'a_dict': {'a_field': 'a_value',
                            'another_field': 'another_value'}}

    """

    starting_character_length = len(starting_characters)

    if field_with_json is None:
        new_event = {}

        for k, v in event.items():
            if k.startswith(starting_characters):
                new_event[k[starting_character_length:]] = v
            else:
                new_event[k] = v

        new_event['_metadata'] = deepcopy(event['_metadata'])
        return new_event

    elif field_with_json is not None:
        new_dict = {}

        if field_with_json in event:
            for k, v in event[field_with_json].items():
                if k.startswith(starting_characters):
                    new_dict[k[starting_character_length:]] = v
                else:
                    new_dict[k] = v

            event[field_with_json] = new_dict
        return event


def remove_whitespace(event, field_or_field_list):
    """ Remove leading and trailing whitespace

    :param event: A dictionary
    :param field_or_field_list: A field or list of fields to trim the whitespace from
    :return: A trimmed string

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': '  should not have whitespace at ends    '}
        event = remove_whitespace(event, field_or_field_list='a_field')
        event = {'a_field': 'should not have whitespace at ends'}

        # Example #2
        event = {'a_field': '  should not have whitespace at ends    ',
                'another_field': '  also should not have whitespace at ends    '}
        event = remove_whitespace(event, field_or_field_list=['a_field', 'another_field'])
        event = {'a_field': 'should not have whitespace at ends',
                'another_field': 'also should not have whitespace at ends'}


    """

    if type(field_or_field_list) is not list:
        field_or_field_list = [field_or_field_list]

    for field in field_or_field_list:
        if field in event and isinstance(event[field], str):
            event[field] = event[field].strip()

    return event


def rename_fields(event, field_dict):
    """ Renames fields from the key to value
    :param event: A dict with the entire event
    :param field_dict: A dict with the rename mapping with the key as the existing field and the value as the new field
    :return: An altered event with the renamed fields

    Examples:

    .. code-block:: python

        # Example #1
        event = {'a_field': 'a_value',
                'another_field': 'another_value',
                'no_change': 'same'}
        event = rename_fields(event, field_dict={'a_field': 'field_one', 'another_field': 'field_two'})
        event = {'field_one': 'a_value',
                'field_two': 'another_value',
                'no_change': 'same'}

    """

    new_event = {}

    for k, v in event.items():
        if k in field_dict:
            if field_dict[k] not in new_event:
                new_event[field_dict[k]] = event[k]
            else:
                raise Exception('Key {key_name} already in event'.format(key_name=field_dict[k]))
        else:
            new_event[k] = event[k]

    if '_metadata' in event:
        new_event['_metadata'] = deepcopy(event['_metadata'])

    return new_event


def split_event_to_multiple_events(event, table_name_list):
    """ Splits events into a list of events with a schema_name.table_name

    :param event: A dict with a single event
    :param table_name_list: The table names for the new events
    :return: A list of the new events.  If an event has already been split it will not re-split and returns the original event.

    Examples:

    .. code-block:: python

        # Example #1
        event = {'_metadata': {'@uuid': '123-abc', 'event_type':
                                'my_schema.my_table'},
                'a_field': 'a_value'}
        event = split_event_to_multiple_events(event, table_name_list=['table_one', 'table_two'])
        # A parent UUID is added in Alooma when events are split.  Local testing won't add a parent UUID.
        event = [{'_metadata': {'@parent_uuid': '123-abc',
                                '@uuid': '456-def',
                                'event_type': 'my_schema.table_one'},
                'a_field': 'a_value'},
                {'_metadata': {'@uuid': '123-abc',
                                '@uuid': '789-ghi',
                                'event_type': 'my_schema.table_two'},
                'a_field': 'a_value'}]

        # Example #2
        event = {'_metadata': {'@parent_uuid': '123-abc',
                                '@uuid': '456-def',
                                'event_type': 'my_schema.table_one'},
                'a_field': 'a_value'}
        event = split_event_to_multiple_events(event, table_name_list=['table_one', 'table_two'])
        # If the event has a parent_uuid it will not be re-split
        event = {'_metadata': {'@parent_uuid': '123-abc',
                                '@uuid': '456-def',
                                'event_type': 'my_schema.table_one'},
                'a_field': 'a_value'}

    """

    # Avoids re-splitting events
    if '@parent_uuid' in event['_metadata'] and len(event['_metadata']['@parent_uuid']) > 0:
        return event

    if '.' not in event['_metadata']['event_type']:
        raise Exception('Only fully qualified events can be split. Event type must be schema_name.table_name')

    event_list = []

    for table_name in table_name_list:
        new_event = {}

        for k, v in event.items():
            if k != "_metatdata":
                new_event[k] = v

        new_event['_metadata'] = deepcopy(event['_metadata'])
        new_event['_metadata']['event_type'] = event['_metadata']['event_type'].split('.')[0] + '.' + table_name
        event_list.append(new_event)

    return event_list


def split_field_list_to_multiple_events(event, fields_to_split, add_counter, counter_name, reverse=False):
    """ Take an event that has columns that are lists (of same length) and break into multiple rows

    :param event: A dictionary
    :param fields_to_split: The field with to split
    :param add_counter: True to add a counter field to the event
    :param counter_name: The name of the counter field
    :param reverse: True to start the counter in reverse
    :return: A list of events

    Examples:

    .. code-block:: python

        # Example #1
        event = {'id': 1,
                'names': ['first', 'second'],
                '_metadata': {'uuid': '1a'}}
        event =  split_field_list_to_multiple_events(event=input, fields_to_split=['names'], add_counter=True, counter_name='counter', reverse=False)
        event = [{'id': 1,
                   'name': 'first',
                   'counter': 1,
                   '_metadata': {'@parent_uuid': '1a',
                                '@uuid': '456-def'}},
                  {'id': 1,
                   'name': 'second',
                   'counter': 2,
                   '_metadata': {'@parent_uuid': '1a',
                                '@uuid': '789-ghi'}}]

    """

    # Avoids re-splitting events
    if '@parent_uuid' in event['_metadata'] and len(event['_metadata']['@parent_uuid']) > 0:
        return event

    event_list = []
    number_events = len(event[fields_to_split[0]])
    for i in range(number_events):
        new_event = {}
        for k, v in event.items():
            if k in fields_to_split:
                if reverse:
                    v = v[::-1]
                if i + 1 > len(v):
                    new_event[convert_string_to_snake_case(k[:-1])] = None
                else:
                    new_event[convert_string_to_snake_case(k[:-1])] = v[i]
            elif k != "_metadata":
                new_event[convert_string_to_snake_case(k)] = v

        new_event['_metadata'] = deepcopy(event['_metadata'])
        if add_counter:
            new_event[counter_name] = i + 1
        event_list.append(new_event)

    return event_list


def whitelist_or_blacklist_columns(event, field_list, white_or_black_list='whitelist'):
    """ Allows you to remove a list of fields (blacklist) or limit an event to a list of fields (whitelist)

    :param event: A dictionary
    :param field_list: A list of fields to keep or remove
    :param white_or_black_list: whitelist = Only let a particular list of columns through the event and remove other columns. blacklist = Don't allow a particular list of columns through. Leave all other columns
    :return: An altered dictionary

    Examples:

    .. code-block:: python

        # Example #1
        event = {'_metadata': {},
                'keep_me': 'i stay',
                'keep_me_too': 'i stay too',
                'remove_me': 'im gone'}
        event = whitelist_or_blacklist_columns(event, field_list=['keep_me', 'keep_me_too'], white_or_black_list='whitelist')
        event = {'_metadata': {},
                'keep_me': 'i stay',
                'keep_me_too': 'i stay too'}

        # Example #2
        event = {'_metadata': {},
                'keep_me': 'i stay',
                'keep_me_too': 'i stay too',
                'remove_me': 'im gone'}
        event = whitelist_or_blacklist_columns(event, field_list=['remove_me'], white_or_black_list='blacklist')
        event = {'_metadata': {},
                'keep_me': 'i stay',
                'keep_me_too': 'i stay too'}

    """

    field_list = [f.lower() for f in field_list]

    new_event = {}

    if white_or_black_list == 'whitelist':
        for k, v in event.items():
            if k != "_metadata" and k.lower() in field_list:
                new_event[k] = v

    elif white_or_black_list == 'blacklist':
        for k, v in event.items():
            if k != "_metadata" and k.lower() not in field_list:
                new_event[k] = v

    new_event['_metadata'] = deepcopy(event['_metadata'])

    return new_event
