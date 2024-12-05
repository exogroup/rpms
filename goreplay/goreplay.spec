Name: goreplay
Version: 1.3.3
Release: 1
Summary: Network monitoring tool to record and replay live traffic
License: LGPLv3
URL: https://github.com/buger/goreplay
Source0: https://github.com/buger/goreplay/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source1: prep-packages.sh
BuildRequires: golang
BuildRequires: libpcap-devel

%description
GoReplay is an open-source network monitoring tool which can record your live
traffic and use it for shadowing, load testing, monitoring and detailed
analysis.


%prep
%setup -q


%build
%gobuild -o gor .


%install
install -D -p -m 0755 gor %{buildroot}%{_bindir}/gor


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/gor


%changelog
* Thu Dec  5 2024 Matthias Saou <matthias@saou.eu> 1.3.3-1
- Initial RPM release
- Upstream rpm is in /usr/local not in root's $PATH, and no aarch64.

