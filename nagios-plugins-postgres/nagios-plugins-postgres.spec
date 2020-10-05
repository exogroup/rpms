Name:      nagios-plugins-postgres
Version:   2.25.0
Release:   1%{?dist}
Summary:   Provides check_postgres support for Nagios.
Group:     Applications/System
License:   BSD
URL:       https://bucardo.org/wiki/Check_postgres
Source0:   https://bucardo.org/downloads/check_postgres-%{version}.tar.gz
Patch0:    nagios-plugins-postgres-disable_no_psql_option.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:  nagios-plugins
Requires:  perl(Data::Dumper)
Requires:  perl(DateTime::Format::DateParse)
Requires:  perl(Digest::MD5)
BuildArch: noarch


%description
Provides check_postgres support for Nagios.


%prep
%setup -q -n check_postgres-%{version}
%patch0 -p1


%install
rm -rf %{buildroot}
install -D -p -m 0755 check_postgres.pl \
  %{buildroot}%{_libdir}/nagios/plugins/check_postgres


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md TODO
%{_libdir}/nagios/plugins/check_postgres


%changelog
* Mon Oct  5 2020 Matthias Saou <matthias@saou.eu> 2.25.0-1
- Update to 2.25.0.

* Tue Nov 07 2017 Michał Lisowski <michal@exads.com> - 2.23.0-1
- Update to 2.23.0 with postgresql 10.0 support

* Fri Oct 02 2015 Michal Lisowski <michal@exads.com> - 2.22.0-3
- Add R: perl(Digest::MD5) needed by some actions

* Mon Sep 28 2015 Matthias Saou <matthias@saou.eu> 2.22.0-2
- Remove .pl extension from plugin script for consistency.

* Fri Sep 25 2015 Michal Lisowski <michal@exads.com> - 2.22.0-1
- Initial RPM release

