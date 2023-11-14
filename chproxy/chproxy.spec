Summary: ClickHouse http proxy and load balancer
Name: chproxy
Version: 1.25.0
Release: 1
License: MIT
URL: https://github.com/Vertamedia/chproxy
Source0: https://github.com/ContentSquare/chproxy/releases/download/v%{version}/chproxy_%{version}_linux_amd64.tar.gz
Source1: https://raw.githubusercontent.com/Vertamedia/chproxy/master/config/examples/simple.yml
Source2: chproxy.service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
ExclusiveArch: x86_64
%{?systemd_requires}

%description
Chproxy, is an http proxy and load balancer for ClickHouse database.


%prep
%setup -q -c


%build
# Nothing to see here...


%install
rm -rf %{buildroot}
install -D -p -m 0755 chproxy %{buildroot}/usr/bin/chproxy
install -D -p -m 0640 %{SOURCE1} %{buildroot}/etc/chproxy.yml
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/chproxy.service


%pre
getent group chproxy >/dev/null || groupadd -r chproxy
getent passwd chproxy >/dev/null || \
  useradd -r -d /var/lib/chproxy -g chproxy \
  -s /sbin/nologin -c "ClickHouse Proxy" chproxy

%post
%systemd_post chproxy.service

%preun
%systemd_preun chproxy.service

%postun
%systemd_postun_with_restart chproxy.service


%files
%config(noreplace) %attr(0640,root,chproxy) /etc/chproxy.yml
/usr/bin/chproxy
%{_unitdir}/chproxy.service


%changelog
* Tue Nov 14 2023 Matthias Saou <matthias@saou.eu> 1.25.0-1
- Update to 1.25.0.

* Tue Oct  4 2022 Matthias Saou <matthias@saou.eu> 1.17.2-1
- Update to 1.17.2.
- Update source URL.

* Wed Sep  9 2020 Matthias Saou <matthias@saou.eu> 1.14.0-1
- Update to 1.14.0.
- Drop dist tag, as binaries aren't dist-specific.
- Update/fix source URL.
- Enable debuginfo package (not sure why it was disabled).

* Fri Oct 19 2018 Alfred Dobradi <alfred@exads.com> - 1.13.0-2
- Add ExecReload to service

* Thu Oct 04 2018 Michał Lisowski <michal@exads.com> - 1.13.0-1
- Update to 1.13.0

* Tue Jul 24 2018 Matthias Saou <matthias@saou.eu> 1.12.0-1
- Initial RPM release.

