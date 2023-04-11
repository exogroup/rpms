#!/bin/bash
#
# VERY rough around the edges. 'Just works' as ./prep-packages.sh
#

shopt -s dotglob

# This gets the version string from the .spec file, so change it there first
COMMIT="$(grep "^%global commit " clickhouse_exporter.spec | awk '{print $3}')"
SHORTCOMMIT=${COMMIT:0:7}
WD=$(pwd)

rm -rf clickhouse_exporter-*

git clone https://github.com/ClickHouse/clickhouse_exporter.git clickhouse_exporter-${SHORTCOMMIT}
cd clickhouse_exporter-${SHORTCOMMIT}
git checkout "${COMMIT}"

rm -rf .git*
# Sources need to be in $GOPATH/src/github.com/... during build
mkdir -p src/github.com/ClickHouse/clickhouse_exporter
mv * src/github.com/ClickHouse/clickhouse_exporter 2>/dev/null

cd src/github.com/ClickHouse/clickhouse_exporter
GOPATH=${WD}/clickhouse_exporter-${SHORTCOMMIT} GO111MODULE=on go mod download -x
chmod -R u+w ${WD}/clickhouse_exporter-${SHORTCOMMIT}/pkg

cd $WD
tar czf clickhouse_exporter-${SHORTCOMMIT}.tar.gz clickhouse_exporter-${SHORTCOMMIT}
rm -rf clickhouse_exporter-${SHORTCOMMIT}
ls -lh clickhouse_exporter-${SHORTCOMMIT}.tar.gz
