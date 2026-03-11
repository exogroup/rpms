#!/bin/bash
#
# VERY rough around the edges. 'Just works' as ./prep-packages.sh
#

# This gets the version string from the .spec file, so change it there first
VERSION="$(grep "^Version:" zkcli.spec | awk '{print $2}')"
COMMIT="$(grep "%define commit" zkcli.spec | awk '{print $3}')"

# Temporary directory to store git config and go cache
LOCAL=$(pwd)/.home
mkdir -p ${LOCAL}

rm -rf zkcli-*

# https://github.com/maxjustus/zkcli/archive/%{commit}.tar.gz
git clone https://github.com/maxjustus/zkcli zkcli-${VERSION} || exit 1
pushd zkcli-${VERSION}

git checkout ${COMMIT}

rm -rf .git* .dockerignore
# Change $HOME for go mod to store cache
HOME=${LOCAL} go mod vendor || exit 1

popd
chmod u+w -R zkcli-${VERSION} ${LOCAL}
tar czf zkcli-${VERSION}.tar.gz zkcli-${VERSION}
rm -rf zkcli-${VERSION} ${LOCAL}
ls -lh zkcli-${VERSION}.tar.gz

