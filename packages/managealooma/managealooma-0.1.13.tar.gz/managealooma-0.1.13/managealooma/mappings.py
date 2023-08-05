import pprint
import re
import copy
import requests
from .dictionary_difference import DictionaryDifferences


class Mappings:

    def __init__(
            self, api, event_name, preview_full=True, preview_changes=True,
            apply_changes=False, pprint_indent=2, pprint_width=250,
            pprint_depth=5):
        """View and change Alooma mappings. Mappings are the conversion of a dictionary to a flattened table structure.
        The class is initiated with the following variables:

        :param api: The Alooma API client authentication
        :param event_name: The name of the event to view or change settings for
        :param preview_full: Prints the mapping or mapping changes if True. The default is True.
        :param preview_changes: Prints the changes in the mapping by category if True
        :param apply_changes: Executes the mapping changes if True
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        :param pprint_depth: The depth value to pprint dictionaries

        """
        self.api = api
        self.event_name = event_name
        self.preview_full = preview_full
        self.preview_changes = preview_changes
        self.apply_changes = apply_changes
        self.pprint_indent = pprint_indent
        self.pprint_width = pprint_width
        self.pprint_depth = pprint_depth

    def get_mapping_for_event(self):
        """ Gets the mapping for the event name that the class was initialized with

        :return: a dictionary with the mapping
        """
        return self.api.get_mapping(self.event_name)

    def view_mapping(self, view_field_mappings=False):
        """ Gets the mapping for an event and allows printing with or with the field details

        :param view_field_mappings: Hides the field details when set to false. Useful for quick view of consolidation and mapping details without all the fields
        :return: Returns the mapping dictionary the user viewed

        Sample Mapping printed with view_field_mappings=False.  The mapping['fields'] key with the list of fields IS NOT printed.

        .. code-block:: python

          {'autoMappingError': None,
           'consolidation': {'consolidatedSchema': 'MY_SCHEMA',
                            'consolidatedTableName': 'MY_TABLE',
                            'consolidationKeys': ['ID'],
                            'viewSchema': None},
           'inputObjects': {'12345-asdfg': ['98765-zxcvb']},
           'mapping': {'isDiscarded': False,
                       'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
                       'outputId': 'a1s2d3-f4g5h6',
                       'readOnly': False,
                       'schema': 'MY_SCHEMA',
                       'tableName': 'MY_TABLE_LOG'},
            'mappingMode': 'AUTO_MAP',
            'name': 'MY_SCHEMA.MY_TABLE',
            'origInputLabel': 'production_database',
            'schemaUrls': ['schema?id=12345-asdfg&schema_object=my_table',
                        'schema?id=d=12345-asdfg&sschema_object=deleted_rows'],
            'state': 'MAPPED',
            'usingDefaultMappingMode': False}



        Sample Mapping printed with view_field_mappings=True. The mapping['fields'] key with the list of fields IS printed.

        .. code-block:: python

          {'autoMappingError': None,
           'consolidation': {'consolidatedSchema': 'MY_SCHEMA',
                            'consolidatedTableName': 'MY_TABLE',
                            'consolidationKeys': ['ID'],
                            'viewSchema': None},
            'fields': [ {'fieldName': 'id',
                        'fields': [],
                        'mapping': {'columnName': 'ID',
                        'columnType': {'nonNull': True,
                                        'precision': 38,
                                        'scale': 0,
                                        'type': 'NUMERIC'},
                                        'isDiscarded': False,
                                        'machineGenerated': False,
                                        'subFields': None}},
                        {'fieldName': 'name',
                        'fields': [],
                        'mapping': {'columnName': 'NAME',
                        'columnType': {'length': 16777216,
                                        'nonNull': False,
                                        'truncate': False,
                                        'type': 'VARCHAR'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}
                        ],
           'inputObjects': {'12345-asdfg': ['98765-zxcvb']},
           'mapping': {'isDiscarded': False,
                       'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
                       'outputId': 'a1s2d3-f4g5h6',
                       'readOnly': False,
                       'schema': 'MY_SCHEMA',
                       'tableName': 'MY_TABLE_LOG'},
            'mappingMode': 'AUTO_MAP',
            'name': 'MY_SCHEMA.MY_TABLE',
            'origInputLabel': 'production_database',
            'schemaUrls': ['schema?id=12345-asdfg&schema_object=my_table',
                        'schema?id=d=12345-asdfg&sschema_object=deleted_rows'],
            'state': 'MAPPED',
            'usingDefaultMappingMode': False}


        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping to remove the fields
        new_mapping.pop('fields', None)

        if self.preview_changes and not self.preview_full:
            raise Exception(
                'You must specify preview_changes=True to see the mapping. This function does not change the mapping and preview_changes is ignored')

        # Print the dictionary with or without the fields
        if view_field_mappings:
            DD = DictionaryDifferences(
                old_dictionary=mapping,
                new_dictionary=None,
                pprint_indent=self.pprint_indent,
                pprint_width=self.pprint_width,
                pprint_depth=self.pprint_depth)
            DD.show_dictionary_all()
            return mapping
        else:
            DD = DictionaryDifferences(
                old_dictionary=None,
                new_dictionary=new_mapping,
                pprint_indent=self.pprint_indent,
                pprint_width=self.pprint_width,
                pprint_depth=self.pprint_depth)
            DD.show_dictionary_all()
            return new_mapping

    def change_mapping_mode(self, new_mapping_mode='STRICT'):
        """ Change the mapping mode. Alooma has 3 modes of AUTO_MAP, STRICT, and FLEXIBLE. We only use AUTO_MAP or STRICT

        :param new_mapping_mode: The new mapping mode to set: AUTO_MAP, STRICT, and FLEXIBLE
        :return: The altered mapping

        The mapping settings keys and sample values

        .. code-block:: python

            {'autoMappingError': None,
            'mappingMode': None,
            'usingDefaultMappingMode': True}

        The mapping mode with the specified new mappingMode to alter

        .. code-block:: python

            {'autoMappingError': None,
            'mappingMode': 'AUTO_MAP',
            'usingDefaultMappingMode': True}

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        new_mapping['mappingMode'] = new_mapping_mode

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="NEW MAPPING MODE SET")

        return new_mapping

    def change_mapping_consolidation_settings(
            self, consolidation_schema, consolidation_table_name,
            consolidation_keys):
        """ Updates the consolidation information for an event

        :param consolidation_schema: The schema of consolidated table
        :param consolidation_table_name: The name of the consolidated table
        :param consolidation_keys: The consolidation keys (primary key) for the table. Takes a single field or a list
        :return: The altered mapping

        The old consolidation settings

        .. code-block:: python

            {'consolidatedSchema': 'MY_SCHEMA_TEMP',
            'consolidatedTableName': 'NY_TABLE_ITEMS',
            'consolidationKeys': ['IDENTIFIER'],
            'viewSchema': None}

        The new consolidation settings to apply

        .. code-block:: python

            {'consolidatedSchema': 'MY_SCHEMA',
            'consolidatedTableName': 'MY_TABLE',
            'consolidationKeys': ['ID'],
            'viewSchema': None}

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        if not isinstance(consolidation_keys, list):
            key_list = []
            key_list.append(consolidation_keys)

        new_mapping['consolidation']['consolidatedSchema'] = consolidation_schema
        new_mapping['consolidation']['consolidatedTableName'] = consolidation_table_name
        new_mapping['consolidation']['consolidationKeys'] = key_list

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="UPDATED CONSOLIDATION")

        return new_mapping

    def change_mapping_consolidation_key(self, new_consolidation_key):
        """ Change the conolidation key only

        :param new_consolidation_key: The new consolidation key. This is the primary key for the table.
        :return: The altered mapping

        The consolidation key is set to the field name ID when tables are auto-mapped

        .. code-block:: python

            {'consolidatedSchema': 'MY_SCHEMA',
            'consolidatedTableName': 'MY_TABLE',
            'consolidationKeys': ['ID'],
            'viewSchema': None}

        This example will change the key to a field named IDENTIFIER

        .. code-block:: python

            {'consolidatedSchema': 'MY_SCHEMA',
            'consolidatedTableName': 'MY_TABLE',
            'consolidationKeys': ['IDENTIFIER'],
            'viewSchema': None}
        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        new_mapping['consolidation']['consolidationKeys'] = new_consolidation_key

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="CONSOLIDATION KEY SET")

        return new_mapping

    def change_mapping_to_use_log(self):
        """ Changes the mapping from using the consolidated table to the log table. Used when adjusting manual mappings

        :param event_name: The event name of the mapping to alter
        :return: The altered mapping

        Events without a _log do not have consolidated table information

        .. code-block:: python

             'mapping': {'isDiscarded': False,
              'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
              'outputId': 'a1s2d3-f4g5h6',
              'readOnly': False,
              'schema': 'MY_SCHEMA',
              'tableName': 'MY_TABLE'}

        This example will change the key to a field named IDENTIFIER

        .. code-block:: python

            'mapping': {'isDiscarded': False,
              'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
              'outputId': 'a1s2d3-f4g5h6',
              'readOnly': False,
              'schema': 'MY_SCHEMA',
              'tableName': 'MY_TABLE_LOG'}

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        table_name_with_log = mapping['mapping']['tableName'] + '_LOG'
        new_mapping['mapping']['tableName'] = table_name_with_log

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="LOG TABLE SET")

        return new_mapping

    def change_mapping_for_manual_consolidation_creation(
            self, consolidation_schema, consolidation_table_name,
            consolidation_keys, case='UPPER'):
        """ Updates the mapping after creating the log table manually

        :param consolidation_schema: The schema of consolidated table
        :param consolidation_table_name: The name of the consolidated table
        :param consolidation_keys: The consolidation keys (primary key) for the table. Takes a single field or a list
        :param case: UPPER if your events are MY_SCHEMA.MY_EVENT and LOWER if the events are my_schema_my_event
        :return: The altered mapping

        First adjust the tables in the data warehouse.

        .. code-block:: python

            ALTER TABLE MY_TABLE RENAME TO MY_TABLE_LOG;
            CREATE TABLE MY_TABLE LIKE MY_TABLE_LOG;

        Then run change_mapping_for_manual_consolidation_creation  to change the mapping to insert data into the new log table. This is the old mapping:

        .. code-block:: python

            'consolidation': {'consolidatedSchema': None,
                            'consolidatedTableName': None,
                            'consolidationKeys': ,
                            'viewSchema': None},
           'mapping': {'isDiscarded': False,
                       'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
                       'outputId': 'a1s2d3-f4g5h6',
                       'readOnly': False,
                       'schema': 'MY_SCHEMA',
                       'tableName': 'MY_TABLE'},

        These are the changes that will be applied with the new mapping

        .. code-block:: python

            'consolidation': {'consolidatedSchema': 'MY_SCHEMA',
                            'consolidatedTableName': 'MY_TABLE',
                            'consolidationKeys': ['ID_FIELD'],
                            'viewSchema': None},
           'mapping': {'isDiscarded': False,
                       'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
                       'outputId': 'a1s2d3-f4g5h6',
                       'readOnly': False,
                       'schema': 'MY_SCHEMA',
                       'tableName': 'MY_TABLE_LOG'},

        Lastly add consolidation queries to combine the new data with the existing data using :func:`~managealooma.consolidations.Consolidations.create_consolidation`

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        if not isinstance(consolidation_keys, list):
            key_list = []
            key_list.append(consolidation_keys)

        # Enforce casing
        if case == 'UPPER':
            key_list = [k.upper() for k in key_list]
            consolidation_schema = consolidation_schema.upper()
            consolidation_table_name = consolidation_table_name.upper()
            mapping_table_name = mapping['mapping']['tableName'].upper(
            ) + '_LOG'
        elif case.lower() == 'lower':
            key_list = [k.lower() for k in key_list]
            consolidation_schema = consolidation_schema.lower()
            consolidation_table_name = consolidation_table_name.lower()
            mapping_table_name = mapping['mapping']['tableName'].lower(
            ) + '_log'

        # Set the new fields with the default case of UPPER
        new_mapping['consolidation']['consolidatedSchema'] = consolidation_schema.upper()
        new_mapping['consolidation']['consolidatedTableName'] = consolidation_table_name.upper()
        new_mapping['consolidation']['consolidationKeys'] = key_list
        new_mapping['mapping']['tableName'] = mapping_table_name

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="UPDATED CONSOLIDATION")

        return new_mapping

    def delete_field_from_mapping(self, field_name):
        """ Gets a mapping, deletes a field from the mapping, and resets the mapping table statistics.

        :param event_name: the name of event for which to make the change
        :param field_name: the field name that should be deleted
        :return: The altered mapping

        If print_changes is specified the details for the field to remove is printed

        .. code-block:: python

           {'fieldName': 'name',
                        'fields': [],
                        'mapping': {'columnName': 'NAME',
                        'columnType': {'length': 16777216,
                                        'nonNull': False,
                                        'truncate': False,
                                        'type': 'VARCHAR'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}



        Then the entire new mapping is printed. The 'name' field is not longer in the mapping

        .. code-block:: python

          {'autoMappingError': None,
           'consolidation': {'consolidatedSchema': 'MY_SCHEMA',
                            'consolidatedTableName': 'MY_TABLE',
                            'consolidationKeys': ['ID'],
                            'viewSchema': None},
            'fields': [ {'fieldName': 'id',
                        'fields': [],
                        'mapping': {'columnName': 'ID',
                        'columnType': {'nonNull': True,
                                        'precision': 38,
                                        'scale': 0,
                                        'type': 'NUMERIC'},
                                        'isDiscarded': False,
                                        'machineGenerated': False,
                                        'subFields': None}}
                        ]
           'inputObjects': {'12345-asdfg': ['98765-zxcvb']},
           'mapping': {'isDiscarded': False,
                       'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
                       'outputId': 'a1s2d3-f4g5h6',
                       'readOnly': False,
                       'schema': 'MY_SCHEMA',
                       'tableName': 'MY_TABLE_LOG'},
            'mappingMode': 'AUTO_MAP',
            'name': 'MY_SCHEMA.MY_TABLE',
            'origInputLabel': 'production_database',
            'schemaUrls': ['schema?id=12345-asdfg&schema_object=my_table',
                        'schema?id=d=12345-asdfg&sschema_object=deleted_rows'],
            'state': 'MAPPED',
            'usingDefaultMappingMode': False}

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        new_fields = [f for f in mapping['fields']
                      if f['fieldName'] != field_name]
        new_mapping['fields'] = new_fields

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=False,
            show_removed=True,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message=f'REMOVED FILE {field_name} FROM {self.event_name}')

        return new_mapping

    def change_field_mapping_settings(
            self, field_name, new_data_type, truncate=False, non_null=False):
        """ Updates a single filed in a mapping

        :param field_name: The field name to alter
        :param new_data_type: The new datatype for the mapping such as VARCHAR(1024) or INT
        :param truncate: Set to True if the event should be truncated when it's longer than the specific mapping length. Redshift's max VARCHAR is 65535 and Snowflake's max VARCHAR is 16777216.
        :param non_null: Set to true if the field is needs to be not null
        :return: The altered mapping

        The current mapping field settings

        .. code-block:: python

           {'fieldName': 'name',
                        'fields': [],
                        'mapping': {'columnName': 'NAME',
                        'columnType': {'INT':
                                        'nonNull': False,
                                        'truncate': False,
                                        'type': 'VARCHAR'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}

        The new mapping field settings to apply

        .. code-block:: python

           {'fieldName': 'name',
                        'fields': [],
                        'mapping': {'columnName': 'NAME',
                        'columnType': {'length': 1024,
                                        'nonNull': False,
                                        'truncate': True,
                                        'type': 'VARCHAR'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        if 'VARCHAR' in new_data_type.upper():
            new_length = re.search(r'(\d+)', new_data_type).group(0)
            new_data_type = 'VARCHAR'
        else:
            new_length = None

        # Find the field to change and change it
        for field in new_mapping['fields']:
            if field['fieldName'] == field_name:
                field['mapping']['columnType']['length'] = new_length
                field['mapping']['columnType']['type'] = new_data_type
                field['mapping']['columnType']['truncate'] = truncate
                field['mapping']['columnType']['nonNull'] = non_null

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="NEW MAPPING SET")

        return new_mapping

    def change_field_varchar_length(self, field_name, new_length):
        """ Updates only the length of a varchar for a field.

        :param field_name: The field name to alter
        :param new_length: The new length for the varchar
        :return: None

        .. code-block:: python

           {'fieldName': 'name',
                        'fields': [],
                        'mapping': {'columnName': 'NAME',
                        'columnType': {'length': 1024,
                                        'nonNull': False,
                                        'truncate': False,
                                        'type': 'VARCHAR'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}

        .. code-block:: python

           {'fieldName': 'name',
                        'fields': [],
                        'mapping': {'columnName': 'NAME',
                        'columnType': {'length': 16777216,
                                        'nonNull': False,
                                        'truncate': True,
                                        'type': 'VARCHAR'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        for field in new_mapping['fields']:
            if field['fieldName'] == field_name:
                field['mapping']['columnType']['length'] = new_length

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="CHANGED FILED")

        return new_mapping

    def change_field_null_constraint(self, field_name, nonnull=False):
        """ Removes the NULL constraint from a column

        :param field_name: The column for which to remove the constraint
        :param nonnull: The new null setting for the field
        :return: The altered mapping

        The field mapping details with the current nonnull setting

         .. code-block:: python

             {'fieldName': 'id',
             'fields': [],
             'mapping': {'columnName': 'ID',
                        'columnType': {'nonNull': True,
                                        'precision': 38,
                                        'scale': 0,
                                        'type':'NUMERIC'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}


        The field mapping details with the new nonnull setting

         .. code-block:: python

             {'fieldName': 'id',
             'fields': [],
             'mapping': {'columnName': 'ID',
                        'columnType': {'nonNull': False,
                                        'precision': 38,
                                        'scale': 0,
                                        'type':'NUMERIC'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        for f in new_mapping['fields']:
            if f['fieldName'] == field_name:
                f['mapping']['columnType']['nonNull'] = nonnull

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="ADJUSTED NULL CONSTRAINT")

        return new_mapping

    def check_if_consolidation_uses_log(self):
        """ Checks if the event uses a log table

        :param event_name: The name of the event for which to check
        :return: None

        Prints the event name, consolidation key list, the table data is inserted to, and True/False if the insert contains _LOG in the name
        event_name ['consolidation_key_list'] mapping_table_name True/False
        """

        mapping = self.get_mapping_for_event()
        uses_log = '_LOG' in mapping['mapping']['tableName'].upper()
        print(
            self.event_name,
            mapping['consolidation']['consolidationKeys'],
            mapping['mapping']['tableName'],
            uses_log)

        return uses_log

    def copy_mapping(self, new_event):
        """ Copies mapping from the event the class is instantiated with to a new event. Only the name changes

        :param new_event: The name of the event to copy to
        :param print_mapping: Prints the changes if specified
        :param apply_changes: Applies the changes if specified
        :return: The altered mapping
        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        new_mapping['name'] = new_event

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="MAPPING COPIED")

        return new_mapping

    def set_mapping_from_existing_mapping(
            self, new_event_name, new_schema, new_table, new_input_label):
        """ Takes the mapping from the event the class is instantiated with event and uses it to set a new mapping

        :param new_event_name: The event for which to set the new mapping
        :param new_schema: The schema for the new mapping
        :param new_table: The table for the new mapping
        :param new_input_label: The input label of the new mapping
        :return: The altered mapping
        """
        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        new_mapping['consolidation']['consolidatedSchema'] = new_schema
        new_mapping['consolidation']['consolidatedTableName'] = new_table

        new_mapping['mapping']['outputId'] = None
        new_mapping['mapping']['outputHint'] = None
        new_mapping['mapping']['schema'] = new_schema
        new_mapping['mapping']['tableName'] = new_table + '_LOG'

        new_mapping['name'] = new_event_name
        new_mapping['origInputLabel'] = new_input_label
        new_mapping['inputObjects'] = None
        new_mapping['schemaUrls'] = []

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=True,
            show_removed=False,
            show_added=False)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="MAPPING COPIED")

        return new_mapping

    def add_field_to_mapping(
            self, field_name, column_name, data_type, precision=38, scale=0,
            length=16777216, truncate=False, non_null=False):
        """ Adds a single field without sub-fields to the mapping. Works for Snowflake data types only.

        :param field_name: The field name to add
        :param column_name: The name of the column in the target DB
        :param data_type: The data type for the field out of NUMBER, VARIANT, BOOLEAN, VARCHAR, FLOAT, TIMESTAMP
        :param precision: The precision for numeric data
        :param scale: The scale for numeric data
        :param length: The length for a varchar
        :param truncate: Set to True if the event should be truncated when it's longer than the specific mapping length.  Redshift's max VARCHAR is 65535
        :param non_null: Set to true if the field is needs to be not null
        :return: The altered mapping

        Prints the entire existing mapping before the field is added

        .. code-block:: python

          {'autoMappingError': None,
           'consolidation': {'consolidatedSchema': 'MY_SCHEMA',
                            'consolidatedTableName': 'MY_TABLE',
                            'consolidationKeys': ['ID'],
                            'viewSchema': None},
            'fields': [ {'fieldName': 'id',
                        'fields': [],
                        'mapping': {'columnName': 'ID',
                        'columnType': {'nonNull': True,
                                        'precision': 38,
                                        'scale': 0,
                                        'type': 'NUMERIC'},
                                        'isDiscarded': False,
                                        'machineGenerated': False,
                                        'subFields': None}}
                        ]
           'inputObjects': {'12345-asdfg': ['98765-zxcvb']},
           'mapping': {'isDiscarded': False,
                       'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
                       'outputId': 'a1s2d3-f4g5h6',
                       'readOnly': False,
                       'schema': 'MY_SCHEMA',
                       'tableName': 'MY_TABLE_LOG'},
            'mappingMode': 'AUTO_MAP',
            'name': 'MY_SCHEMA.MY_TABLE',
            'origInputLabel': 'production_database',
            'schemaUrls': ['schema?id=12345-asdfg&schema_object=my_table',
                        'schema?id=d=12345-asdfg&schema_object=deleted_rows'],
            'state': 'MAPPED',
            'usingDefaultMappingMode': False}

        Then prints the entire new mapping to set after the field is added. This example adds the NAME field as a VARCHAR

        .. code-block:: python

            {'autoMappingError': None,
           'consolidation': {'consolidatedSchema': 'MY_SCHEMA',
                            'consolidatedTableName': 'MY_TABLE',
                            'consolidationKeys': ['ID'],
                            'viewSchema': None},
            'fields': [ {'fieldName': 'id',
                        'fields': [],
                        'mapping': {'columnName': 'ID',
                        'columnType': {'nonNull': True,
                                        'precision': 38,
                                        'scale': 0,
                                        'type': 'NUMERIC'},
                                        'isDiscarded': False,
                                        'machineGenerated': False,
                                        'subFields': None}},
                        {'fieldName': 'name',
                        'fields': [],
                        'mapping': {'columnName': 'NAME',
                        'columnType': {'length': 16777216,
                                        'nonNull': False,
                                        'truncate': False,
                                        'type': 'VARCHAR'},
                        'isDiscarded': False,
                        'machineGenerated': False,
                        'subFields': None}}
                        ]
           'inputObjects': {'12345-asdfg': ['98765-zxcvb']},
           'mapping': {'isDiscarded': False,
                       'outputHint': '{"table":"my_table","schema":"MY_SCHEMA"}',
                       'outputId': 'a1s2d3-f4g5h6',
                       'readOnly': False,
                       'schema': 'MY_SCHEMA',
                       'tableName': 'MY_TABLE_LOG'},
            'mappingMode': 'AUTO_MAP',
            'name': 'MY_SCHEMA.MY_TABLE',
            'origInputLabel': 'production_database',
            'schemaUrls': ['schema?id=12345-asdfg&schema_object=my_table',
                        'schema?id=d=12345-asdfg&sschema_object=deleted_rows'],
            'state': 'MAPPED',
            'usingDefaultMappingMode': False}

        """

        # Get the mapping and make a deep copy
        mapping = self.get_mapping_for_event()
        new_mapping = copy.deepcopy(mapping)

        # Adjust the copied mapping
        for field in new_mapping['fields']:
            if field_name == field['fieldName']:
                raise Exception('FIELD ALREADY IN MAPPING %s' % field_name)

        if data_type == 'NUMBER':
            new_field = {'fieldName': field_name,
                         'fields': [],
                         'mapping': {'columnName': column_name,
                                     'columnType': {'nonNull': non_null,
                                                    'precision': precision,
                                                    'scale': scale,
                                                    'type': data_type},
                                     'isDiscarded': False,
                                     'machineGenerated': False,
                                     'subFields': None}}

        elif data_type == 'VARCHAR':

            if length > 16777216:
                raise Exception(
                    'Max varchar length is 16777216. You are not allowed to set a varchar of %s' %
                    str(length))

            new_field = {'fieldName': field_name,
                         'fields': [],
                         'mapping': {'columnName': column_name,
                                     'columnType': {'length': length,
                                                    'nonNull': non_null,
                                                    'truncate': truncate,
                                                    'type': data_type},
                                     'isDiscarded': False,
                                     'machineGenerated': False,
                                     'subFields': None}}

        elif data_type == 'BOOLEAN':
            new_field = {'fieldName': field_name,
                         'fields': [],
                         'mapping': {'columnName': column_name,
                                     'columnType': {'nonNull': non_null,
                                                    'type': data_type},
                                     'isDiscarded': False,
                                     'machineGenerated': False,
                                     'subFields': None}}

        elif data_type == 'VARIANT':
            new_field = {'fieldName': field_name,
                         'fields': [],
                         'mapping': {'columnName': column_name,
                                     'columnType': {'nonNull': non_null,
                                                    'type': data_type},
                                     'isDiscarded': False,
                                     'machineGenerated': False,
                                     'subFields': None}}

        elif data_type == 'FLOAT':
            new_field = {'fieldName': field_name,
                         'fields': [],
                         'mapping': {'columnName': column_name,
                                     'columnType': {'nonNull': non_null,
                                                    'type': data_type},
                                     'isDiscarded': False,
                                     'machineGenerated': False,
                                     'subFields': None}}

        elif data_type == 'TIMESTAMP':
            new_field = {'fieldName': field_name,
                         'fields': [],
                         'mapping': {'columnName': column_name,
                                     'columnType': {'nonNull': non_null,
                                                    'type': data_type},
                                     'isDiscarded': False,
                                     'machineGenerated': False,
                                     'subFields': None}}

        else:
            raise Exception(
                'Only SNOWFlAKE data types of NUMBER, VARIANT, BOOLEAN, VARCHAR, FLOAT, TIMESTAMP are allowed')

        new_mapping['fields'].append(new_field)

        # Print and apply the mapping changes
        self._preview_mapping_changes(
            mapping=mapping,
            new_mapping=new_mapping,
            show_matching=False,
            show_changed=False,
            show_removed=False,
            show_added=True)
        self._apply_mapping_changes(
            mapping=new_mapping,
            print_message="NEW MAPPING SET")

        return new_mapping

    def _preview_mapping_changes(
            self, mapping, new_mapping, show_matching, show_changed,
            show_removed, show_added):
        """ Takes an original mapping and altered mapping and prints various views on the changes

        :param mapping: A dictionary representing the current state of the mapping
        :param new_mapping: An altered dictionary representing the changed state of the mapping
        :param show_matching: Show the key value pairs that match between the two mappings
        :param show_changed: Show the key value pairs that have been changed between the two mappings
        :param show_removed: Show the key value pairs that were removed from the current state of the mapping
        :param show_added: Show the key value pairs that were added to the changed state of the mapping
        :return: None
        """

        # Instantiate the Dictionary Difference Class
        DD = DictionaryDifferences(
            old_dictionary=mapping,
            new_dictionary=new_mapping,
            pprint_indent=self.pprint_indent,
            pprint_width=self.pprint_width,
            pprint_depth=self.pprint_depth)

        # Print the full before and after dictionaries
        if self.preview_full:
            DD.show_dictionary_all()

        # Print only the differences between the dictionaries
        if self.preview_changes:
            DD.show_dictionary_differences(
                show_matching=show_matching,
                show_changed=show_changed,
                show_removed=show_removed,
                show_added=show_added)

        return None

    def _apply_mapping_changes(self, mapping, print_message):
        """ Apply the mapping changes in the Alooma API

        :param mapping: The new mapping to set
        :param print_message: A message to print after a successful change
        :return: None
        """

        if self.apply_changes:
            try:
                self.api.set_mapping(mapping, self.event_name)
                print(print_message, self.event_name)
            except Exception as e:
                print(e)

        return None

    # Needs tests
    def remove_unmapped_fields_and_clear_table_stats(self):
        """ Remove unmapped fields from the a mapping and clear the UI stats.
        The mapper can become very slow over time and clearing the table stats periodically will help speed it back up.

        :return: none
        """

        if self.preview_full:
            print(
                "CLEAR UNMAPPED FIELDS AND RESET STATS IN UI FOR",
                self.event_name)

        if self.apply_changes:
            url = self.api.rest_url + "event-types/%s/clear-stats" % self.event_name
            response = self.api._Client__send_request(
                requests.delete, url, timeout=300)

            if response.status_code == 204:
                print(
                    "REMOVED UNMAPPED FIELDS AND RESET TABLE STATS IN UI",
                    self.event_name)
            else:
                raise Exception(
                    'Unable to clear stats for ' + self.event_name +
                    ' response code is ' + str(response.status_code))

            return response.status_code
