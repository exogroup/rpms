Name:       journal-triggerd
Version:    0.2.1
Release:    2%{?dist}
Summary:    Triggers on journal messages

License:    GPLv3+
URL:        https://jjacky.com/journal-triggerd/
Source0:    https://jjacky.com/journal-triggerd/journal-triggerd-%{version}.tar.gz
Source1:    journal-triggerd.service

BuildRequires:  gcc
BuildRequires:  systemd-devel
BuildRequires:  glib2-devel

%description
journal-triggerd is a small daemon that runs in the background, listening to
systemd's journal, and will run "triggers" (i.e. exec a command line) when
certain messages are added.

You can define which messages to listen for, and what to run when such
messages are added to the journal, by defining simple text file rules.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/usr/share/doc/journal-triggerd
install -p -D -m 0644 %{SOURCE1} \
    %{buildroot}%{_unitdir}/journal-triggerd.service


%pre
getent group journal-trigger >/dev/null || groupadd -r journal-trigger
getent passwd journal-trigger >/dev/null || \
    useradd -r -g journal-trigger -G systemd-journal -d / -s /sbin/nologin \
    -c "journal-trigger User Daemon" journal-trigger
exit 0

%post
%systemd_post journal-triggerd.service

%preun
%systemd_preun journal-triggerd.service

%postun
%systemd_postun_with_restart journal-triggerd.service


%files
%doc AUTHORS HISTORY README.md
%license COPYING
%dir /etc/journal-triggerd.rules
%{_bindir}/journal-triggerd
%{_mandir}/man1/journal-triggerd.*
%{_unitdir}/journal-triggerd.service


%changelog
* Tue Jun 28 2022 Matthias Saou <matthias@saou.eu> 0.2.1-2
- Add missing gcc build requirement.

* Mon Jul 31 2017 - David Castañeda <david.castaneda@exoclick.com> 0.2.1-1
- Initial RPM release.

