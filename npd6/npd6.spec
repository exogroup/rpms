Summary: Neighbor Proxy Daemon for IPv6
Name: npd6
Version: 1.1.0
Release: 3%{?dist}
License: GPLv3+
Group: System Environment/Daemons
URL: https://github.com/npd6/npd6
Source0: https://github.com/npd6/npd6/archive/%{version}.tar.gz
Source1: npd6.service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: systemd
%{?systemd_requires}

%description
A daemon to provide a proxy service for IPv6 Neighbor Solicitations received
by a gateway routing device.


%prep
%setup -q


%build
# The -c is required or the build fails, taken from the Makefile
make %{?_smp_mflags} CFLAGS="-c %{optflags}"


%install
make install INSTALL_PREFIX=%{_prefix} DESTDIR=%{buildroot}
# Put the sample entirely into place
mv %{buildroot}%{_sysconfdir}/npd6.conf.sample \
   %{buildroot}%{_sysconfdir}/npd6.conf
# Remove old init script (avoid unpackaged files error)
rm -f %{buildroot}%{_sysconfdir}/init.d/npd6
# Create systemd unit file
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/npd6.service


%post
%systemd_post npd6.service

%preun
%systemd_preun npd6.service

%postun
%systemd_postun_with_restart npd6.service


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/npd6.conf
%{_bindir}/npd6
%{_unitdir}/npd6.service
%{_mandir}/man5/npd6.conf.5*
%{_mandir}/man8/npd6.8*


%changelog
* Wed Aug 11 2021 Matthias Saou <matthias@saou.eu> 1.1.0-3
- Fix service file's missing Install section.

* Tue Mar 17 2020 Matthias Saou <matthias@saou.eu> 1.1.0-2
- Minor cleanups.

* Mon Mar 16 2020 Michele Brodoloni <michele@exads.com> - 1.1.0-1
- Change to systemd service.

* Tue Jul 14 2015 Matthias Saou <matthias@saou.eu> 1.1.0-1
- Update to 1.1.0.

* Tue Jul 17 2012 Matthias Saou <matthias@saou.eu> 0.4.6-1
- Initial RPM release.

