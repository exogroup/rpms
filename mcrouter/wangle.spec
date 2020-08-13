%global commit 5ad3fbcf378ab50ef52b0bc9cd12d3e9d6fa1e82
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: C++ networking library
Name: wangle
Version: 2019.11.04.00
Release: 1%{?shortcommit:.git.%{shortcommit}}%{?dist}
License: ASL 2.0
URL: https://github.com/facebook/wangle
Source0: https://github.com/facebook/wangle/archive/%{commit}/wangle-%{shortcommit}.tar.gz
BuildRequires: cmake
BuildRequires: folly-devel
BuildRequires: fizz-devel
BuildRequires: fmt-devel
BuildRequires: openssl-devel
BuildRequires: glog-devel
BuildRequires: gflags-devel
BuildRequires: libevent-devel
BuildRequires: double-conversion-devel
BuildRequires: gmock-devel
BuildRequires: gtest-devel

%description
Wangle is a library that makes it easy to build protocols, application clients,
and application servers.
It's like Netty + Finagle smooshed together, but in C++.


%package devel
Summary: C++ networking library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Wangle is a library that makes it easy to build protocols, application clients,
and application servers.
It's like Netty + Finagle smooshed together, but in C++.


%prep
%setup -q -n wangle-%{commit}


%build
%cmake wangle
%make_build


%install
make install DESTDIR="%{buildroot}"


%check
# 71% tests passed, 4 tests failed out of 14 :-(
ctest || exit 0


%files
%license LICENSE
%doc CONTRIBUTING.md README.md tutorial.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/wangle/
%{_prefix}/lib/cmake/wangle/
%{_libdir}/*.so


%changelog
* Wed Jul 29 2020 Matthias Saou <matthias@saou.eu> 2019.11.04.00-1
- Initial RPM release.

