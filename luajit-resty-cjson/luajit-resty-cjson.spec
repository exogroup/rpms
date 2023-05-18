%global luaver 5.1
%global luaincludedir %{_includedir}/luajit-2.1
%global lualibdir %{_libdir}/lua/%{luaver}
%global luadatadir %{_datadir}/lua/%{luaver}

Summary: JSON support for Lua
Name: luajit-resty-cjson
Version: 2.1.0.12
Release: 1%{?dist}
License: MIT
URL: https://github.com/openresty/lua-cjson/
Source0: https://github.com/openresty/lua-cjson/archive/refs/tags/%{version}/lua-cjson-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc
BuildRequires: luajit-resty-devel

%description
Lua CJSON provides JSON support for Lua. Features:
Fast, standards compliant encoding/parsing routines.
Full support for JSON with UTF-8, including decoding surrogate pairs.
Optional run-time support for common exceptions to the JSON specification.
No dependencies on other libraries.

This is the OpenResty fork, which icludes bugfixes and additions.


%prep
%setup -q -n lua-cjson-%{version}


%build
make %{?_smp_mflags} CFLAGS="%{optflags}" \
  LUA_INCLUDE_DIR="%{luaincludedir}" \
  LUA_CMODULE_DIR="%{lualibdir}" \
  LUA_MODULE_DIR="%{luadatadir}" \
  LUA_BIN_DIR="%{_bindir}"


%install
for target in install install-extra; do
make $target DESTDIR=%{buildroot} \
  LUA_INCLUDE_DIR="%{luaincludedir}" \
  LUA_CMODULE_DIR="%{lualibdir}" \
  LUA_MODULE_DIR="%{luadatadir}" \
  LUA_BIN_DIR="%{_bindir}"
done


%files
%license LICENSE
%doc README.md
%{_bindir}/json2lua
%{_bindir}/lua2json
%{lualibdir}/cjson.so
%{luadatadir}/cjson/


%changelog
* Thu May 18 2023 Matthias Saou <matthias@saou.eu> 2.1.0.12-1
- Initial RPM release.

