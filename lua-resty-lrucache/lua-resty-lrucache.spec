%global lua_version 5.1

Summary: Lua-land LRU cache based on the LuaJIT FFI
Name: lua-resty-lrucache
Version: 0.13
Release: 1%{?dist}
License: BSD
URL: https://github.com/openresty/lua-resty-lrucache
Source0: https://github.com/openresty/lua-resty-lrucache/archive/refs/tags/v%{version}/lua-resty-lrucache-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: luajit-resty-devel

%description
This library implements a simple LRU cache for the ngx_lua module.


%prep
%setup -q -n lua-resty-lrucache-%{version}


%build
# Lua only, nothing to see here


%install
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_pkgdir}


%files
%doc README.markdown
%dir %{lua_pkgdir}/
%dir %{lua_pkgdir}/resty/
%{lua_pkgdir}/resty/lrucache/
%{lua_pkgdir}/resty/lrucache.lua


%changelog
* Thu May 18 2023 Matthias Saou <matthias@saou.eu> 0.13-1
- Initial RPM release.

