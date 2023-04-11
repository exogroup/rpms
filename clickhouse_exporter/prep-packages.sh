#!/bin/bash
#
# VERY rough around the edges. 'Just works' as ./prep-packages.sh
#

shopt -s dotglob

# This gets the version string from the .spec file, so change it there first
COMMIT="$(grep "^%global commit " clickhouse_exporter.spec | awk '{print $3}')"
SHORTCOMMIT=${COMMIT:0:7}

rm -rf clickhouse_exporter-*

git clone https://github.com/f1yegor/clickhouse_exporter.git clickhouse_exporter-${SHORTCOMMIT}
pushd clickhouse_exporter-${SHORTCOMMIT}
git checkout "${COMMIT}"

rm -rf .git*
mkdir -p src/github.com/f1yegor/clickhouse_exporter
mv * src/github.com/f1yegor/clickhouse_exporter 2>/dev/null
export GOPATH="${PWD}"
pushd src/github.com/f1yegor/clickhouse_exporter
go install -v
popd
popd
tar czf clickhouse_exporter-${SHORTCOMMIT}.tar.gz clickhouse_exporter-${SHORTCOMMIT}
rm -rf clickhouse_exporter-${SHORTCOMMIT}
ls -lh clickhouse_exporter-${SHORTCOMMIT}.tar.gz
