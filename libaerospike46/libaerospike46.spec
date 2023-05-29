# Either 'libev' (recommended), 'libuv' or 'libevent'
%global eventlib libev

# Git submodules - git submodule status
%global commit_common 4c4bf86e0e1861081872c548bbe00520029dcb89
%global shortc_common %(c=%{commit_common}; echo ${c:0:7})
%global commit_modlua d7f060ce89a6524825dfc2bcace863732d41fa2c
%global shortc_modlua %(c=%{commit_modlua}; echo ${c:0:7})
%global commit_lua    e0725f73702f6d1cebd7042064d6303a583b6fd6
%global shortc_lua    %(c=%{commit_lua};    echo ${c:0:7})
%global commit_luajit 6c4a18258631ff01f963e9a1e64df57d7a453fd6
%global shortc_luajit %(c=%{commit_luajit}; echo ${c:0:7})

# LuaJIT instead of Lua
%bcond_without luajit

Summary: Aerospike C Client Shared Library
Name: libaerospike46
Version: 4.6.24
Release: 1%{?dist}
License: ASL 2.0
URL: https://github.com/aerospike/aerospike-client-c/
Source0: https://github.com/aerospike/aerospike-client-c/archive/%{version}/aerospike-client-c-%{version}.tar.gz
Source1: https://github.com/aerospike/aerospike-common/archive/%{commit_common}/aerospike-common-%{shortc_common}.tar.gz
Source2: https://github.com/aerospike/aerospike-mod-lua/archive/%{commit_modlua}/aerospike-mod-lua-%{shortc_modlua}.tar.gz
Source3: https://github.com/aerospike/lua/archive/%{commit_lua}/lua-%{shortc_lua}.tar.gz
Source4: https://github.com/aerospike/luajit/archive/%{commit_luajit}/luajit-%{shortc_luajit}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: make
BuildRequires: gcc
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: %{eventlib}-devel

%description
The Aerospike C client is used to connect with an Aerospike server and perform
database operations.


%package devel
Summary: Aerospike C Client Shared Library development files
Requires: %{name} = %{version}-%{release}
Requires: openssl-devel
Requires: %{eventlib}-devel

%description devel
The Aerospike C client is used to connect with an Aerospike server and perform
database operations.


%prep
%setup -q -n aerospike-client-c-%{version} -a 1 -a 2 -a 3 -a 4
mv aerospike-common-%{commit_common}/* modules/common/
mv aerospike-mod-lua-%{commit_modlua}/* modules/mod-lua/
mv lua-%{commit_lua}/* modules/lua/
mv luajit-%{commit_luajit}/* modules/luajit/


%build
# Using _smp_mflags breaks ¯\_(ツ)_/¯
make EVENT_LIB=%{eventlib} %{?with_luajit:USE_LUAJIT=1}


%install
rm -rf %{buildroot}
# 'make install' is a hack, just do what pkg/install does
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
cp -a target/*/include/* %{buildroot}%{_includedir}/
cp -a target/*/lib/libaerospike.* %{buildroot}%{_libdir}/


%check
# This requires an actual Aerospike server running
#make EVENT_LIB=%{eventlib} %{?with_luajit:USE_LUAJIT=1} test


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%license LICENSE.md
%doc README.md
%{_libdir}/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.a


%changelog
* Mon May 29 2023 Matthias Saou <matthias@saou.eu> 4.6.24-1
- Update to 4.6.24.

* Thu Mar  4 2021 Matthias Saou <matthias@saou.eu> 4.6.20-1
- Initial RPM release.

