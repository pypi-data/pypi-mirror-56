import pandas as pd
from tabulate import tabulate
import pprint
import requests


class Events:

    def __init__(self, api):
        """ Gets information from Alooma on events and prints detailed information about events.

        :param api: api authentication using the Alooma package
        """
        self.api = api

    @staticmethod
    def print_sorted_list(lst):
        """
        :param lst: list Takes a list and prints a sorted list
        """
        print('\n'.join(sorted(lst)))

    def get_all_events(self):
        """ Gets the information for all events from Alooma

        :return: A list of dictionaries with information for each event
        """
        return self.api.get_event_types()

    def view_events(self, single_input=None, single_event=None, print_format='table', table_limit=None, pprint_indent=2, pprint_width=250, pprint_depth=5):
        """ Prints a data from with the event info

        :param single_input: The name of a specific input to filter the results
        :param single_event: The name of a specific event to filter the results
        :param print_format: Specify 'table' to print event info as tables or 'json' to print as dictionaries
        :param table_limit: Limit the number of events printed in the dataframe
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        :param pprint_depth: The depth value to pprint dictionaries
        :return: The event data in the print_format of a dataframe or a list of dictionaries
        """

        events = self.get_all_events()

        if single_event:
            events = [e for e in events if e["name"] == single_event]

        if single_input:
            events = [e for e in events if e["origInputLabel"] == single_input]

        if print_format == 'table':
            df = pd.DataFrame(events)
            df = df.reindex(['origInputLabel', 'name', 'state', 'stats', 'mappingMode', 'autoMappingError',
                                  'usingDefaultMappingMode', 'schemaUrls', 'consolidation'], axis=1)
            df.sort_values(by=['origInputLabel', 'name'], ascending=True, inplace=True)
            print(tabulate(df.head(n=table_limit), headers='keys', tablefmt='psql', showindex=False))
            return df

        elif print_format == 'json':
            for e in events:
                pprint.pprint(e, indent=pprint_indent, width=pprint_width, depth=pprint_depth)
            return events

    def list_events(self, input_labels='all', print_lst=False, add_quotes_commas=False):
        """ Prints and/or returns a list of event names

        :param input: string 'all' for all events or specify an input label for a specific events
        :param print_lst: boolean True to print the list to the console
        :param add_quotes_commas: boolean True to print the list to the console with single quotes around strings and commas after each item
        :return: list of events by name
        """
        events = self.get_all_events()

        if input_labels != 'all':
            events = [e["name"] for e in events if input_labels == e["origInputLabel"]]
        else:
            events = [e["name"] for e in events]

        if print_lst:
            if not add_quotes_commas:
                self.print_sorted_list(events)
            else:
                events = ["'" + e + "'," for e in events]
                self.print_sorted_list(events)

        return events

    def delete_event(self, event_name):
        """ Deletes an event from the mapper and prints the event_name and API response

        :param event_name: The name of the event to delete
        :return: None
        """

        res = self.api.delete_event_type(event_name)
        print("Deleted event", event_name)

        return res

