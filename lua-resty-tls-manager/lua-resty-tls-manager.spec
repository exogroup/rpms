%global lua_version 5.1

Summary: Library to automatically provide SSL certificate files
Name: lua-resty-tls-manager
Version: 0.3.1
Release: 1%{?dist}
License: BSD
URL: https://github.com/exogroup/lua-resty-tls-manager
Source0: https://github.com/exogroup/lua-resty-tls-manager/archive/refs/tags/v%{version}/lua-resty-tls-manager-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: lua-resty-core
BuildRequires: make
BuildRequires: luajit-resty-devel

%description
Library to automatically provide SSL certificate files.

%prep
%setup -q


%build
# Lua only, nothing to see here


%install
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_pkgdir}


%files
%doc README.md
%dir %{lua_pkgdir}/
%dir %{lua_pkgdir}/resty/
%dir %{lua_pkgdir}/resty/tls_manager/
%dir %{lua_pkgdir}/resty/tls_manager/strategy/
%{lua_pkgdir}/resty/*.lua
%{lua_pkgdir}/resty/tls_manager/*.lua
%{lua_pkgdir}/resty/tls_manager/strategy/*.lua

%changelog
* Thu May 02 2024 Michele Brodoloni <michele@exads.com> - 0.3.1-1
- Update to v0.3.1

* Thu May 02 2024 Michele Brodoloni <michele@exads.com> - 0.3.0-1
- Update to v0.3.0

* Tue Apr 16 2024 Michele Brodoloni <michele@exads.com> - 0.2.0-1
- Update to v0.2.0

* Tue Apr 09 2024 Michele Brodoloni <michele@exads.com> - 0.1.0-1
- Initial release


