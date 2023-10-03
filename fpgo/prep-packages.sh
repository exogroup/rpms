#!/bin/bash
#
# VERY rough around the edges. 'Just works' as ./prep-packages.sh
#

# This gets the version string from the .spec file, so change it there first
VERSION="$(grep "^Version:" fpgo.spec | awk '{print $2}')"
# Temporary directory to store git config and go cache
LOCAL=$(pwd)/.home
mkdir -p ${LOCAL}

rm -rf fpgo-*

git clone -b "v${VERSION}" https://github.com/joeky888/fpgo fpgo-${VERSION} || exit 1
pushd fpgo-${VERSION}

rm -rf .git* .dockerignore
# Change $HOME for go mod to store cache
HOME=${LOCAL} go mod vendor || exit 1

popd
chmod u+w -R fpgo-${VERSION} ${LOCAL}
tar czf fpgo-${VERSION}.tar.gz fpgo-${VERSION}
rm -rf fpgo-${VERSION}
ls -lh fpgo-${VERSION}.tar.gz
