%global rctag beta3
%global date 20230410

Name:           luajit-resty
Version:        2.1.0
%global apiver %(v=%{version}; echo ${v%.${v#[0-9].[0-9].}})
%global srcver %{version}%{?rctag:-%{rctag}}
Release:        0.2%{?date:_%{date}}%{?dist}
Summary:        OpenResty version of the Just-In-Time Compiler for Lua
License:        MIT
URL:            https://github.com/openresty/luajit2/
Source0:        https://github.com/openresty/luajit2/archive/refs/tags/v%{apiver}%{?date:-%{date}}/luajit2-%{apiver}%{?date:-%{date}}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
# This is required by C modules
Provides:       lua(abi) = 5.1

%description
LuaJIT implements the full set of language features defined by Lua 5.1.
The virtual machine (VM) is API- and ABI-compatible to the standard
Lua interpreter and can be deployed as a drop-in replacement.

This is the official OpenResty branch of LuaJIT.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%package static
Summary:        Library for statically linking %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
This package contains the static library for %{name}.

%prep
%autosetup -n luajit2-%{apiver}%{?date:-%{date}}

# Enable Lua 5.2 features
sed -i -e '/-DLUAJIT_ENABLE_LUA52COMPAT/s/^#//' src/Makefile

# preserve timestamps (cicku)
sed -i -e '/install -m/s/-m/-p -m/' Makefile

%build
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
make amalg Q= E=@: PREFIX=%{_prefix} TARGET_STRIP=: \
           CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}" \
           MULTILIB=%{_lib} \
           %{?_smp_mflags}

%install
# PREREL= - disable -betaX suffix
# INSTALL_TNAME - executable name
%make_install PREFIX=%{_prefix} \
              MULTILIB=%{_lib}

rm -rf _tmp_html ; mkdir _tmp_html
cp -a doc _tmp_html/html

%ldconfig_scriptlets

%check
# Don't fail the build on a check failure.
make check || true

%files
%license COPYRIGHT
%doc README*
%{_bindir}/luajit
%{_bindir}/luajit-%{srcver}
%{_libdir}/libluajit-*.so.*
%{_mandir}/man1/luajit.1*
%{_datadir}/luajit-%{srcver}/

%files devel
%doc _tmp_html/html/
%{_includedir}/luajit-%{apiver}/
%{_libdir}/libluajit-*.so
%{_libdir}/pkgconfig/luajit.pc

%files static
%{_libdir}/libluajit-*.a

%changelog
* Thu May 18 2023 Matthias Saou <matthias@saou.eu> 2.1-0.2_20230410
- Provide "lua(abi) = 5.1" required by C modules (cjson).

* Tue May 16 2023 Matthias Saou <matthias@saou.eu> 2.1-0.1_20230410
- Fork Fedora spec as luajit-resty with OpenResty sources, used for nginx module.

