#!/bin/bash
# Very fragile, but gets the simple job done
# A lot more than we actually need gets downloaded... *cough* windows *cough*
# but cannot be deleted, or the build fails

if [[ -z "$1" ]]; then
  echo "Usage: $0 <version> [branch]"
  exit 1
fi

if [[ -n "$2" ]]; then
  BRANCH=$2
fi

if ! which cargo &>/dev/null; then
  echo "You must install the 'cargo' executable"
  exit 1
fi

VERSION=$1

rm -rf php-client-${VERSION}

if [[ -z "$BRANCH" ]]; then
  wget https://github.com/aerospike/php-client/archive/refs/tags/v${VERSION}/php-client-${VERSION}.tar.gz
  tar xzvf php-client-${VERSION}.tar.gz
  rm -f php-client-${VERSION}.tar.gz
else
  git clone git@github.com:aerospike/php-client.git --depth=1 --branch=$BRANCH php-client-${VERSION}
fi

cd php-client-${VERSION}
cargo vendor
mkdir .cargo
cat > .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/aerospike/aerospike-client-rust.git?branch=php-rs"]
git = "https://github.com/aerospike/aerospike-client-rust.git"
branch = "php-rs"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
# Neuter the sources we will never need to save space :-) (keep Cargo.toml)
# (down from 546MB to 93MB sources for 0.1.0)
cd vendor
for i in vcpkg win*; do
  # We need to keep most first level src/*.rs files
  find $i/src -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;
  rm -rf $i/{lib,third*party}
done
cd ..

# Now we have the Go daemon too
cd aerospike-connection-manager
# This is a PITA for el9, so create from Fedora
make proto
# Change $HOME for go mod to store cache
LOCAL=$(pwd)/.home
HOME=${LOCAL} go mod tidy || exit 1
HOME=${LOCAL} go mod vendor || exit 1
chmod -R u+w ${LOCAL}
rm -rf ${LOCAL}
cd ..

cd ..
mv php-client-${VERSION} php-client-${VERSION}-vendor
tar czvf php-client-${VERSION}-vendor.tar.gz php-client-${VERSION}-vendor
rm -rf php-client-${VERSION}-vendor
ls -lh php-client-${VERSION}-vendor.tar.gz
