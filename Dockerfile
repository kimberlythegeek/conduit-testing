FROM ubuntu:trusty

RUN apt-get install git mercurial python3 -y && \
  mkdir /workspace/ &&  /workspace/bin && \
  cd /workspace/bin && \
  git clone https://github.com/phacility/libphutil workspace/bin/libphutil && \
  git clone https://github.com/phacility/arcanist workspace/bin/arcanist && \
  git clone https://github.com/mozilla-conduit/arcanist --branch master --single-branch workspace/bin/cinnabarc && \
  alias arc='/workspace/bin/arcanist/bin/arc' && \
  git clone https://github.com/glandium/git-cinnabar.git --branch master --single-branch workspace/bin/git-cinnabar && \
  export PATH='/workspace/bin/git-cinnabar:$PATH' && \
  hg clone https://hg.mozilla.org/automation/phabricator-qa-dev/ workspace/bin/phabricator-qa-dev && \
  git clone hg::https://hg.mozilla.org/automation/phabricator-qa-dev/ phabricator-qa-dev-cinnabar && \
  cd workspace/bin/git-cinnabar && git cinnabar download


WORKDIR /workspace/
