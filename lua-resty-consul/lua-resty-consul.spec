%global lua_version 5.1

Summary: Library to interface with the consul HTTP API from ngx_lua
Name: lua-resty-consul
Version: 0.4.0
Release: 1%{?dist}
License: MIT
URL: https://github.com/hamishforbes/lua-resty-consul
Source0: https://github.com/hamishforbes/lua-resty-consul/archive/refs/tags/v%{version}/lua-resty-consul-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: lua-resty-http
BuildRequires: luajit-resty-devel

%description
Library to interface with the consul HTTP API from ngx_lua.


%prep
%setup -q -n lua-resty-consul-%{version}


%build
# Lua only, nothing to see here


%install
mkdir -p %{buildroot}%{lua_pkgdir}/resty
cp -a lib/resty/* %{buildroot}%{lua_pkgdir}/resty/


%files
%license LICENSE
%doc README.md
%dir %{lua_pkgdir}/
%dir %{lua_pkgdir}/resty/
%{lua_pkgdir}/resty/consul.lua


%changelog
* Thu May 18 2023 Matthias Saou <matthias@saou.eu> 0.4.0-1
- Initial RPM release.

