import pprint


class DictionaryDifferences:

    def __init__(self, old_dictionary, new_dictionary, pprint_indent=2, pprint_width=250, pprint_depth=5):
        """ Takes 2 Dictionaries and has methods to print the out

        :param old_dictionary:
        :param new_dictionary:
        :param pprint_indent: The indent value to pprint dictionaries
        :param pprint_width: The width value to pprint dictionaries
        :param pprint_depth: The depth value to pprint dictionaries
        """

        self.old_dictionary = old_dictionary
        self.new_dictionary = new_dictionary
        self.pprint_indent = pprint_indent
        self.pprint_width = pprint_width
        self.pprint_depth = pprint_depth

    def show_dictionary_all(self):
        """ Shows the before and after transformation for entire dictionaries

        :return: None
        """

        if self.old_dictionary is not None and self.new_dictionary is not None:
            print('\n' * 2)
            print('ORIGINAL DICTIONARY'.center(200, '-'))
            pprint.pprint(self.old_dictionary, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)
            print('\n' * 2)
            print('ALTERED DICTIONARY'.center(200, '-'))
            pprint.pprint(self.old_dictionary, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)
        elif self.old_dictionary is not None:
            print('\n' * 2)
            print('DICTIONARY'.center(200, '-'))
            pprint.pprint(self.old_dictionary, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)
        elif self.new_dictionary is not None:
            print('\n' * 2)
            print('DICTIONARY'.center(200, '-'))
            pprint.pprint(self.new_dictionary, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

    def show_dictionary_differences(self, show_matching=True, show_changed=True, show_removed=True, show_added=True):
        """ Shows the matching, changed, removed, and added dictionary keys and values

        :return: None
        """

        removed_key_and_value = {}
        added_key_and_value = {}
        changed_values = {}
        matching_keys_and_values = {}

        for key, value in self.old_dictionary.items():
            if key in self.new_dictionary and value == self.new_dictionary[key]:
                matching_keys_and_values[key] = value
            if key in self.new_dictionary and value != self.new_dictionary[key]:
                changed_values[key] = {'old_value': value, 'new_value': self.new_dictionary[key]}
            if key not in self.new_dictionary:
                removed_key_and_value[key] = value

        for key, value in self.new_dictionary.items():
            if key not in self.old_dictionary:
                added_key_and_value[key] = value

        if show_matching:
            print('\n' * 2)
            print('MATCHING KEYS AND VALUES'.center(200, '-'))
            pprint.pprint(matching_keys_and_values, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        if show_changed:
            print('\n' * 2)
            print('CHANGED VALUES'.center(200, '-'))
            pprint.pprint(changed_values, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        if show_removed:
            print('\n' * 2)
            print('REMOVED KEYS VALUES'.center(200, '-'))
            pprint.pprint(removed_key_and_value, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)

        if show_added:
            print('\n' * 2)
            print('ADDED KEYS AND VALUES'.center(200, '-'))
            pprint.pprint(added_key_and_value, indent=self.pprint_indent, width=self.pprint_width, depth=self.pprint_depth)


