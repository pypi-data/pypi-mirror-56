class ColumnDDL:
    """
    Prints DDL for direct DB changes of data type, dropping columns, or adding columns
    """

    def __init__(self, tuple_or_tuple_list, change_type='data_type', has_log=False, case='UPPER'):
        """ Prints DDL for direct DB changes of data_type, drop, or add

        :param tuple_or_tuple_list: A single tuple or list of tuples with information about the changes to make
        :param change_type: The type of DDL to create out of data_type, add, rename, combine or drop
        :param log_table: True if the event has a log table
        :param case: UPPER or LOWER case for the DDL statements

        For a change_type of data_type or adding a column the tuple_or_tuple_list should contain the schema.table, the column name, and the column data type.

        .. code-block:: python

            ('schema_name.table_name', 'column_one', 'INT')
            or
            [('schema_name.table_name', 'column_one', 'INT'),
            ('schema_name.table_name', 'column_two', 'VARCHAR(16777216)')]

        For a change_type of dropping a column a column the tuple_or_tuple_list should contain the schema.table and the column name

        .. code-block:: python

            ('schema_name.table_name', 'column_one')
            or
            [('schema_name.table_name', 'column_one'),
            ('schema_name.table_name', 'column_two')]

        For a change_type of renaming a column a column the tuple_or_tuple_list should contain the schema.table, the current column name, and the new column name

        .. code-block:: python

            ('schema_name.table_name', 'my_bad_column', 'my_good_column', 'INT')
            or
            [('schema_name.table_name', 'my_bad_column_one', 'my_good_column_one', 'INT'),
            ('schema_name.table_name', 'my_bad_column_two', 'my_good_column_two', 'VARCHAR(16777216)')]

        For a change_type of combining columns the tuple_or_tuple_list should contain the schema.table, the current column name, the new column name, and the column data type.

        .. code-block:: python

            ('schema_name.table_name', 'my_bad_column', 'my_good_column', 'INT')
            or
            [('schema_name.table_name', 'my_bad_column_name_one', 'my_good_column_name_one', 'INTEGER'),
            ('schema_name.table_name', 'my_bad_column_name_two', 'my_good_column_name_two', 'VARCHAR(16777216)')]

        """

        self.tuple_or_tuple_list = tuple_or_tuple_list
        self.change_type = change_type
        self.has_log = has_log
        self.case = case

    def convert_tuple_to_list(self):
        """ Converts single tuples into a list of tuples so list iteration on single event changes works

        :param tuple_or_tuple_list: A tuple or a tuple list
        :return: A list of tuple
        """

        # Check if the input is a single tuple and convert to a list if needed
        if type(self.tuple_or_tuple_list) is tuple:
            column_list = []
            column_list.append(self.tuple_or_tuple_list)
        else:
            column_list = self.tuple_or_tuple_list

        return column_list

    def create_ddl_statements(self):
        """ Creates DDL statements, prints the statements, and returns the statements

        :param event_column_type_tuple: The tuple from the function specified
        :param change_type: The type of column change statements to print. Options are column, drop, combine_drop
        :param log_table: True if the columns to alter have log tables
        :return: A string with all the queries generated

        """

        # The query list returns all the queries generate and is used for testing
        query_strings = ''

        # Check if the input is a single tuple and convert to a list if needed
        column_list = self.convert_tuple_to_list()

        # Parse the tuples into pieces and print the DDL statements
        for column in column_list:
            fully_qualified_table_name_db = column[0]
            split_fully_qualified_table_name_db = fully_qualified_table_name_db.split('.')
            schema_name = split_fully_qualified_table_name_db[0]
            table_name = split_fully_qualified_table_name_db[1]

            column_name = column[1]

            if len(column) >= 3 and self.change_type in ['add', 'data_type']:
                column_data_type = column[2]

                if 'varchar' in column_data_type:
                    column_data_type_no_char_count = 'varchar'
                else:
                    column_data_type_no_char_count = column_data_type

            if len(column) == 3 and self.change_type == 'rename':
                new_column_name = column[2]

            if len(column) >= 4 and self.change_type == 'combine':
                new_column_name = column[2]
                column_data_type = column[3]

                if 'varchar' in column_data_type:
                    column_data_type_no_char_count = 'varchar'
                else:
                    column_data_type_no_char_count = column_data_type

            if self.change_type == 'data_type':
                query = self.change_column_data_type(schema_name=schema_name, table_name=table_name, column_name=column_name, new_column_type=column_data_type, new_column_type_no_count=column_data_type_no_char_count)
            if self.change_type == 'drop':
                query = self.drop_column(schema_name=schema_name, table_name=table_name, column_to_drop=column_name)
            if self.change_type == 'add':
                query = self.add_column(schema_name=schema_name, table_name=table_name, column_to_add=column_name, new_column_type=column_data_type)
            if self.change_type == 'rename':
                query = self.rename_column(schema_name=schema_name, table_name=table_name, existing_column_name=column_name, new_column_name=new_column_name)
            if self.change_type == 'combine':
                query = self.combine_columns(schema_name=schema_name, table_name=table_name, column_to_drop=column_name, column_to_keep=new_column_name, column_to_keep_type=column_data_type_no_char_count)

            if self.case == 'UPPER':
                query = query.upper()
            else:
                query = query.lower()

            print(query)

            query_strings = query_strings + query

        return query_strings

    def drop_column(self, schema_name, table_name, column_to_drop):
        """ Prints drop column statements

        :param schema_name: The name of the schema
        :param table_name: The name of the table
        :param column_to_drop: The name of the column to drop
        :return: the query

        For a change_type of dropping a column a column the tuple_or_tuple_list should contain the schema.table and the column name

        .. code-block:: python

            ('schema_name.table_name', 'column_one')
            or
            [('schema_name.table_name', 'column_one'),
            ('schema_name.table_name', 'column_two')]

        """

        if self.has_log:
            query = f"""BEGIN TRANSACTION;
                         ALTER TABLE "{schema_name}"."{table_name}"
                         DROP COLUMN "{column_to_drop}" CASCADE;

                         ALTER TABLE "{schema_name}"."{table_name}_LOG"
                         DROP COLUMN "{column_to_drop}" CASCADE ;

                        COMMIT;"""

        else:
            query = f"""BEGIN TRANSACTION;
                         ALTER TABLE "{schema_name}"."{table_name}"
                         DROP COLUMN "{column_to_drop}" CASCADE;

                        COMMIT;"""

        return query

    def add_column(self, schema_name, table_name, column_to_add, new_column_type):
        """ Prints add column statements

        :param schema_name: The name of the schema
        :param table_name: The name of the table
        :param column_to_add: The name of the column to add
        :return: The query

        For a change_type of data_type or adding a column the tuple_or_tuple_list should contain the schema.table, the column name, and the column data type.

        .. code-block:: python

            ('schema_name.table_name', 'column_one', 'INT')
            or
            [('schema_name.table_name', 'column_one', 'INT'),
            ('schema_name.table_name', 'column_two', 'VARCHAR(16777216)')]


        """

        if self.has_log:
            query = f"""ALTER TABLE "{schema_name}"."{table_name}"
                        ADD COLUMN "{column_to_add}" {new_column_type};
                              
                        ALTER TABLE "{schema_name}"."{table_name}_LOG"
                        ADD COLUMN "{column_to_add}" {new_column_type};"""

        else:
            query = f"""ALTER TABLE "{schema_name}"."{table_name}"
                        ADD COLUMN "{column_to_add}" {new_column_type};"""

        return query

    def change_column_data_type(self, schema_name, table_name, column_name, new_column_type, new_column_type_no_count):
        """ Prints the DB DDL statement for a single column

        :param schema_name: The name of the schema
        :param table_name: The name of the table
        :param log_table: True if the table has a log table
        :return: The query

        For a change_type of data_type or adding a column the tuple_or_tuple_list should contain the schema.table, the column name, and the column data type.

        .. code-block:: python

            ('schema_name.table_name', 'column_one', 'INT')
            or
            [('schema_name.table_name', 'column_one', 'INT'),
            ('schema_name.table_name', 'column_two', 'VARCHAR(16777216)')]


        """

        if self.has_log:
            query = f"""
                     BEGIN TRANSACTION;
                         ALTER TABLE "{schema_name}"."{table_name}"
                         RENAME COLUMN "{column_name}" TO "{column_name}_TMP";

                         ALTER TABLE "{schema_name}"."{table_name}"
                           ADD COLUMN "{column_name}" {new_column_type};
                           UPDATE "{schema_name}"."{table_name}"
                           SET "{column_name}" = "{column_name}_TMP"::{new_column_type_no_count}
                           WHERE "{column_name}" IS NULL;

                         ALTER TABLE "{schema_name}"."{table_name}"
                           DROP COLUMN "{column_name}_TMP" CASCADE;

                         ALTER TABLE "{schema_name}"."{table_name}_LOG"
                         RENAME COLUMN "{column_name}" TO "{column_name}_TMP";

                          ALTER TABLE "{schema_name}"."{table_name}_LOG"
                           ADD COLUMN "{column_name}" {new_column_type};
                           UPDATE "{schema_name}"."{table_name}_LOG"
                           SET "{column_name}" = "{column_name}_TMP"::{new_column_type_no_count}
                           WHERE "{column_name}" IS NULL;

                         ALTER TABLE "{schema_name}"."{table_name}_LOG"
                           DROP COLUMN "{column_name}_TMP" CASCADE;
                     COMMIT;
                     """

        else:
            query = f"""BEGIN TRANSACTION;
                         ALTER TABLE "{schema_name}"."{table_name}"
                         RENAME COLUMN "{column_name}" TO "{column_name}_TMP";

                         ALTER TABLE "{schema_name}"."{table_name}"
                           ADD COLUMN "{column_name}" {new_column_type};
                           UPDATE "{schema_name}"."{table_name}"
                           SET "{column_name}" = "{column_name}_TMP"::{new_column_type_no_count}
                           WHERE "{column_name}" IS NULL;

                         ALTER TABLE "{schema_name}"."{table_name}"
                           DROP COLUMN "{column_name}_TMP" CASCADE;
                        COMMIT;"""
        return query

    def rename_column(self, table_name, schema_name, existing_column_name, new_column_name):
        """ Prints the DB DDL statement to rename a single column

        :param schema_name: The name of the schema
        :param table_name: The name of the table
        :param existing_column_name: The existing column name of the colum
        :param new_column_name: The new column name for the column
        :return: The query

        For a change_type of renaming a column a column the tuple_or_tuple_list should contain the schema.table, the current column name, and the new column name

        .. code-block:: python

            ('schema_name.table_name', 'my_bad_column', 'my_good_column', 'INT')
            or
            [('schema_name.table_name', 'my_bad_column_one', 'my_good_column_one', 'INT'),
            ('schema_name.table_name', 'my_bad_column_two', 'my_good_column_two', 'VARCHAR(16777216)')]

        """

        if self.has_log:
            query = f"""ALTER TABLE "{schema_name}"."{table_name}"
                         RENAME COLUMN "{existing_column_name}" TO "{new_column_name}";

                         ALTER TABLE "{schema_name}"."{table_name}_LOG"
                         RENAME COLUMN "{existing_column_name}" TO "{new_column_name}";"""

        else:
            query = f"""ALTER TABLE "{schema_name}"."{table_name}"
                         RENAME COLUMN "{existing_column_name}" TO "{new_column_name}";"""
        return query

    def combine_columns(self, schema_name, table_name, column_to_drop, column_to_keep, column_to_keep_type):
        """ Prints statement to combine data from 2 columns into a target column and drop the non-target column

        :param fully_qualified_table_name_db: The schema.table_name of the table to change
        :param column: The tuple for an individual column
        :param log_table: True if the table has a log table
        :return: The query

        For a change_type of combining columns the tuple_or_tuple_list should contain the schema.table, the current column name, the new column name, and the column data type.

        .. code-block:: python

            ('schema_name.table_name', 'my_bad_column', 'my_good_column', 'INT')
            or
            [('schema_name.table_name', 'my_bad_column_name_one', 'my_good_column_name_one', 'INTEGER'),
            ('schema_name.table_name', 'my_bad_column_name_two', 'my_good_column_name_two', 'VARCHAR(16777216)')]

        """

        if self.has_log:
            query = f"""BEGIN TRANSACTION;
                         UPDATE TABLE "{schema_name}"."{table_name}"
                           SET "{column_to_keep}" = "{column_to_drop}"::{column_to_keep_type}
                           WHERE "{column_to_keep}" IS NULL;

                         ALTER TABLE "{schema_name}"."{table_name}"
                         DROP COLUMN "{column_to_drop}" CASCADE;

                          UPDATE TABLE "{schema_name}"."{table_name}_LOG"
                           SET "{column_to_keep}" = "{column_to_drop}"::{column_to_keep_type}
                           WHERE "{column_to_keep}" IS NULL;

                         ALTER TABLE "{schema_name}"."{table_name}_LOG"
                         DROP COLUMN "{column_to_drop}" CASCADE;
                     COMMIT;
                     """

        else:
            query = f"""BEGIN TRANSACTION;
                            UPDATE TABLE "{schema_name}"."{table_name}"
                               SET "{column_to_keep}" = "{column_to_drop}"::{column_to_keep_type}
                               WHERE "{column_to_keep}" IS NULL;
    
                             ALTER TABLE "{schema_name}"."{table_name}"
                             DROP COLUMN "{column_to_drop}" CASCADE;
                        COMMIT;"""
        return query

