# Extracted from the .gitmodule's hash
%global helio_version 0.2.0

Summary: Modern replacement for Redis and Memcached
Name: dragonfly
Version: 0.11.0
Release: 1%{?dist}
License: BSL 1.1
URL: https://dragonflydb.io/
Source0: https://github.com/dragonflydb/dragonfly/archive/refs/tags/v%{version}/dragonfly-%{version}.tar.gz
Source1: dragonfly.service
Source2: dragonfly.sysconfig
Source10: https://github.com/romange/helio/archive/refs/tags/v%{helio_version}/helio-%{helio_version}.tar.gz
# 3rd party content tried to download at build time (no-no!)
# These are all extracted from:
# * helio-*/cmake/third_party.cmake -> helio-*-url_hash.patch
# * src/CMakeLists.txt -> dragonfly-*-url_hash.patch
# The URL_HASH is required, or a new download gets triggered anyway
# helio (not all included seem relevant/needed for dragonfly)
Source11: https://github.com/google/googletest/archive/release-1.11.0.zip
Source12: https://github.com/google/benchmark/archive/v1.6.1.tar.gz
Source13: https://github.com/abseil/abseil-cpp/archive/20220623.0.tar.gz
# This is taken from a custom branch called 'Absl'
Source14: https://github.com/romange/glog/archive/e433227/glog-e433227.tar.gz
Source15: https://github.com/axboe/liburing/archive/refs/tags/liburing-2.2.tar.gz
Source16: https://github.com/microsoft/mimalloc/archive/refs/tags/v2.0.5.tar.gz
Source17: https://github.com/gperftools/gperftools/archive/gperftools-2.9.1.tar.gz
Source18: https://github.com/Cyan4973/xxHash/archive/v0.8.0.tar.gz
# dragonfly
Source21: https://github.com/danielaparker/jsoncons/archive/refs/tags/v0.168.7.tar.gz
Source22: https://github.com/google/double-conversion/archive/refs/tags/v3.2.0.tar.gz
Source23: https://github.com/lua/lua/archive/refs/tags/v5.4.4.tar.gz
Patch11: helio-0.2.0-url_hash.patch
Patch21: dragonfly-0.11.0-url_hash.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: gcc-c++
BuildRequires: libunwind-devel
BuildRequires: boost-devel
BuildRequires: openssl-devel
BuildRequires: libxml2-devel
BuildRequires: autoconf-archive
BuildRequires: libtool
BuildRequires: libatomic
BuildRequires: systemd

%description
Dragonfly is a modern in-memory datastore, fully compatible with Redis and
Memcached APIs. Dragonfly implements novel algorithms and data structures on
top of a multi-threaded, shared-nothing architecture. As a result, Dragonfly
reaches x25 performance compared to Redis and supports millions of QPS on a
single instance.

Dragonfly's core properties make it a cost-effective, high-performing, and
easy-to-use Redis replacement.


%prep
%setup -q -a 10
%patch11 -p0
%patch21 -p1
rmdir helio
mv helio-%{helio_version} helio
# helio
mkdir -p build-opt/_deps/gtest-subbuild/gtest-populate-prefix/src/
cp -a %{SOURCE11} build-opt/_deps/gtest-subbuild/gtest-populate-prefix/src/
mkdir -p build-opt/_deps/benchmark-subbuild/benchmark-populate-prefix/src/
cp -a %{SOURCE12} build-opt/_deps/benchmark-subbuild/benchmark-populate-prefix/src/
mkdir -p build-opt/_deps/abseil_cpp-subbuild/abseil_cpp-populate-prefix/src/
cp -a %{SOURCE13} build-opt/_deps/abseil_cpp-subbuild/abseil_cpp-populate-prefix/src/
mkdir -p build-opt/_deps/glog-subbuild/glog-populate-prefix/src/
cp -a %{SOURCE14} build-opt/_deps/glog-subbuild/glog-populate-prefix/src/
mkdir -p build-opt/third_party/uring/
cp -a %{SOURCE15} build-opt/third_party/uring/
mkdir -p build-opt/third_party/mimalloc/
cp -a %{SOURCE16} build-opt/third_party/mimalloc/
mkdir -p build-opt/third_party/gperf/
cp -a %{SOURCE17} build-opt/third_party/gperf/
mkdir -p build-opt/third_party/xxhash/
cp -a %{SOURCE18} build-opt/third_party/xxhash/
# dragonfly
mkdir -p build-opt/third_party/jsoncons/
cp -a %{SOURCE21} build-opt/third_party/jsoncons/
mkdir -p build-opt/third_party/dconv/
cp -a %{SOURCE22} build-opt/third_party/dconv/
mkdir -p build-opt/third_party/lua/
cp -a %{SOURCE23} build-opt/third_party/lua/


%build
./helio/blaze.sh -release
cd build-opt
ninja dragonfly


%install
rm -rf %{buildroot}
install -D -m 0755 build-opt/dragonfly %{buildroot}%{_bindir}/dragonfly
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/dragonfly.service
install -D -p -m 0640 %{SOURCE2} %{buildroot}/etc/sysconfig/dragonfly
install -d -m 0750 %{buildroot}/var/lib/dragonfly
install -d -m 0750 %{buildroot}/var/log/dragonfly


%pre
getent group dragonfly >/dev/null || groupadd -r dragonfly
getent passwd dragonfly >/dev/null || \
  useradd -r -d /var/lib/dragonfly -g dragonfly \
  -s /sbin/nologin -c "Dragonfly" dragonfly

%post
%systemd_post dragonfly.service

%preun
%systemd_preun dragonfly.service

%postun
# Don't use '_with_restart' variant, as it would flush all cache
%systemd_postun dragonfly.service


%files
%doc CONTRIBUTORS.md LICENSE.md README.md TODO.md
%config(noreplace) %attr(0640,root,dragonfly) /etc/sysconfig/dragonfly
%{_bindir}/dragonfly
%{_unitdir}/dragonfly.service
%attr(0750,dragonfly,dragonfly) /var/lib/dragonfly
%attr(0750,dragonfly,dragonfly) /var/log/dragonfly


%changelog
* Wed Nov 16 2022 Matthias Saou <matthias@saou.eu> 0.11.0-1
- Initial RPM release.

