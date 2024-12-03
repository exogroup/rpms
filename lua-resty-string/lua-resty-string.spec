%global lua_version 5.1

Summary: Lua string utilities and common hash functions for ngx_lua
Name: lua-resty-string
Version: 0.16
Release: 1%{?dist}
License: BSD
URL: https://github.com/openresty/lua-resty-string
Source0: https://github.com/openresty/lua-resty-string/archive/refs/tags/v%{version}/lua-resty-string-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: lua-resty-core
BuildRequires: make
BuildRequires: luajit-resty-devel

%description
Lua string utilities and common hash functions for ngx_lua.


%prep
%setup -q -n lua-resty-string-%{version}


%build
# Lua only, nothing to see here


%install
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_pkgdir}


%files
%doc README.markdown
%dir %{lua_pkgdir}/
%dir %{lua_pkgdir}/resty/
%{lua_pkgdir}/resty/*.lua


%changelog
* Tue Dec  3 2024 Matthias Saou <matthias@saou.eu> 0.16-1
- Initial RPM release.

