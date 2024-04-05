%global lua_version 5.1

Summary: Lua FFI-based OpenSSL binding library for ngx_lua
Name: lua-resty-openssl
Version: 1.2.1
Release: 1%{?dist}
License: BSD
URL: https://github.com/fffonion/lua-resty-openssl
Source0: https://github.com/fffonion/lua-resty-openssl/archive/refs/tags/%{version}/lua-resty-openssl-%{version}.tar.gz
Patch0: Makefile.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: lua-resty-core
BuildRequires: luajit-resty-devel

%description
Lua FFI-based OpenSSL binding library for ngx_lua.


%prep
%setup -q -n lua-resty-openssl-%{version}
%patch -P 0 -p1

%build
# Lua only, nothing to see here


%install
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_pkgdir}


%files
%doc README.md
%dir %{lua_pkgdir}/
%dir %{lua_pkgdir}/resty/
%dir %{lua_pkgdir}/resty/openssl/
%{lua_pkgdir}/resty/openssl.lua
%{lua_pkgdir}/resty/openssl/*.lua


%changelog
* Fri Apr 05 2024 Michele Brodoloni <michele@exads.com> - 1.2.1-1
- Initial RPM release.

