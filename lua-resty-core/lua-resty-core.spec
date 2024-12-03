%global lua_version 5.1

Summary: FFI-based Lua API for the lua nginx module
Name: lua-resty-core
Version: 0.1.30
Release: 1%{?dist}
License: BSD
URL: https://github.com/openresty/lua-resty-core
Source0: https://github.com/openresty/lua-resty-core/archive/refs/tags/v%{version}/lua-resty-core-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: lua-resty-lrucache
BuildRequires: make
BuildRequires: luajit-resty-devel

%description
This pure Lua library reimplements part of the ngx_lua module's Nginx API for
Lua with LuaJIT FFI and installs the new FFI-based Lua API into the ngx.* and
ndk.* namespaces used by the ngx_lua module.


%prep
%setup -q -n lua-resty-core-%{version}


%build
# Lua only, nothing to see here


%install
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_pkgdir}


%files
%doc README.markdown
%dir %{lua_pkgdir}/
%{lua_pkgdir}/ngx/
%{lua_pkgdir}/resty/


%changelog
* Tue Dec  3 2024 Matthias Saou <matthias@saou.eu> 0.1.30-1
- Update to 0.1.30.

* Thu May 18 2023 Matthias Saou <matthias@saou.eu> 0.1.26-1
- Initial RPM release.

