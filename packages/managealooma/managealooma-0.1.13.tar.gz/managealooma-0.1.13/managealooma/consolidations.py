import pprint
import requests
import pandas as pd
from tabulate import tabulate
from collections import OrderedDict
import copy


class Consolidations:

    def __init__(self, api, preview_changes=True, apply_changes=False, pprint_indent=2, pprint_width=250, pprint_depth=5):
        """Consolidations are Alooma's way of making sure only the most recent row for each table appears in the main table.
         Consolidation management the v2 API.  The class is initiated with the following variables:

        :param api: The Alooma API client authentication
        :param preview_changes: Prints the consolidation or consolidations changes if True
        :param apply_changes: Executes the consolidation changes if True
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        :param pprint_depth: The depth value to pprint dictionaries

        """

        self.api = api
        self.preview_changes = preview_changes
        self.apply_changes = apply_changes
        self.pprint_indent = pprint_indent
        self.pprint_width = pprint_width
        self.pprint_depth = pprint_depth

    def get_scheduled_queries(self):
        """ Gets the list of scheduled queries from Alooma

        :return: The JSON response with all of the scheduled queries
        """

        # Consolidation V2
        CONSOLIDATION_V2 = 'v2/consolidation'
        CONSOLIDATION_STATE_V2 = 'v2/consolidation/{query_id}'
        CONSOLIDATION_RUN_V2 = 'v2/consolidation/{query_id}/run'

        url = self.api.rest_url + 'v2/consolidation'
        res = self.api._Client__send_request(requests.get, url)

        return res.json()

    def scheduled_query_table(self):
        """ Retrieves a list of the consolidation queries running in Alooma. Prints the information in a dataframe if the class preview_changes flag is True.

        :return: A dataframe with the information on the scheduled queries
        """
        scheduled_queries = self.get_scheduled_queries()

        orderedDictList = []
        for query in scheduled_queries:

            orderedDictList.append(OrderedDict([('id', query['id']),
                                                ('event_name', query['event_type']),
                                                ('error_message', query['error_message']),
                                                ('is_active', query['is_active']),
                                                ('is_running', query['is_running']),
                                                ('schedule', query['schedule']),
                                                ('last_success_time', query['last_success_time']),
                                                ('last_run_start_time', query['last_run_start_time']),
                                                ('last_run_end_time', query['last_run_end_time']),
                                                ('last_run_return_code', query['last_run_return_code']),
                                                ('start_time', query['start_time']),
                                                ('next_run_time', query['next_run_time']),
                                                ('generated_by', query['generated_by']),
                                                ('query_type', query['query_type']),
                                                ('service_type', query['service_type']),
                                                ('time_limit', query['time_limit']),
                                                ('name', query['name']),
                                                ('service_type', query['service_type']),
                                                ('enqueue_time', query['enqueue_time']),
                                                ('docker_tag', query['docker_tag']),
                                                ('docker_img', query['docker_img']),
                                                ('docker_cmd', query['docker_cmd'])
                                               ]))

        df = pd.DataFrame(orderedDictList).sort_values('event_name')

        if self.preview_changes:
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

        return df

    def create_consolidation(self, event_name, cron_schedule='*/15 * * * *', custom_variables=False):
        """ Create Consolidation Given Configuration

            :param event_name: The event type for which to create the consolidation
            :param cron_schedule: The cron schedule on which to run the schedule query. Default is 15 minutes.
            :param custom_variables: custom variables to add to consolidation. For consolidations from database tables set custom variables to None. For consolidations for all other tables the recommended customer variable settings are custom_variables = {"all_ri_fields": ["_metadata.@timestamp"], "ri_field": "_metadata.@timestamp", "ri_column": "_metadata.@timestamp"}

        """

        configuration = {
            "event_type": event_name,
            "run_at": cron_schedule,
            "query_type": 'incremental'
        }

        # For non-database tables use the metadata fields for custom variables
        if custom_variables:
            configuration["custom_variables"] = {"all_ri_fields": ["_metadata.@timestamp"], "ri_field": "_metadata.@timestamp", "ri_column": "_metadata.@timestamp"}

        if "deployment_name" not in configuration:
            deployment_name = self.api.get_deployment_info()['deploymentName']
            configuration["deployment_name"] = deployment_name

        if self.preview_changes:
            pprint.pprint(configuration, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        if self.apply_changes:
            url = self.api.rest_url + 'v2/consolidation'
            res = self.api._Client__send_request(requests.post, url, json=configuration)
            pprint.pprint(res.json(), indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        return configuration

    def get_scheduled_query_for_event(self, event_name):
        """ Gets the scheduled query for a specific event

        :param event_name: The name of the event for which to retrieve the schedule query
        :return: Returns the schedule query
        """

        schqueries = self.get_scheduled_queries()
        schquery = [c for c in schqueries if c['event_type'] == event_name]

        return schquery[0]

    def view_schedule_query_for_event(self, event_name, show_configuration_only=True):
        """ Prints the scheduled query for an event when

        :param event_name: The event to view a scheduled query for
        :param show_configuration_only: Print the configuration only without the query
        :return: The scheduled query
        """

        try:
            schquery = self.get_scheduled_query_for_event(event_name)
        except IndexError:
            print ("No Consolidation for", event_name)

        if self.preview_changes:
            if show_configuration_only:
                consolidation_without_details = copy.deepcopy(schquery)
                consolidation_without_details.pop('consolidation_query', None)
                pprint.pprint(consolidation_without_details, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)
            else:
                pprint.pprint(schquery, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        return schquery

    def remove_scheduled_query(self, schquery):
        """ Removes the scheduled query for a specific ID

        :param schquery: the ID of a schedule query to remove
        :return: None
        """
        url = self.api.rest_url + 'v2/consolidation/' + str(schquery['id'])

        if self.apply_changes:
            res = self.api._Client__send_request(requests.delete, url)
            print(res)

        return None

    def remove_scheduled_query_for_event(self, event_name, show_configuration_only=True):
        """ Removes the scheuled query for an event

        :param event_name: The name of the event for which to remove the consolidation
        :param print_consolidations: print the current consolidation
        :param show_configuration_only: Print the configuration only without the query
        :param apply_change: apply the remove consolidation
        :return:
        """
        schquery = self.get_scheduled_query_for_event(event_name)

        if self.preview_changes:
            if show_configuration_only:
                consolidation_without_details = copy.deepcopy(schquery)
                consolidation_without_details.pop('consolidation_query', None)
                pprint.pprint(consolidation_without_details, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)
            else:
                pprint.pprint(schquery, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        if self.apply_changes:
            self.remove_scheduled_query(schquery)

        return None

    def change_scheduled_query_frequency_for_event(self, event_name, cron_schedule='*/15 * * * *'):
        """ Change the frequency of the scheduled query

        :param event_name: he name of the event for which to remove the consolidation
        :param cron_schedule: The new cron schedule to set for the event
        :return: None
        """

        schquery = self.get_scheduled_query_for_event(event_name)

        if self.preview_changes:
            print("OLD FREQUENCY", schquery['configuration']['run_at'])

        schquery['configuration']['run_at'] = cron_schedule

        if self.preview_changes:
            print ("NEW FREQUENCY", schquery['configuration']['run_at'])

        if self.apply_changes:
            res = self.remove_scheduled_query(schquery)
            print("REMOVING OLD QUERY", res)
            res = self.create_consolidation_v2(self.api, schquery['configuration'])
            print("RE-CREATING QUERY WITH NEW SCHEDULE", res)

        return None
