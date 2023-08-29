Summary: Neighbor Proxy Daemon for IPv6
Name: npd6
Version: 1.1.0
Release: 4%{?dist}
License: GPLv3+
Group: System Environment/Daemons
URL: https://github.com/npd6/npd6
Source0: https://github.com/npd6/npd6/archive/%{version}/npd6-%{version}.tar.gz
Source1: npd6.service
Patch0: npd6-1.1.0-sysctl-removal.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc
BuildRequires: systemd
%{?systemd_requires}

%description
A daemon to provide a proxy service for IPv6 Neighbor Solicitations received
by a gateway routing device.


%prep
%setup -q
%patch0 -p1


%build
# The -c is required or the build fails, taken from the Makefile
# The -fcommon is required to fix link errors on el9+
make %{?_smp_mflags} CFLAGS="-c %{optflags} -fcommon"


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
* Tue Aug 29 2023 Matthias Saou <matthias@saou.eu> 1.1.0-4
- Add gcc BR.
- Include patch to remove obsolete sysctl include (removed from glibc 2.32).
- Compile with -fcommon to fix "multiple definition" ld errors.

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

