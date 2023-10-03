%global daemon_name fpgo

Name: fpgo
Version: 0.2.1
Release: 1
Summary: Fasthttp forward proxy
License: Public Domain
URL: https://github.com/joeky888/fpgo
# Created by prep-packages.sh
Source0: fpgo-%{version}.tar.gz
Source1: fpgo.service
Source2: fpgo.sysconfig
Source99: prep-packages.sh
BuildRequires: golang
# For DynamicUser= support
BuildRequires: systemd >= 232
%{?systemd_requires}

%description
Fasthttp forward proxy.


%prep
%setup -q


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
* Tue Oct  3 2023 Matthias Saou <matthias@saou.eu> 0.2.1-1
- Initial RPM release.

