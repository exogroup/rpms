#!/bin/bash
# VERY rough around the edges. 'Just works' as ./prep-packages.sh
# To be replaced later one with proper release .tar.gz download from GH

# This gets the version string from the .spec file, so change it there first
VERSION="$(grep "^Version:" lua-resty-tls-manager.spec | awk '{print $2}')"

git clone git@github.com:exogroup/lua-resty-tls-manager -b v${VERSION} lua-resty-tls-manager-v${VERSION}
rm -rf lua-resty-tls-manager-v${VERSION}/.git

tar czf lua-resty-tls-manager-v${VERSION}.tar.gz lua-resty-tls-manager-v${VERSION}
rm -rf lua-resty-tls-manager-v${VERSION}
