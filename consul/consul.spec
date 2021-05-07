%undefine _missing_build_ids_terminate_build

Summary: Tool for service discovery and configuration
Name: consul
Version: 1.9.5
Release: 1
License: MPLv2.0
URL: https://consul.io/
Source0: https://releases.hashicorp.com/consul/%{version}/consul_%{version}_linux_amd64.zip
Source1: consul.hcl.template
Source2: consul.service
Source3: consul.bash_completion
%{?systemd_requires}

%description
Distributed, highly available, and data center aware solution to connect and
configure applications across dynamic, distributed infrastructure.


%prep
%setup -q -c


%build
# Single go binary...


%install
install -D -p -m 0755 consul %{buildroot}%{_bindir}/consul
install -D -p -m 0644 %{SOURCE1} consul.hcl.template
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/consul.service
install -D -p -m 0644 %{SOURCE3} %{buildroot}/etc/bash_completion.d/consul
mkdir -p %{buildroot}/etc/{consul.d,sysconfig}
touch %{buildroot}/etc/sysconfig/consul
mkdir -p %{buildroot}/var/lib/consul


%pre
getent group consul >/dev/null || groupadd -r consul
getent passwd consul >/dev/null || \
  useradd -r -d /var/lib/consul -g consul \
  -s /sbin/nologin -c "Consul" consul

%post
%systemd_post consul.service

%preun
%systemd_preun consul.service

%postun
%systemd_postun_with_restart consul.service


%files
%doc consul.hcl.template
/etc/bash_completion.d/consul
%attr(0750,root,consul) %config %dir /etc/consul.d
%ghost %config /etc/sysconfig/consul
%{_bindir}/consul
%{_unitdir}/consul.service
%attr(0750,consul,consul) %dir /var/lib/consul


%changelog
* Fri May  7 2021 Matthias Saou <matthias@saou.eu> 1.9.5-1
- Update to 1.9.5.

* Fri Feb  5 2021 Matthias Saou <matthias@saou.eu> 1.9.3-1
- Update to 1.9.3.

* Mon Aug 31 2020 Matthias Saou <matthias@saou.eu> 1.8.3-1
- Update to 1.8.3.

* Wed Aug 12 2020 Matthias Saou <matthias@saou.eu> 1.8.2-1
- Update to 1.8.2.

* Thu Jul  2 2020 Matthias Saou <matthias@saou.eu> 1.8.0-4
- Include /etc/sysconfig/consul %%ghost file, for service env vars.

* Wed Jul  1 2020 Matthias Saou <matthias@saou.eu> 1.8.0-3
- Update to 1.8.0.
- Don't include template in config dir, as %%doc instead.

* Sun May 10 2020 Matthias Saou <matthias@saou.eu> 1.7.3-1
- Update to 1.7.3.

* Thu May 07 2020 Matthias Saou <matthias@saou.eu> 1.7.2-1
- Initial RPM release.

