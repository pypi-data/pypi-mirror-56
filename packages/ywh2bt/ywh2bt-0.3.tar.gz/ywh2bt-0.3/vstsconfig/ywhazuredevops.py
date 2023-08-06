from vstsclient.vstsclient import VstsClient
from vstsclient.models import JsonPatchDocument, JsonPatchOperation
from vstsclient.constants import SystemFields, MicrosoftFields
from colorama import Fore, Style
from .ywhtfs import YWHTfs, YWHTfsConfig, NewVstsClient
from ywh2bt.utils import read_input


class YWHAzuredevops(YWHTfs):
    def __define_client__(self, *args, **kwargs):
        self.bt = NewVstsClient(
            args[0], personal_access_token=args[1], scheme=kwargs["scheme"]
        )


class YWHAzuredevopsConfig(YWHTfsConfig):
    # base_url = "dev.azure.com"
    bugtracker_type = "azuredevops"
    client = YWHAzuredevops
    mandatory_keys = [
        key for key in YWHTfsConfig.mandatory_keys if key != "url"
    ]
    optional_keys = {**YWHTfsConfig.optional_keys, "url": "dev.azure.com"}

    def user_config(self):

        orga = read_input(
            Fore.BLUE
            + "organisation name if you don't have set it in url '{url}/<orga>':".format(
                url=url
            )
            + Style.RESET_ALL
        )

        # project_types = self.bt.get_workitem_types(self.project_name)
        self._url = "{url}/{orga}".format(url=self.url, orga=orga)
