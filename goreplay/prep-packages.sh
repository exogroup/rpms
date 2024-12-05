#!/bin/bash
#
# VERY rough around the edges. 'Just works' as ./prep-packages.sh
#

# This gets the version string from the .spec file, so change it there first
VERSION="$(grep "^Version:" goreplay.spec | awk '{print $2}')"
# Temporary directory to store git config and go cache
LOCAL=$(pwd)/.home
mkdir -p ${LOCAL}

rm -rf goreplay-*

git clone -b "${VERSION}" https://github.com/buger/goreplay goreplay-${VERSION} || exit 1
pushd goreplay-${VERSION}

rm -rf .git* .dockerignore
# Change $HOME for go mod to store cache
HOME=${LOCAL} go mod vendor || exit 1

popd
chmod u+w -R goreplay-${VERSION} ${LOCAL}
tar czf goreplay-${VERSION}.tar.gz goreplay-${VERSION}
rm -rf goreplay-${VERSION}
ls -lh goreplay-${VERSION}.tar.gz
