import os
import pprint
import json
import os.path
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
import pandas as pd
import datetime

from .events import Events
from .inputs import Inputs


class Samples:

    def __init__(self, api, sample_event_directory):
        """ For each event Alooma stores sample dictionaries. This class will help you interact and copy the samples for testing. We run integration testing on the entirety of the sample set before deploying.

        :param api: The Alooma API client authentication
        :param sample_event_directory: The full path and name of the directory in which to store sample events such as /Users/myname/code/hover/alooma-etl/sample_events
        """
        self.api = api
        self.sample_event_directory = sample_event_directory

    def build_sample_file_path_and_file_name(self, sample_file_type='event', name=None):
        """ Constructs the file path and name for writing the samples

        :param sample_file_type: The type of file either 'event' or 'input'
        :param name: The name of the event or input
        :return: a file path with the file name
        """

        file_name = sample_file_type + '_' + name.replace('.', '_').lower() + '.json'
        file_path = os.path.join(self.sample_event_directory, file_name)

        return file_path

    @staticmethod
    def print_samples(sample_list, view_all_or_index='all', pprint_indent=2, pprint_width=200, pprint_depth=5):
        """ Prints all the samples in a list or pretty prints a single sample

        :param sample_list: A list of samples
        :param view_all_or_index: 'all' to print all samples or a number to print sample by index
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        :param pprint_depth: The depth value to pprint dictionaries
        :return: None
        """

        if view_all_or_index == 'all':
            for idx, val in enumerate(sample_list):
                print(idx, val)
        else:
            pprint.pprint(sample_list[int(view_all_or_index)], indent=pprint_indent, width=pprint_width, depth=pprint_depth)

    def get_samples_for_event_from_alooma_api(self, event_name):
        """ Gets samples for a single event from the API

        :param event_name: The event for which to get samples
        :return: A list of samples
        """

        sample_list = self.api.get_samples(event_type=event_name)
        return sample_list

    def view_samples_for_event_from_alooma_api(self, event_name, view_all_or_index='all'):
        """ View samples for an event from the API. Print all or a single event by index.

        :param event_name: The name of the event for which to view samples
        :param view_all_or_index: Specify to view 'all' the samples for an event or a specific event by index number
        """
        samples = self.get_samples_for_event_from_alooma_api(event_name=event_name)
        self.print_samples(samples, view_all_or_index)

        return samples

    @staticmethod
    def get_samples_from_file(file_path):
        """

        :return:
        """
        with open(file_path, 'r') as outfile:
            sample_list = json.loads(outfile.read())

        return sample_list

    def get_samples_from_saved_sample_files(self, sample_file_type='event', name=None):
        """ Gets the samples for an event or input from a saved file

        :param sample_file_type: The name of the file to retrieve samples for. Exclude the .json extension
        :param name: The name of the event or input to get the samples for
        :return: A list with the samples from the file
        """

        if sample_file_type == 'event':
            file_path = self.build_sample_file_path_and_file_name(sample_file_type='event', name=name)
        elif sample_file_type == 'input':
            file_path = self.build_sample_file_path_and_file_name(sample_file_type='input', name=name)

        return self.get_samples_from_file(file_path)

    def view_samples_from_file(self, sample_file_type='event', name=None, view_all_or_index='all', pprint_indent=2, pprint_width=200, pprint_depth=5):
        """ Prints the samples for an event or input from the API

        :param sample_file_type: Whether the samples are for an 'event' or an 'input'
        :param name: The name of the event or input
        :param view_all_or_index: Specify to view 'all' the samples for an event or a specific event by index
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        :param pprint_depth: The depth value to pprint dictionaries
        :return: None
        """

        samples = self.get_samples_from_saved_sample_files(sample_file_type=sample_file_type, name=name)
        self.print_samples(samples, view_all_or_index, pprint_indent=pprint_indent, pprint_width=pprint_width, pprint_depth=pprint_depth)

        return samples

    def save_alooma_samples_to_files(self, event_name=None, input_name=None):
        """ Saves samples to files in the specified directory.
        If no event_name or input_name are specified samples for ALL events will be written to a file

        :param event_name: The event name for samples to save.  If specified only samples for this event are retrieved
        :param input_name: The input name for samples to save. If specified all samples for this input are retrieved
        :return: None
        """

        E = Events(api=self.api)
        I = Inputs(api=self.api)

        # Writes samples to a file for the event
        if event_name is not None:
            self.write_alooma_samples_to_files(event_list=[event_name], input_name=None)

        # Writes samples to a file for each event and a file with all events for the input
        elif input_name is not None:
            event_list = E.list_events(print_lst=False, input_labels=input_name)
            self.write_alooma_samples_to_files(event_list=event_list, input_name=input_name)

        # Writes samples to a file for each event and all events for an input to a file for each input
        else:
            input_list = I.list_inputs(print_lst=False)

            for input_name in input_list:
                event_list = E.list_events(print_lst=False, input_labels=input_name)
                self.write_alooma_samples_to_files(event_list=event_list, input_name=input_name)

        return None

    def write_alooma_samples_to_files(self, event_list, input_name=None):
        """ Writes samples to files for each event. Writes input file with samples for all events in the input when input_name is specified.

        :param event_list: A list of events for which to write samples for
        :param input_name: The name of the input to write the samples for to limit the samples to a specific input
        :return: None
        """

        sample_lst = []

        for event in event_list:
            event_file_path = self.build_sample_file_path_and_file_name(sample_file_type='event', name=event)

            print("GETTING & WRITING SAMPLES FOR:", event)

            samples = self.get_samples_for_event_from_alooma_api(event)

            with open(event_file_path, 'w') as outfile:
                json.dump(samples, outfile)

            sample_lst = sample_lst + samples

        if input_name is not None:
            print("WRITING INPUT SAMPLES FOR:", input_name)
            print("INPUT SAMPLE COUNT:", len(sample_lst))
            input_file_path = self.build_sample_file_path_and_file_name(sample_file_type='input', name=input_name)

            with open(input_file_path, 'w') as outfile:
                json.dump(sample_lst, outfile)

        return None

    @staticmethod
    def get_sample_from_any_api(url, payload, api_key, input_label, print_api_response=True, test_index_number=0, input_type='rest_endpoint'):
        """ Gets a sample to test from a 3rd party API using the requests package and adds the required Alooma _metadata to the event

        :param url: The URL for which to make the get request e.g. https://harvest.greenhouse.io/v1/scheduled_interviews
        :param payload: A JSON dictionary with the parameters to add to the requests e.g. {'updated_after': '2018-08-25T00:00:00Z'}
        :param api_key: The API key with which to make the request
        :param preview_events: If True all the events retrieved will be printed to the console
        :param input_label: The input_label to give these events when deployed in Alooma
        :param test_index_number: The index number of the event to test
        :param input_type: The type of input the data will use when deployed to Alooma
        :return: An event with metadata added that can be tested through the transformation code
        """

        try:
            response = requests.get(url, auth=HTTPBasicAuth(api_key, api_key), params=payload, timeout=3)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            raise Exception('Http Error: %s' % errh)
        except requests.exceptions.ConnectionError as errc:
            raise Exception('Error Connecting:' % errc)
        except requests.exceptions.Timeout as errt:
            raise Exception('Timeout Error: %s' % errt)
        except requests.exceptions.RequestException as err:
            raise Exception('Timeout Error: %s' % err)

        events = response.json()

        if print_api_response:
            for event in events:
                print(event)

        event = events[test_index_number]
        event['_metadata'] = {'input_label': input_label, 'input_type': input_type}

        return event

    @staticmethod
    def get_sample_from_postgresql_database(db_host, db_port, db_user, db_password, db_name, input_label, table_name, id_field, row_id, print_event=True):

        db_settings = {
            'drivername': 'postgres',
            'host': db_host,
            'port': db_port,
            'username': db_user,
            'password': db_password,
            'database': db_name
        }

        # Adds quotes to the ID field if it's a string
        if isinstance(row_id, str):
            row_id = "\'" + row_id + "\'"

        # Creates the query, gets a row from PostgreSQL,  and adds the Alooma _metadata needed to go through the code
        engine = create_engine(URL(**db_settings))
        sql = "SELECT * FROM {table_name} WHERE {id_field} = {row_id};".format(table_name=table_name, id_field=id_field, row_id=row_id)
        df = pd.read_sql(sql, engine)
        event = df.to_dict(orient='records')[0]
        event['_metadata'] = {'input_label': input_label, 'table': table_name, 'event_type': table_name, 'input_type': 'odbc_psql_incremental_load'}

        # Turn timestamp into a string so testing in the API will work
        for k, v in event.items():
            if isinstance(v, datetime.datetime):
               event[k] = v.strftime('%Y-%m-%d %H:%M:%S.%f')

        if print_event:
            pprint.pprint(event, indent=2, width=200)

        return event
