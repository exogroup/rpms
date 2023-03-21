#!/bin/bash
#
# VERY rough around the edges. 'Just works' as ./prep-packages.sh
#

shopt -s dotglob

# This gets the version string from the .spec file, so change it there first
VERSION="$(grep "^Version:" couchbase_exporter.spec | awk '{print $2}')"

rm -rf couchbase_exporter-*

git clone https://github.com/couchbase/couchbase-exporter.git couchbase_exporter-${VERSION}
pushd couchbase_exporter-${VERSION}
git checkout "${VERSION}"

rm -rf .git*
mkdir -p src/github.com/couchbase/couchbase-exporter
mv * src/github.com/couchbase/couchbase-exporter 2>/dev/null
export GOPATH="${PWD}"
pushd src/github.com/couchbase/couchbase-exporter
go get all
go mod vendor -v
popd
popd
chmod u+w -R couchbase_exporter-${VERSION}
rm -rf couchbase_exporter-${VERSION}/pkg/mod/cache
tar czf couchbase_exporter-${VERSION}.tar.gz couchbase_exporter-${VERSION}
rm -rf couchbase_exporter-${VERSION}
ls -lh couchbase_exporter-${VERSION}.tar.gz
