import os
import pytest

from dotenv import load_dotenv, find_dotenv
from user import User


# Check to see if we have a dotenv file and use it
if find_dotenv():
    load_dotenv(find_dotenv())


@pytest.fixture(scope="module")
def secure_user_one():
    bug_host = os.getenv('BUGZILLA_HOST')
    bug_key =  os.getenv('BUGZILLA_API_KEY_1')
    phab_host = os.getenv('PHABRICATOR_API_URL')
    phab_key = os.getenv('PHABRICATOR_API_KEY_1')

    user = User(bug_host, bug_key, phab_host, phab_key)
    return user
