#!/bin/bash
# This gets the version string from the .spec file, so change it there first
VERSION="$(grep "^Version:" docker-distribution-auth.spec | awk '{print $2}')"
NAME="docker-distribution-auth-${VERSION}"
WD=$(pwd)

mkdir -p ${NAME}/src/github.com/cesanta

git clone git@github.com:cesanta/docker_auth --depth 1 \
  -b "${VERSION}" \
  ${NAME}/src/github.com/cesanta/docker_auth

(
  cd ${NAME}/src/github.com/cesanta/docker_auth/auth_server
  GOPATH=${WD}/${NAME} GO111MODULE=on go mod download
  chmod -R u+w ${WD}/${NAME}/pkg
)

tar czf ${NAME}.tar.gz ${NAME}/
rm -rf ${NAME}
ls -lh ${NAME}.tar.gz

