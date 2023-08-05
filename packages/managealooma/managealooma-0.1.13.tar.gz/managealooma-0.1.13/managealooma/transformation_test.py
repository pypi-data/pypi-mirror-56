import pprint
import copy
import os

from .dictionary_difference import DictionaryDifferences
from .samples import Samples


class TransformationTest:

    def __init__(self, api=None, code_package=None, preview_full_events=True, preview_difference_dicts=True, local_or_api='local', pprint_indent=2, pprint_width=250, pprint_depth=5):
        """ Tests the Alooma events

        :param api: api authentication using the Alooma package
        :param preview: True to print the transformations for visual inspection
        :param code_package: Your specific transformation code to use as a package. This is needed for local testing
        :param local_or_api: 'local' to test on local code or 'api' to test on code deployed to Alooma
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        """

        self.api = api
        self.preview_full_events = preview_full_events
        self.preview_difference_dicts = preview_difference_dicts
        self.code_package = code_package
        self.local_or_api = local_or_api
        self.pprint_indent = pprint_indent
        self.pprint_width = pprint_width
        self.pprint_depth = pprint_depth

    def test_single_event(self, sample):
        """ Tests a single event using the local code and pretty prints the before and after dictionaries to the console

        :param sample: A single sample event dictionary
        :return: The output dictionary
        """

        # Copy the original event for diffs to work
        original_event = copy.deepcopy(sample)

        # Transform the even in the API or locally
        if self.local_or_api == 'local':
            transformed_event = self.code_package.transform(sample)
        elif self.local_or_api == 'api':
            output = self.api.test_code_engine_code(sample)
            transformed_event = output['result']

        # Print the before and after full events
        if self.preview_full_events:
            print('INPUT EVENT'.center(200, '-'))
            pprint.pprint(original_event, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)
            print('\n' * 2)
            print('OUTPUT EVENT'.center(200, '-'))
            pprint.pprint(transformed_event, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)
            if self.local_or_api == 'api':
                if len(output['notifications']) > 0:
                    print('\n' * 2)
                    print('API NOTIFICATIONS'.ljust(200, '-'))
                    print(output['notifications'])

        # Print dictionaries categorizing the differences in the transformation
        if self.preview_difference_dicts:
            DD = DictionaryDifferences(old_dictionary=original_event, new_dictionary=transformed_event)
            DD.show_dictionary_differences()

        if transformed_event is not None and 'errorMessage' in transformed_event:
            self.fail(
                'Failed on event "%s"\n%s' % (
                    sample[sample],
                    transformed_event['errorMessage']))

        return transformed_event

    def loop_through_events_to_test(self, sample_event_list):
        """ Loops through the event files to test each sample

        :param sample_event_list: A list of dictionaries to test. The expected format from Alooma is a dictionary as formatted below
        :return: None

        Alooma samples are in a list of dictionaries with the sample inside of a key of sample:

        .. code-block:: python

            [{'sample': {}
            {'sample': {}
            {'sample': {}]

        """

        for event in sample_event_list:
            self.test_single_event(sample=event['sample'])

        return None

    def test_all_events(self, sample_event_directory, file_name, file_prefix='input'):
        """ Tests all events from a specified file or all the saved input sample.

        :param sample_event_directory: The name of the directory where sample files are saved.
        :param file_name: The name of a specific file to test. A file should be a list with dictionaries.
        :param file_prefix: Specific a file prefix to test all the events in files with a similar name.  The defaul will test all the samples for all inputs that have been saved using the Samples.save_alooma_samples_to_files function.
        :return: True if the samples should be printed to the console
        """

        S = Samples(api=self.api, sample_event_directory=sample_event_directory)

        if file_name is None:
            for file in os.listdir(sample_event_directory):
                if file.endswith(".json") and file.startswith(file_prefix):
                    file_path = (os.path.join(sample_event_directory, file))
                    sample_event_list = S.get_samples_from_file(file_path)
                    self.loop_through_events_to_test(sample_event_list)

        else:
            file_path = (os.path.join(sample_event_directory, file_name))
            sample_event_list = S.get_samples_from_file(file_path)
            self.loop_through_events_to_test(sample_event_list)

        return None

