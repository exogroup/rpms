%global lua_version 5.1

Summary: Memcached client driver for the ngx_lua nginx module
Name: lua-resty-memcached
Version: 0.17
Release: 1%{?dist}
License: BSD
URL: https://github.com/openresty/lua-resty-memcached
Source0: https://github.com/openresty/lua-resty-memcached/archive/refs/tags/v%{version}/lua-resty-memcached-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: lua-resty-core
BuildRequires: luajit-resty-devel

%description
This Lua library is a memcached client driver for the ngx_lua nginx module.


%prep
%setup -q -n lua-resty-memcached-%{version}


%build
# Lua only, nothing to see here


%install
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_pkgdir}


%files
%doc README.markdown
%dir %{lua_pkgdir}/
%dir %{lua_pkgdir}/resty/
%{lua_pkgdir}/resty/memcached.lua


%changelog
* Thu May 18 2023 Matthias Saou <matthias@saou.eu> 0.17-1
- Initial RPM release.

