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
    assert update_revision["object"]["id"] == revision["object"]["id"]
