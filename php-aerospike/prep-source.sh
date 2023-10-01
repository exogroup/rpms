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

GH_COMMIT="e37a8a1c404f516d5261da5cb8c7108b79561a4e"
GH_SHORT="${GH_COMMIT:0:7}"
VERSION=$1
test -f php-client-${VERSION}-${GH_SHORT}.tar.gz || \
  wget https://github.com/aerospike/php-client/archive/${GH_COMMIT}/php-client-${VERSION}-${GH_SHORT}.tar.gz
rm -rf php-client-${GH_COMMIT}*
tar xzvf php-client-${VERSION}-${GH_SHORT}.tar.gz
cd php-client-${GH_COMMIT}
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
mv php-client-${GH_COMMIT} php-client-${GH_COMMIT}-vendor
tar czvf php-client-${VERSION}-${GH_SHORT}-vendor.tar.gz php-client-${GH_COMMIT}-vendor
ls -lh php-client-${VERSION}-${GH_SHORT}-vendor.tar.gz
