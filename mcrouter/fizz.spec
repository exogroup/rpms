%global commit 979b09dbcd0344890692582d4fb5cb97bc7ab21e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: TLS 1.3 implementation
Name: fizz
Version: 2019.11.04.00
Release: 1%{?shortcommit:.git.%{shortcommit}}%{?dist}
License: ASL 2.0
URL: https://github.com/facebookincubator/fizz
Source0: https://github.com/facebookincubator/fizz/archive/%{commit}/fizz-%{shortcommit}.tar.gz
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: folly-devel
BuildRequires: openssl-devel
BuildRequires: glog-devel
BuildRequires: double-conversion-devel
BuildRequires: libsodium-devel
BuildRequires: gflags-devel
BuildRequires: libevent-devel
BuildRequires: gmock-devel
BuildRequires: gtest-devel

%description
Fizz currently supports TLS 1.3 drafts 28, 26 (both wire-compatible with the
final specification), and 23. All major handshake modes are supported,
including PSK resumption, early data, client authentication, and
HelloRetryRequest.


%package libs
Summary: TLS 1.3 implementation

%description libs
Fizz currently supports TLS 1.3 drafts 28, 26 (both wire-compatible with the
final specification), and 23. All major handshake modes are supported,
including PSK resumption, early data, client authentication, and
HelloRetryRequest.


%package devel
Summary: TLS 1.3 implementation
Requires: %{name}-libs = %{version}-%{release}
Requires: folly-devel
Requires: openssl-devel
Requires: libsodium-devel

%description devel
Fizz currently supports TLS 1.3 drafts 28, 26 (both wire-compatible with the
final specification), and 23. All major handshake modes are supported,
including PSK resumption, early data, client authentication, and
HelloRetryRequest.


%prep
%setup -q -n fizz-%{commit}


%build
%cmake fizz
%make_build


%install
make install DESTDIR="%{buildroot}"
install -D -m 0755 bin/fizz %{buildroot}%{_bindir}/fizz


%check
ctest


%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{_bindir}/fizz

%files libs
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/fizz/
%{_prefix}/lib/cmake/fizz/
%{_prefix}/lib/libfizz_test_support.so
%{_libdir}/*.so


%changelog
* Wed Jul 29 2020 Matthias Saou <matthias@saou.eu> 2019.11.04.00-1
- Initial RPM release.

