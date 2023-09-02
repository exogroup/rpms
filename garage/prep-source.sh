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
test -f v${VERSION}.tar.gz || \
  wget https://git.deuxfleurs.fr/Deuxfleurs/garage/archive/v${VERSION}.tar.gz
rm -rf garage garage-${VERSION}-vendor
tar xzvf v${VERSION}.tar.gz
cd garage
cargo vendor
mkdir .cargo
cat > .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
# Neuter the sources we will never need to save space :-) (keep Cargo.toml)
# (down from 100MB to 28MB sources for 0.8.3)
cd vendor
for i in aws* win* k8s* prost* libsqlite3* ring linux* web*; do
  # We need to keep most first level src/*.rs files
  find $i/src -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;
  rm -rf $i/{lib,third*party}
done
rm -rf libsodium-sys/{mingw}
rm -rf libsqlite3-sys/{sqlcipher,sqlite3}
rm -rf ring/{crypto,pregenerated}
rm -rf web-sys/webidls
# TODO: Remove at least *.lib and *.a from libsodium-sys/.cargo-checksum.json
find libsodium-sys \( -name '*.lib' -o -name '*.a' \) -exec truncate -s 0 {} \;
cat libsodium-sys/.cargo-checksum.json | json_reformat | grep -E -v '"(mingw|msvc)/' > tmp
mv tmp libsodium-sys/.cargo-checksum.json
cd ..
rm -rf doc
cd ..
mv garage garage-${VERSION}-vendor
tar czvf garage-${VERSION}-vendor.tar.gz garage-${VERSION}-vendor
ls -lh garage-${VERSION}-vendor.tar.gz
