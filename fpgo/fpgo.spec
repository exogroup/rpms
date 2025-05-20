%global daemon_name fpgo

Name: fpgo
Version: 1.1.6
Release: 2
Summary: Fasthttp forward proxy
License: Public Domain
URL: https://github.com/app-fast/fpgo/
# Created by prep-packages.sh
Source0: fpgo-%{version}.tar.gz
Source1: fpgo.service
Source2: fpgo.sysconfig
Source99: prep-packages.sh
BuildRequires: golang
# For DynamicUser= support
BuildRequires: systemd >= 232
%{?systemd_requires}
Patch0: fpgo-1.1.6-ipv6.patch

%description
Fasthttp forward proxy.


%prep
%setup -q
%autopatch


%build
%gobuild -o fpgo .


%install
install -m 0755 -D fpgo %{buildroot}%{_bindir}/fpgo
install -D -p -m 0644 %{SOURCE1} \
  %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 0644 %{SOURCE2} \
  %{buildroot}/etc/sysconfig/fpgo


%post
%systemd_post %{daemon_name}.service

%preun
%systemd_preun %{daemon_name}.service

%postun
%systemd_postun_with_restart %{daemon_name}.service


%files
%doc ReadMe.md
%config(noreplace) /etc/sysconfig/fpgo
%{_bindir}/fpgo
%{_unitdir}/%{daemon_name}.service


%changelog
* Tue May  6 2025 Matthias Saou <matthias@saou.eu> 1.1.6-2
- Include IPv6 patch.

* Tue May  6 2025 Matthias Saou <matthias@saou.eu> 1.1.6-1
- Update to 1.1.6.

* Tue Mar 25 2025 Matthias Saou <matthias@saou.eu> 1.1.4-1
- Update to 1.1.4.

* Tue Oct  3 2023 Matthias Saou <matthias@saou.eu> 0.2.1-1
- Initial RPM release.

