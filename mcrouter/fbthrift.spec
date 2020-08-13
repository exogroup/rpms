%global commit 6d6f6b8dd7d3333690e78e27b4c68ff7a55614df
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Serialization and RPC framework for service communication
Name: fbthrift
Version: 2019.11.04.00
Release: 1%{?shortcommit:.git.%{shortcommit}}%{?dist}
License: ASL 2.0
URL: https://github.com/facebook/fbthrift
Source0: https://github.com/facebook/fbthrift/archive/%{commit}/fbthrift-%{shortcommit}.tar.gz
BuildRequires: cmake
BuildRequires: openssl-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: gflags-devel
BuildRequires: glog-devel
BuildRequires: boost-devel
BuildRequires: folly-devel
BuildRequires: fizz-devel
BuildRequires: wangle-devel
BuildRequires: zlib-devel
BuildRequires: libzstd-devel
BuildRequires: fmt-devel
BuildRequires: yarpl-devel
BuildRequires: rsocket-cpp-devel
# FIXME: Not working...
#  By not providing "Findpython-six.cmake" in CMAKE_MODULE_PATH this project
#  has asked CMake to find a package configuration file provided by
#  "python-six", but CMake did not find one.
#BuildRequires: python3-six
#BuildRequires: python3-Cython

%description
Thrift is a serialization and RPC framework for service communication. Thrift
enables these features in all major languages, and there is strong support for
C++, Python, Hack, and Java. Most services at Facebook are written using Thrift
for RPC, and some storage systems use Thrift for serializing records on disk.


%package devel
Summary: Serialization and RPC framework for service communication
Requires: %{name} = %{version}-%{release}
Requires: openssl-devel
Requires: boost-devel
Requires: fmt-devel
Requires: glog-devel
Requires: libzstd-devel
Requires: wangle-devel
Requires: yarpl-devel
Requires: rsocket-cpp-devel

%description devel
Thrift is a serialization and RPC framework for service communication. Thrift
enables these features in all major languages, and there is strong support for
C++, Python, Hack, and Java. Most services at Facebook are written using Thrift
for RPC, and some storage systems use Thrift for serializing records on disk.


%prep
%setup -q -n fbthrift-%{commit}


%build
%cmake .
%make_build


%install
make install DESTDIR="%{buildroot}"


%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{_bindir}/thrift1
%{_libdir}/*.so

%files devel
%{_includedir}/thrift/
%{_prefix}/lib/cmake/fbthrift/


%changelog
* Wed Jul 29 2020 Matthias Saou <matthias@saou.eu> 2019.11.04.00-1
- Initial RPM release.

