#!/usr/bin/env python
# -*- coding: utf-8 -*-

from azure.common.client_factory import get_client_from_cli_profile
from azure.keyvault import KeyVaultClient
from msrestazure.azure_active_directory import MSIAuthentication
import re


class KeyVault:
    def __init__(self, name):
        self.name = name

        try:
            self.client = get_client_from_cli_profile(KeyVaultClient)

        except:
            self.client = KeyVaultClient(MSIAuthentication())

    """
    get secret value of a specified secret

    parameters:
        - secret_id: name or url of the secret
        - secret_version: version to retrieve

    return:
        - value of the secret
    """

    def get_secret(self, secret_id, secret_version=''):

        secret_id = re.sub(
            "https://{0}.vault.azure.net/secrets/".format(self.name),
            "",
            secret_id)

        try:

            secret_bundle = self.client.get_secret(
                "https://{0}.vault.azure.net/".format(self.name),
                secret_id,
                secret_version)

        except:
            return None

        return secret_bundle.value

    """
    get all secrets ids in vault

    parameters:
        - none

    return:
        - list of secrets (use .id to pass to get_secret method)
    """

    def get_secrets(self):
        return self.client.get_secrets(
            "https://{0}.vault.azure.net/".format(self.name)
        )

    """
    set secret specified

    parameters:
        - secret_id: name of secret to set
        - value: secret value to set

    return:
        - none
    """

    def set_secret(self, secret_id, value):
        self.client.set_secret(
            "https://{0}.vault.azure.net/".format(self.name),
            secret_id,
            value
        )
