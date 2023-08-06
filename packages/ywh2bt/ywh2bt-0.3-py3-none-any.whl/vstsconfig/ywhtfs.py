from vstsclient.vstsclient import VstsClient
from vstsclient.models import JsonPatchDocument, JsonPatchOperation
from vstsclient.constants import SystemFields, MicrosoftFields
from vstsclient._http import HTTPError
from colorama import Fore, Style
from ywh2bt.trackers.bugtracker import BugTracker
from ywh2bt.utils import read_input
from ywh2bt.config import BugTrackerConfig

class NewVstsClient(VstsClient):
    """Override VstsClient Base class for add Scheme support"""

    def __init__(self, *args, scheme="HTTP", **kwargs):
        super(NewVstsClient, self).__init__(*args, **kwargs)
        self._http_client.protocol = scheme


class YWHTfs(BugTracker):

    def __init__(self, url, project, token, assigned_to, collection="DefaultCollection", issuetype="Task"):
        self.__define_client__(
            url,
            token,
            scheme=url.split("://")[0].upper() or "HTTP",
            collection=collection,
        )

        try:
            projects = self.bt.get_projects()
        except HTTPError:
            raise

        self.issuetype = Task
        self.assigned_to = assigned_to

        if project:
            self.project = project
            if self.project not in [project.name for project in projects]:
                raise Exception(
                    "Project Name does'nt exist in {url}".format(config["url"])
                )

    def __define_client__(self, url, pat, collection, scheme="HTTP"):
        self.bt = NewVstsClient(
            url,
            scheme=scheme,
            personal_access_token=pat,
            collection=collection,
        )

    def get_project(self):
        try:
            repo = self.bt.get_project(self.project)
        except HTTPError:
            raise
        return repo

    def post_issue(self, report):
        description = self.description_template
        title = self.issue_name_template.format(
            report_local_id=report.local_id, report_title=report.title
        )
        body = description.format(
            end_point=report.end_point,
            vulnerable_part=report.vulnerable_part,
            cvss=report.cvss.score,
            bug_type=report.bug_type.category.name,
            bug_description=report.bug_type.description,
            remediation_link=report.bug_type.link,
            description=report.description_html,
        )
        doc = JsonPatchDocument()
        doc.add(JsonPatchOperation("add", SystemFields.TITLE, title))
        doc.add(JsonPatchOperation("add", SystemFields.DESCRIPTION, body))
        doc.add(JsonPatchOperation("add", SystemFields.TAGS, "ywh-report"))
        doc.add(
            JsonPatchOperation(
                "add", SystemFields.ASSIGNED_TO, self.assigned_to
            )
        )
        # Create a new work item by specifying the project and work item type
        try:
            workitem = self.bt.create_workitem(
                self.project, self.issuetype, doc
            )
        except HTTPError:
            raise
        return workitem

    def get_url(self, issue):
        return issue.url

    def get_id(self, issue):
        return issue.id


class YWHTfsConfig(BugTrackerConfig):

    bugtracker_type = "tfs"
    client = YWHTfs
    mandatory_keys = ["url", "project", "assigned_to"]
    secret_keys = ["token"]
    optional_keys = dict(issuetype="Task",collection="DefaultCollection")

    # def __init__(
    #         self, name, no_interactive=False, configure_mode=False, **config
    #     ):
            # keys = []
            # self._bugtracker = None

            # if config or not configure_mode:
            #     keys += mandatory_keys
            #     if no_interactive:
            #         keys += secret_keys
            #     super().__init__(
            #         name, keys, no_interactive=no_interactive, **config
            #     )
            #     self._url = config['url']
            #     self._token = config["token"] if no_interactive else ""
            #     self._project = config["project"]
            #     self._assigned_to = config["assigned_to"]
            #     self._issuetype = config.get("issuetype", "Task")
            #     self._collection = config.get("collection", "DefaultCollection")
            # else:
            #     super().__init__(
            #         name,
            #         keys,
            #         no_interactive=no_interactive,
            #         configure_mode=configure_mode,
            #     )

            # if configure_mode:
            #     self.configure()

            # if not no_interactive and not configure_mode:
            #     self.get_interactive_info()

            # if not self._bugtracker:
            #     self._set_bugtracker()


    def config_secret(self):
        self._token = read_input(
            Fore.BLUE
            + "Token for "
            + Fore.GREEN
            + self.url
            + Fore.BLUE
            + ": "
            + Style.RESET_ALL,
            secret=True,
        )

    def config_url(self):
        super().config_url()
        if not self._url.endswith("/tfs"):
            self._url += "/tfs"

    def config_params(self):
        self._collection = (
            read_input(
                Fore.BLUE
                + "Collection name (default: 'DefaultCollection'): "
                + Style.RESET_ALL
            )
            or "DefaultCollection"
        )

        self._assigned_to = read_input(
            Fore.BLUE + "User assignement : " + Style.RESET_ALL
        )

        self._issuetype = (
            read_input(
                Fore.BLUE + "Issue Type (default:  'Task'): " + Style.RESET_ALL
            )
            or "Task"
        )

    def _set_bugtracker(self):
        self._get_bugtracker(
            self._url,
            self._project,
            self._token,
            self._assigned_to,
            issuetype=self._issuetype,
            collection=self._collection
        )