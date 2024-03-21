%global commit d40ec77e960d021861220bc14a273c5dcad13160
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Dump unix domain socket traffic
Name: sockdump
Version: 0.0
Release: 1.%{shortcommit}%{?dist}
License: Unlicense
URL: https://github.com/mechpen/sockdump
Source0: https://github.com/mechpen/sockdump/archive/%{commit}/sockdump-%{version}-%{shortcommit}.tar.gz
Requires: python3-bcc
BuildArch: noarch

%description
Dump unix domain socket traffic.
Supports STREAM and DGRAM types.


%prep
%setup -q -n sockdump-%{commit}


%build


%install
install -p -m 0755 -D sockdump.py %{buildroot}%{_sbindir}/sockdump


%files
%license LICENSE
%doc README.md
%{_sbindir}/sockdump


%changelog
* Thu Mar 21 2024 Matthias Saou <matthias@saou.eu> 0.0-1.d40ec77
- Initial RPM release.

