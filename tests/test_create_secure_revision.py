import subprocess

setup_workspace_commands = [
    "rm -rf workspace/*",
    "git clone https://github.com/phacility/libphutil workspace/libphutil",
    "git clone https://github.com/phacility/arcanist workspace/arcanist",
    "git clone https://github.com/mozilla-conduit/arcanist --branch master --single-branch workspace/cinnabarc",
    "alias arc='/Users/ksereduck/Workspace/conduit-testing/workspace/arcanist/bin/arc'",
    "git clone https://github.com/glandium/git-cinnabar.git --branch master --single-branch workspace/git-cinnabar",
    "export PATH=/Users/ksereduck/Workspace/conduit-testing/workspace/git-cinnabar:$PATH",
    "cd workspace/git-cinnabar && git cinnabar download",
    "alias cinnabarc='/Users/ksereduck/Workspace/conduit-testing/workspace/cinnabarc/bin/arc'",
    "hg clone https://hg.mozilla.org/automation/phabricator-qa-dev/ workspace/phabricator-qa-dev",
    "git clone hg::https://hg.mozilla.org/automation/phabricator-qa-dev/ phabricator-qa-dev-cinnabar",
]

for step in setup_workspace_commands:
    subprocess.run(step, shell=True)
