import pprint
import json
import requests
import copy
import pandas as pd
from tabulate import tabulate


from .dictionary_difference import DictionaryDifferences


class Inputs:

    def __init__(self, api, preview_full=True, preview_changes=True, apply_changes=False, pprint_indent=2, pprint_width=250, pprint_depth=5):
        """View, created and edit Alooma inputs. Inputs are the source of data to bring into Alooma.
        The class is initiated with the following variables:

        :param api: The Alooma API client authentication
        :param preview_full: Prints the input and changed input if True
        :param preview_changes: Prints the changes in the input by category if True
        :param apply_changes: Executes the mapping changes if True
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        :param pprint_depth: The depth value to pprint dictionaries
        """

        self.api = api
        self.preview_full = preview_full
        self.preview_changes = preview_changes
        self.apply_changes = apply_changes
        self.pprint_indent = pprint_indent
        self.pprint_width = pprint_width
        self.pprint_depth = pprint_depth

    @staticmethod
    def print_sorted_list(lst):
        """
        :param lst: list Takes a list and prints a sorted list
        """
        print('\n'.join(sorted(lst)))

    def get_all_inputs(self):
        """ Gets the information for all inputs from Alooma

        :return: A list of dictionaries with information for each input
        """
        return self.api.get_inputs()

    def get_input(self, input_name):
        """ Gets the input information for a specific input

        :param input_name: The name of the input to retrieve
        :return: A dictionary with the input
        """
        input_list = self.get_all_inputs()
        single_input = [i for i in input_list if input_name == i['name']][0]

        return single_input

    def view_inputs(self, single_input=None, print_format='table'):
        """ Prints a data from with the event info

        :param single_input: string The name of a specific input to filter the results
        :param print_format: string 'table' to print event info as tables or 'json' to print as dictionaries
        :return: The list of input dictionaries
        """

        inputs = self.get_all_inputs()

        if single_input:
            inputs = [i for i in inputs if i["name"] == single_input]

        if print_format == 'table':
            df = pd.DataFrame(inputs)
            df = df.reindex(['category', 'name', 'type', 'deleted', 'paused', 'stats', 'state', 'id', 'configuration'], axis=1)
            df.sort_values(by=['name'], ascending=True, inplace=True)
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            return df
        elif print_format == 'json':
            for i in inputs:
                pprint.pprint(i, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)
            if single_input:
                return inputs[0]
            else:
                return inputs

    # Needs tests
    def delete_input(self, input_name):
        """ Delete an input. This can not be undone!

        :param input_name: The name of the input to delete
        :return: None
        """
        input = self.get_input(input_name)

        if self.preview_full:
            print("INPUT TO DELETE")
            pprint.pprint(input, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        if self.apply_changes:
            self.api.remove_input(input['id'])
            print("INPUT DELETED", input_name)

        return None

    # Needs tests
    def pause_input(self, input_name):
        """ Pause the input from pulling data

        :param input_name: The name of the input to pause
        :return: None
        """

        input = self.get_input(input_name)

        params = {"pause": 'true'}
        url = self.api.rest_url + "inputs/{input_id}/pause".format(input['id'])

        res = self.api._Client__send_request(requests.put, url, params=params)
        print("Paused Input:", input_name, res)

        return None

    # Needs tests
    def resume_input(self, input_name):
        """ Resume the input so it will pull date

        :param input_name: The name of the input to resume pulling data
        :return: None
        """

        input = self.get_input(input_name)
        params = {"pause": 'false'}
        url = self.api.rest_url + "inputs/{input_id}/pause".format(input['id'])
        res = self.api._Client__send_request(requests.put, url, params=params)
        print("Resumed Input:", input_name, res)

        return None

    def list_inputs(self, add_quotes_commas=False):
        """ Prints and/or returns a list of input names

        :param print_lst: boolean True to print the list to the console
        :param add_quotes_commas: boolean True to print the list to the console with single quotes around strings and commas between each name
        :return: list of the names of inputs
        """

        inputs = self.get_all_inputs()
        input_name_list = [i["name"] for i in inputs]

        if self.preview_full:
            if not add_quotes_commas:
                self.print_sorted_list(input_name_list)
            else:
                input_name_list = ["'" + i + "'," for i in inputs]
                self.print_sorted_list(input_name_list)

        return input_name_list

    def list_tables(self, input_name):
        """ Prints and/or returns the list of tables in an input

        :param single_input: string The input for which to print or return the tables
        :return: The list if tables in an input
        """

        single_input = self.get_input(input_name=input_name)

        if single_input['type'] != 'ODBC':
            raise Exception('The input ' + single_input['name'] + ' is of type ' + single_input['type'] + ' and not of type ODBC')
        else:
            tables = single_input['configuration']['tables']

        tables = json.loads(tables)
        table_lst = list(tables.keys())

        if self.preview_full:
            self.print_sorted_list(table_lst)

        return table_lst

    def create_input_database(self, source_credentials, new_input_name, existing_input, tables_dict=None, auto_map=True, input_default_schema=None, replication_type='incremental_load', batch_size=100000):
        """ Create a new input with a database as the source

        :param source_credentials: The database credentials and configuration for the source
        :param new_input_name: The name of the new input
        :param existing_input: The name of the existing input from which to copy the configuration
        :param tables_dict: A dictionary containing the tables to replicate and the update indicator such as {"table_name": "xmin::text::bigint"}
        :param auto_map: True if the input should be auto-mapped
        :param input_default_schema: The default schema for the data in the target database
        :param replication_type: The type of replication to apply
        :param batch_size: The number of rows to pull in each batch
        :return: None

        Example database source credentials:

        .. code-block:: python

            {'server': 'server_name',
             'schema': 'schema_name',
             'port': 'port',
             'database': 'database',
             'db_type': 'psql',
             'user': 'username',
             'password': 'password'}

        """

        single_input = self.get_input(input_name=existing_input)

        if single_input['type'] != 'ODBC':
            raise Exception('The input ' + single_input['name'] + ' is of type ' + single_input['type'] + ' and not of type ODBC')

        new_input_config = {}

        # Source Database Information
        new_input_config['server'] = source_credentials['server']
        new_input_config['schema'] = 'public'
        new_input_config['port'] = source_credentials['port']
        new_input_config['database'] = source_credentials['database']
        new_input_config['db_type'] = source_credentials['db_type']
        new_input_config['user'] = source_credentials['user']
        new_input_config['password'] = source_credentials['password']

        # Target database and configuration information
        new_input_config['auto_map'] = auto_map
        new_input_config['batch_size'] = batch_size
        new_input_config['db_type'] = input_default_schema
        new_input_config['replication_type'] = replication_type
        new_input_config['input_default_schema'] = input_default_schema
        new_input_config['tables'] = json.dumps(tables_dict)

        if self.preview_full:
            print("EXISTING INPUT SAMPLE")
            pprint.pprint(single_input, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

            print("NEW INPUT CONFIG")
            pprint.pprint(new_input_config, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        if self.apply_changes:
            self.api.create_input({'name': new_input_name,
                                   'type': 'ODBC',
                                   'configuration': new_input_config})
            print("NEW INPUT CREATED")

        return new_input_config

    def edit_input_configuration(self, input_name=None, field_to_edit=None, new_field_value=None):
        """ Edit a single field in an input configuration at a time

        :param input_name: The name of the input to edit
        :param field_to_edit: The name of the field to edit
        :param new_field_value: The new value for the field
        :return: None
        """

        # Get the mapping and make a deep copy
        input = self.get_input(input_name=input_name)
        new_input = copy.deepcopy(input)

        if field_to_edit not in new_input['configuration']:
            raise Exception('The field ' + field_to_edit + ' is not in the input ' + input_name)

        # Adjust the copied input
        new_input['configuration'][field_to_edit] = new_field_value

        # Print and apply the input changes
        self.preview_input_changes(input=input, new_input=new_input, show_matching=False, show_changed=True, show_removed=False, show_added=False)
        self.apply_input_changes(input=new_input, print_message="CHANGED THE INPUT CONFIGURATION")

        return new_input

    def add_table_to_input(self, input_name, new_table_dict={}):
        """ Add tables to an existing input

        :param input_name: The name of the input to add tables to
        :param new_table_dict: A dictionary with the tables to add and their update field such as  {"table_name": "xmin::text::bigint"}
        :return: None
        """

        # Get the existing input and make a deep copy
        single_input = self.get_input(input_name=input_name)
        new_input = copy.deepcopy(single_input)

        # Check that the input type is ODBC
        if single_input['type'] != 'ODBC':
            raise Exception('The input ' + single_input['name'] + ' is of type ' + single_input['type'] + ' and not of type ODBC')

        # Load the existing string tables to a dictionary
        table_dict = json.loads(single_input['configuration']['tables'])

        for table in new_table_dict:
            if table in table_dict:
                raise Exception('The table ' + table + ' is already in the input ' + input_name)
            else:
                table_dict[table] = new_table_dict[table]

        new_input['configuration']['tables'] = json.dumps(table_dict)

        # Print and apply the input changes
        self.preview_input_changes(input=single_input, new_input=new_input, show_matching=False, show_changed=True, show_removed=False, show_added=False)
        self.apply_input_changes(input=new_input, print_message="ADDED TABLES TO INPUT")

        return new_input

    def change_auto_mapping_mode(self, input_name=None, new_mapping_mode=False):
        """ Edit a single field in an input configuration at a time

        :param input_name: The name of the input to alter
        :param new_mapping_mode: The new automapping mapping mode to set of True or False
        :return: None
        """

        # Get the mapping and make a deep copy
        input = self.get_input(input_name=input_name)
        new_input = copy.deepcopy(input)

        # Adjust the copied input
        new_input['configuration']['auto_map'] = new_mapping_mode

        # Print and apply the input changes
        self.preview_input_changes(input=input, new_input=new_input, show_matching=False, show_changed=True, show_removed=False, show_added=False)
        self.apply_input_changes(input=new_input, print_message="CHANGED AUTO MAPPING MODE")

        return new_input

    def add_template_to_parameter_configuration(self, input_name, add_to_parameter, template):
        """ Add a template to single parameter or a list of parameters in an input configuration

        :param input_name: The input to add template to
        :param add_to_parameter: a single parameter or a list of parameters that you want to add template to
        :param template: e.g. '%Y-%m-%d'
        :return: None
        """

        # Get the mapping and make a deep copy
        input = self.get_input(input_name=input_name)
        new_input = copy.deepcopy(input)

        if 'parameters' not in input['configuration']:
            raise Exception('The input ' + input_name + ' does not have any parameters')

        # Adjust the copied input
        for param in input['configuration']['parameters']:
            if param['parameter'] in add_to_parameter:
                param['template'] = template

        # Print and apply the input changes
        self.preview_input_changes(input=input, new_input=new_input, show_matching=False, show_changed=True, show_removed=False, show_added=False)
        self.apply_input_changes(input=new_input, print_message="ADDED TEMPLATE TO CONFIGURATION PARAMETER")

        return new_input

    def edit_parameter_configuration(self, input_name, parameter_to_edit, value_to_set, new_value):
        """ edit API parameter value, e.g. changing days past value from 100 to 10

        :param input_name: The input to make the change for
        :param parameter_to_edit: a single parameter that you want to edit
        :param value_to_set: name of the field you want to edit
        :param new_value: new value you want to set
        :return: None
        """

        # Get the mapping and make a deep copy
        input = self.get_input(input_name=input_name)
        new_input = copy.deepcopy(input)

        if 'parameters' not in input['configuration']:
            raise Exception('The input ' + input_name + ' does not have any parameters')

        # Adjust the copied input
        for param in new_input['configuration']['parameters']:
            if param['parameter'] == parameter_to_edit:
                param[value_to_set] = new_value

        # Print and apply the input changes
        self.preview_input_changes(input=input, new_input=new_input, show_matching=False, show_changed=True, show_removed=False, show_added=False)
        self.apply_input_changes(input=new_input, print_message="INPUT PARAMETER CONFIGURATION CHANGED")

        return new_input

    def preview_input_changes(self, input, new_input, show_matching, show_changed, show_removed, show_added):
        """ Takes an original mapping and altered mapping and prints various views on the changes

        :param input: A dictionary representing the current state of the mapping
        :param new_input: An altered dictionary representing the changed state of the mapping
        :param show_matching: Show the key value pairs that match between the two mappings
        :param show_changed: Show the key value pairs that have been changed between the two mappings
        :param show_removed: Show the key value pairs that were removed from the current state of the mapping
        :param show_added: Show the key value paids that were added to the changed state of the mapping
        :return: None
        """

        # Instantiate the Dictionary Difference Class
        DD = DictionaryDifferences(old_dictionary=input, new_dictionary=new_input, pprint_indent=self.pprint_indent, pprint_width=self.pprint_width, pprint_depth=self.pprint_depth)

        # Print the full before and after dictionaries
        if self.preview_full:
            DD.show_dictionary_all()

        # Print only the differences between the dictionaries
        if self.preview_changes:
            DD.show_dictionary_differences(show_matching=show_matching, show_changed=show_changed, show_removed=show_removed, show_added=show_added)

        return None

    def apply_input_changes(self, input, print_message):
        """ Apply the input changes in the Alooma API

        :param input: The new input to set
        :param print_message: A message to print after a successful change
        :return: None
        """

        if self.apply_changes:
            try:
                self.api.edit_input(input)
                print(print_message, self.input_name)
            except Exception as e:
                print(e)

        return None
