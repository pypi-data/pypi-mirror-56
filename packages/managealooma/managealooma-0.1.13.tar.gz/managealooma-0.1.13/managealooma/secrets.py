class Secrets:

    def __init__(self, api):
        """ Manages secrets in Alooma. Secrets are Alooma's way of using Environment variables.

        :param api: The Alooma API client authentication
        """

        self.api = api

    def set_secrets(self, secrets_dict):
        """ Sets the secrets in Alooma.

        :param secrets_dict: A dictionary with the secrets as k, v pairs. ex: {"my_user": "example", "my_password": "12345678"}
        :return: None

        """

        response = self.api.set_secrets(secrets_dict)
        print("SET SECRETS:", response)

    def get_secrets(self):
        """ Gets the list of secrets and prints the list.

        :return: None
        """
        secrets = self.api.get_secrets()  # returns ["my_user", "my_password"]
        print(secrets)

        return None

    def delete_secrets(self, secret):
        """ Deletes a secret from Alooma.

        :param secret: The name of the secret to delete. ex: {"my_user": "example", "my_password": "12345678"}  Set to my_user to delete that secret.
        :return: None
        """

        response = self.api.delete_secret(secret)  # deletes "my_user"
        print("DELETED SECRET:", secret, response)
