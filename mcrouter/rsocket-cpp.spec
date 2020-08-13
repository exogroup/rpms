%global commit dd777b8eb153f5564ebaa0f068ebf227e0916e32
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: C++ implementation of RSocket
Name: rsocket-cpp
Version: 2019.09.04.00
Release: 1%{?shortcommit:.git.%{shortcommit}}%{?dist}
License: ASL 2.0
URL: https://github.com/rsocket/rsocket-cpp/tree/master/yarpl
Source0: https://github.com/rsocket/rsocket-cpp/archive/%{commit}/rsocket-cpp-%{shortcommit}.tar.gz
Patch0: rsocket-cpp-libdir.patch
BuildRequires: cmake
BuildRequires: folly-devel
BuildRequires: openssl-devel
BuildRequires: gflags-devel
BuildRequires: glog-devel
BuildRequires: libatomic
#BuildRequires: gmock-devel
#BuildRequires: gtest-devel

%description
C++ implementation of reactive functional programming including both Observable
and Flowable types.


%package devel
Summary: Yet Another Reactive Programming Library
Requires: %{name} = %{version}-%{release}

%description devel
C++ implementation of reactive functional programming including both Observable
and Flowable types.


%package -n yarpl
Summary: Yet Another Reactive Programming Library

%description -n yarpl
C++ implementation of reactive functional programming including both Observable
and Flowable types.


%package -n yarpl-devel
Summary: Yet Another Reactive Programming Library
Requires: yarpl = %{version}-%{release}

%description -n yarpl-devel
C++ implementation of reactive functional programming including both Observable
and Flowable types.


%prep
%setup -q -n rsocket-cpp-%{commit}
%patch0 -p1


%build
# rsocket-cpp
mkdir _build
cd _build
%cmake ..
%make_build
# yarpl
cd ../yarpl
mkdir _build
cd _build
# #869 Error for building the tests:
# The dependency target "gmock" of target "yarpl-tests" does not exist.
%cmake -DBUILD_TESTS=OFF ..
%make_build


%install
make -C _build install DESTDIR="%{buildroot}"
make -C yarpl/_build install DESTDIR="%{buildroot}"


%files
%license LICENSE
%doc README.md
%{_libdir}/libReactiveSocket.so

%files devel
%{_includedir}/rsocket/
%{_prefix}/lib/cmake/rsocket/


%files -n yarpl
%license LICENSE
%doc yarpl/README.md
%{_libdir}/libyarpl.so

%files -n yarpl-devel
%{_includedir}/yarpl/
%{_prefix}/lib/cmake/yarpl/


%changelog
* Wed Jul 29 2020 Matthias Saou <matthias@saou.eu> 2019.09.04.00-1
- Initial RPM release.

