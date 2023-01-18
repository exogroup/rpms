#!/bin/bash

# This script downloads sources and modifies them

set -ex

NAME="mariadb"
VERSION=$( rpmspec -q --srpm --qf '%{VERSION}' "${NAME}.spec" )
# SOURCES_URL=$( spectool -s 0 "$NAME.spec" | cut -d ' ' -f 2 )
SOURCES_URL="https://downloads.mariadb.org/interstitial/mariadb-${VERSION}/source/mariadb-${VERSION}.tar.gz"

OLD_ARCHIVE_NAME="${NAME}-${VERSION}"
NEW_ARCHIVE_NAME="${NAME}-${VERSION}-downstream_modified"

# Retrieve the archive:

rm -rf "./${OLD_ARCHIVE_NAME}.tar.gz" "./${OLD_ARCHIVE_NAME}/" "./${NEW_ARCHIVE_NAME}.tar.gz" "./${NEW_ARCHIVE_NAME}/"
wget "${SOURCES_URL}"

# Modify the archive:

# 1/ Change both the name of the archive and the name of the base directory inside of the archive
#    It will be necessary to change the name in the SPECfile in the %prep phase
#    This will prevent maintainer to rebase to a non-modified sources archive without changing the SPECfile

tar -xof "${OLD_ARCHIVE_NAME}.tar.gz"
mv "${OLD_ARCHIVE_NAME}" "${NEW_ARCHIVE_NAME}"

# 2/ Remove the code licensed under the PerconaFT license
#    which was not yet reviewed as suitable for Fedora or RHEL.
#
#    License file:
#      storage/tokudb/PerconaFT/PATENTS
#
#    The whole storage engine, which requires code under this license
#    has to be removed before uploading sources to Fedora.

rm -r "${NEW_ARCHIVE_NAME}/storage/tokudb"

# Pack the extracted files back to the archive

tar -czf "${NEW_ARCHIVE_NAME}.tar.gz" "${NEW_ARCHIVE_NAME}"

# Remove the decompressed original used to create the archive

rm -r "./${NEW_ARCHIVE_NAME}/"
