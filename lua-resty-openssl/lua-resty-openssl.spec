%global lua_version 5.1

Summary: Lua FFI-based OpenSSL binding library for ngx_lua
Name: lua-resty-openssl
Version: 1.5.1
Release: 1%{?dist}
License: BSD
URL: https://github.com/fffonion/lua-resty-openssl
Source0: https://github.com/fffonion/lua-resty-openssl/archive/refs/tags/%{version}/lua-resty-openssl-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: lua-resty-core
BuildRequires: make
BuildRequires: luajit-resty-devel

%description
Lua FFI-based OpenSSL binding library for ngx_lua.


%prep
%setup -q


%build
# Lua only, nothing to see here


%install
mkdir -p %{buildroot}%{lua_pkgdir}/resty
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_pkgdir}


%files
%doc README.md
%dir %{lua_pkgdir}/
%dir %{lua_pkgdir}/resty/
%{lua_pkgdir}/resty/openssl/
%{lua_pkgdir}/resty/openssl.lua


%changelog
* Tue Dec  3 2024 Matthias Saou <matthias@saou.eu> 1.5.1-1
- Update to 1.5.1.

* Fri Apr 05 2024 Michele Brodoloni <michele@exads.com> - 1.2.1-1
- Initial RPM release.

