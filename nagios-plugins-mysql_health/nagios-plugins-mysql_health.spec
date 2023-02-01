Summary: Provides check_mysql_health support for Nagios
Name: nagios-plugins-mysql_health
Version: 2.2.2
Release: 2%{?dist}
License: GPLv2
Group: Applications/System
URL: https://labs.consol.de/nagios/check_mysql_health/
Source0: https://labs.consol.de/assets/downloads/nagios/check_mysql_health-%{version}.tar.gz
Patch0: check_mysql_health-2.1.3-querycache_hitrate_thresholds.patch
Patch1: check_mysql_health-2.1.3-myisam_keycache_hitrate_thresholds.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: nagios-plugins
Requires: perl(DBD::mysql)
BuildRequires: perl-generators
BuildRequires: perl(DBD::mysql)
BuildArch: noarch

%description
Provides check_mysql_health support for Nagios.


%prep
%setup -q -n check_mysql_health-%{version}
%patch0 -p1
%patch1 -p1


%build
%configure \
  --libexecdir=%{_libdir}/nagios/plugins \
  --with-mymodules-dir=%{_libdir}/nagios/plugins/check_mysql_health-data \
  --with-mymodules-dyn-dir=%{_libdir}/nagios/plugins/check_mysql_health-data
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_libdir}/nagios/plugins/check_mysql_health


%changelog
* Wed Feb  1 2023 Matthias Saou <matthias@saou.eu> 2.2.2-2
- Update URL and Source0. This is the twos.

* Thu Nov 14 2019 Matthias Saou <matthias@saou.eu> 2.2.2-1
- Update to 2.2.2.

* Tue Sep 29 2015 Matthias Saou <matthias@saou.eu> 2.2.1-1
- Update to 2.2.1.

* Mon Sep  8 2014 Matthias Saou <matthias@saou.eu> 2.1.8.2-2
- Change libexec dir to lib dir to match Fedora/EPEL (ugly, but I'm tired).

* Thu Apr 11 2013 Matthias Saou <matthias@saou.eu> 2.1.8.2-1
- Update to 2.1.8.2.

* Wed Dec 28 2011 Matthias Saou <matthias@saou.eu> 2.1.7-1
- Update to 2.1.7.

* Tue Dec  7 2010 Matthias Saou <http://freshrpms.net/> 2.1.3-3
- Add myisam_keycache_hitrate_thresholds patch to avoid useless alarms.

* Mon Nov 22 2010 Matthias Saou <http://freshrpms.net/> 2.1.3-2
- Add querycache_hitrate_thresholds patch (EGWN #2595).

* Wed Oct 13 2010 Matthias Saou <http://freshrpms.net/> 2.1.3-1
- Update to 2.1.3, which includes open files check.

* Wed Aug 25 2010 Matthias Saou <http://freshrpms.net/> 2.1.2-1
- Initial RPM release.

