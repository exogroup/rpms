%global lua_version 5.1

Summary: Lua HTTP client cosocket driver for ngx_lua
Name: lua-resty-http
Version: 0.17.2
Release: 2%{?dist}
License: BSD
URL: https://github.com/ledgetech/lua-resty-http
Source0: https://github.com/ledgetech/lua-resty-http/archive/refs/tags/v%{version}/lua-resty-http-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: lua-resty-core
Requires: lua-resty-string
BuildRequires: make
BuildRequires: luajit-resty-devel

%description
Lua HTTP client cosocket driver for ngx_lua.


%prep
%setup -q -n lua-resty-http-%{version}


%build
# Lua only, nothing to see here


%install
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_pkgdir}


%files
%doc README.md
%dir %{lua_pkgdir}/
%dir %{lua_pkgdir}/resty/
%{lua_pkgdir}/resty/http*.lua


%changelog
* Tue Dec  3 2024 Matthias Saou <matthias@saou.eu> 0.17.2-2
- Update to 0.17.2.
- Add new lua-resty-string requirement.

* Thu May 18 2023 Matthias Saou <matthias@saou.eu> 0.17.1-1
- Initial RPM release.

