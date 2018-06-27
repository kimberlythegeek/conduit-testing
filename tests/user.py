from pytest_bugzilla_notifier.bugzilla_rest_client import BugzillaRESTClient
from phabricator import Phabricator


def generate_transactions(dictionary):
    """Generate a list of Phabricator transactions."""
    transactions = []
    for key, value in dictionary.items():
        transactions.append(
            {"type": key, "value": value}
        )
    return transactions

class User:
    def __init__(self, bug_host, bug_key, phab_host, phab_key):
        api_details = {
            "bugzilla_host": bug_host,
            "bugzilla_api_key": bug_key
        }
        client = BugzillaRESTClient(api_details)

        phab = Phabricator(
            host=phab_host,
            token=phab_key
        )
        phab.update_interfaces()
        self.bugzilla = client
        self.phab = phab


    def create_bug(self, product="Firefox", component="Developer Tools",
                   summary="Test Bug", version="unspecified"):
        """Create a bug on Bugzilla."""
        bug_data = {
            "product": product,
            "component": component,
            "summary": summary,
            "version": version
        }
        return self.bugzilla.bug_create(bug_data)

    def create_diff(self):
        """Create a diff on Phabricator."""
        phab = self.phab
        changes = [{
                "metadata": [],
                "oldPath": "arcanist.txt",
                "currentPath": "arcanist.txt",
                "awayPaths": [],
                "oldProperties": [],
                "newProperties": [],
                "type": 2,
                "fileType": 1,
                "commitHash": None,
                "hunks": [
                    {
                        "oldOffset": "1",
                        "newOffset": "1",
                        "oldLength": "1",
                        "newLength": "2",
                        "addLines": 1,
                        "delLines": 0,
                        "isMissingOldNewline": False,
                        "isMissingNewNewline": False,
                        "corpus": " FIRST COMMENT\n+Second commit\n"
                    }
                ]
            }]
        creatediff_response = phab.differential.creatediff(
            changes=changes,
            sourceMachine="localmachine",
            # FIXME: os-independent file path
            sourcePath="\/Users\/localuser\/phabricator-qa-dev\/",
            branch="default",
            sourceControlSystem="hg",
            sourceControlPath="\/",
            sourceControlBaseRevision="62a4917ca0075386afb8d694ad8910b0e76532fa",
            unitStatus="none",
            lintStatus="none"
            # parentRevisionID="123456",
            # authorPHID=phab.user.whoami().phid,
            # repositoryUUID="12343545"
        )
        return creatediff_response

    def create_revision(self, bug_id, diff, transactions=None):
        """Create a revision on Phabricator."""
        if not transactions:
            transactions = generate_transactions({
                "update": str(diff.phid),
                "title": "Commit message",
                "summary": "Summary",
                "testPlan": "QA create a revision",
                "bugzilla.bug-id": str(bug_id)
        })
        else:
            transactions = generate_transactions(transactions)
        revision = self.phab.differential.revision.edit(
            transactions=transactions
        )
        return revision

    def update_revision(self, bug_id, diff, revision, transactions=None):
        """Update a revision on Phabricator."""
        if not transactions:
            transactions = [
                {"type": "update", "value": str(diff.phid)},
                {"type": "title", "value": "Commit message"},
                {"type": "summary", "value": "Summary"},
                {"type": "testPlan", "value": "QA update a revision"},
                {"type": "bugzilla.bug-id", "value": str(bug_id)}
            ]
        else:
            transactions = generate_transactions(transactions)
        updated_revision = self.phab.differential.revision.edit(
            transactions=transactions,
            objectIdentifier=revision["object"]["id"]
        )
        return updated_revision

    def search_for_revision(self, revision_id):
        """Search for a revision on Phabricator."""
        constraints = {"ids": [revision_id]}
        revisionsearch_response = self.phab.differential.revision.search(
            constraints=constraints
        )
        return revisionsearch_response.data[0]
