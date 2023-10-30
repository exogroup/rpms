#!/bin/bash
# Very fragile, but gets the simple job done
# A lot more than we actually need gets downloaded... *cough* windows *cough*
# but cannot be deleted, or the build fails

if [[ -z "$1" ]]; then
  echo "Usage: $0 <version>"
  exit 1
fi

if ! which cargo &>/dev/null; then
  echo "You must install the 'cargo' executable"
  exit 1
fi

VERSION=$1
test -f php-client-${VERSION}.tar.gz || \
  wget https://github.com/aerospike/php-client/archive/refs/tags/${VERSION}/php-client-${VERSION}.tar.gz
rm -rf php-client-${VERSION}
tar xzvf php-client-${VERSION}.tar.gz
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
cd ..
mv php-client-${VERSION} php-client-${VERSION}-vendor
tar czvf php-client-${VERSION}-vendor.tar.gz php-client-${VERSION}-vendor
rm -rf php-client-${VERSION}-vendor
ls -lh php-client-${VERSION}-vendor.tar.gz
