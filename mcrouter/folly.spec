%global commit b35bea8f0784806e687e32f6914f4a504785ea06
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Facebook Open Source Library
Name: folly
Version: 2019.11.04.00
Release: 1%{?shortcommit:.git.%{shortcommit}}%{?dist}
License: ASL 2.0
URL: https://github.com/facebook/folly
Source0: https://github.com/facebook/folly/archive/%{commit}/folly-%{shortcommit}.tar.gz
BuildRequires: cmake
BuildRequires: gflags-devel
BuildRequires: glog-devel
BuildRequires: libevent-devel
BuildRequires: openssl-devel
BuildRequires: boost-devel
BuildRequires: double-conversion-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel
BuildRequires: lz4-devel
BuildRequires: libzstd-devel
BuildRequires: snappy-devel
BuildRequires: libdwarf-devel
BuildRequires: binutils-devel
BuildRequires: libaio-devel
BuildRequires: liburing-devel
BuildRequires: libsodium-devel
BuildRequires: fmt-devel
BuildRequires: jemalloc-devel
BuildRequires: libunwind-devel
BuildRequires: automake

%description
Folly (acronymed loosely after Facebook Open Source Library) is a library of
C++14 components designed with practicality and efficiency in mind.
Folly contains a variety of core library components used extensively at
Facebook. In particular, it's often a dependency of Facebook's other open
source C++ efforts and place where those projects can share code.


%package devel
Summary: Facebook Open Source Library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gflags-devel
Requires: glog-devel
Requires: libevent-devel
Requires: openssl-devel
Requires: boost-devel
Requires: double-conversion-devel
Requires: zlib-devel
Requires: bzip2-devel
Requires: xz-devel
Requires: lz4-devel
Requires: libzstd-devel
Requires: snappy-devel
Requires: libdwarf-devel
Requires: binutils-devel
Requires: libaio-devel
Requires: liburing-devel
Requires: libsodium-devel
Requires: fmt-devel
Requires: jemalloc-devel
Requires: libunwind-devel

%description devel
Folly (acronymed loosely after Facebook Open Source Library) is a library of
C++14 components designed with practicality and efficiency in mind.
Folly contains a variety of core library components used extensively at
Facebook. In particular, it's often a dependency of Facebook's other open
source C++ efforts and place where those projects can share code.


%prep
%setup -q -n folly-%{commit}


%build
# #833 -fPIC error
%cmake -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON .
%make_build


%install
make install DESTDIR="%{buildroot}"
# Fix bogus include path presence that causes issues later on
sed -i -e 's|;//include||g' \
  %{buildroot}%{_prefix}/lib/cmake/folly/folly-targets.cmake


%files
%license LICENSE
%doc CONTRIBUTING.md README.md
%{_libdir}/*.so

%files devel
%{_includedir}/folly/
%{_prefix}/lib/cmake/folly/
%{_libdir}/pkgconfig/libfolly.pc


%changelog
* Wed Jul 29 2020 Matthias Saou <matthias@saou.eu> 2019.11.04.00-1
- Initial RPM release.

