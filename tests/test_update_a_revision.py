import os
import time

from phabricator import Phabricator

def test_update_a_revision(secure_user_one):
    bug_id = secure_user_one.create_bug()
    diff = secure_user_one.create_diff()
    revision = secure_user_one.create_revision(bug_id, diff)
    print(revision)

    diff2 = secure_user_one.create_diff()
    updated_revision = secure_user_one.update_revision(bug_id, diff, revision)
    print(updated_revision)
    assert updated_revision["object"]["phid"] == revision["object"]["phid"]
    assert updated_revision["object"]["id"] == revision["object"]["id"]

    """
    Now read back details of the revision and make sure values are as
    we expect them to be
    """
    revision_id = updated_revision["object"]["id"]
    revision_search = secure_user_one.search_for_revision(revision_id)
    assert revision_search["id"] == revision_id
    assert revision_search["fields"]["title"] == "Commit message"
    assert revision_search["fields"]["summary"] == "Summary"
    assert revision_search["fields"]["testPlan"] == "QA update a revision"
    assert revision_search["fields"]["bugzilla.bug-id"] == "Commit message"
    assert revision_search["fields"]["title"] == "Commit message"
    assert revision_search["fields"]["title"] == "Commit message"
