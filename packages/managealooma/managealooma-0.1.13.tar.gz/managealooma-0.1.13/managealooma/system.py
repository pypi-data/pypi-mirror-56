import pandas as pd
from tabulate import tabulate
import pprint


class System:

    def __init__(self, api):
        """ Gets information on system information like notifications, status codes, and metrics
        :param api: api authentication using the Alooma package
        """
        self.api = api

    def get_status_codes(self):
        """ Gets the possible status codes from Alooma

        :return: A dictionary with status codes and their descriptions
        """
        return self.api.get_samples_status_codes()

    def status_code_info(self, print_format='table', table_limit=None, pprint_indent=2, pprint_width=20, pprint_depth=5):
        """ Prints the status codes that Alooma may return from with the event info

        :param print_format: string 'table' to print event info as tables or 'json' to print as dictionaries
        :param table_limit: A limit to the columns to print
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        :param pprint_depth: The depth value to pprint dictionaries
        :return: A dictionary with the status codes and their descriptions

        """

        status_codes = self.get_status_codes()

        if print_format == 'table':
            df = pd.Series(status_codes).reset_index()
            df.columns = ['Status Code', 'Status Description']
            print (tabulate(df.head(n=table_limit), headers='keys', tablefmt='psql', showindex=True))
        elif print_format == 'json':
            pprint.pprint(status_codes, indent=pprint_indent, width=pprint_width, depth=pprint_depth)

        return status_codes

    def system_metric_info(self, metric_type_names=None, last_n_minutes=60):
        """ Gets the system metrics and prints a dataframe with the results

        :param metric_type_names: string or list A list of systems metrics or a single metric name.
        :param last_n_minutes: The length of time in minutes counting back from the current time to retrieve notifications for
        :return: A dataframe with the inforamtion
        """

        metric_names = ['EVENTS_IN_PIPELINE',
                        'UNMAPPED_EVENTS',
                        'IGNORED_EVENTS',
                        'ERROR_EVENTS',
                        'LOADED_EVENTS_RATE']

        if not metric_type_names:
            metric_type_names = metric_names

        system_metrics = self.api.get_metrics_by_names(metric_names=metric_type_names, minutes=last_n_minutes)

        lst = []

        for metrics in system_metrics:

            row_dict = {'target': metrics['target'],
                        'value1':  metrics['datapoints'][0][0],
                        'timestamp1': pd.to_datetime(metrics['datapoints'][0][1], unit='s'),
                        'value2': metrics['datapoints'][1][0],
                        'timestamp2': pd.to_datetime(metrics['datapoints'][1][1], unit='s')}

            lst.append(row_dict)

        df = pd.DataFrame(lst)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=True))

        return df

