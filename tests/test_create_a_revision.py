import os
import time



def test_create_a_revision(secure_user_one):
    bug_id = secure_user_one.create_bug("Firefox", "Developer Tools",
                                        "Test Bug", "unspecified")

    # Grab the bug and let"s see what data exists
    response = secure_user_one.bugzilla.bug_read(bug_id)
    bug_info = response["bugs"][0]
    assert "product" in bug_info
    assert "component" in bug_info
    assert "summary" in bug_info
    assert "version" in bug_info
    assert bug_info["product"] == "Firefox"
    assert bug_info["component"] == "Developer Tools"
    assert bug_info["summary"] == "Test Bug"
    assert bug_info["version"] == "unspecified"

    # Create a diff on Phabricator
    diff = secure_user_one.create_diff()
    # Now create the revision using the diff information
    revision = secure_user_one.create_revision(bug_id, diff)
    print(revision)
    assert revision["object"]["phid"] is not None
    assert revision["object"]["id"] is not None

    """
    Now read back details of the revision and make sure values are as
    we expect them to be
    """
    revision_id = revision["object"]["id"]
    phab = secure_user_one.phab
    constraints = {"ids": [revision_id]}
    revisionsearch_response = phab.differential.revision.search(
        constraints=constraints
    )
    # We are expecting our records to be in the first element of the list
    data = revisionsearch_response.data[0]
    assert data["id"] == revision_id
    assert data["fields"]["title"] == "Commit message"

    """
    Now we need to read the bug and look for our attachment that proves
    Phabricator has updated the bug

    The sleep statement is required because updating a bug does not happen
    instantly

    This test only ever generates one attachment for the bug
    """
    time.sleep(8)
    response = secure_user_one.bugzilla.get_attachments(bug_id)
    bug_info = response["bugs"]
    assert bug_info[str(bug_id)][0]["content_type"] == "text/x-phabricator-request"
