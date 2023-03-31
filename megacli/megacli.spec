%define debug_package %{nil}
%define version_dot 8.07.14
%define version_dash 8-07-14

Summary: LSI Logic MegaCLI
Name: megacli
Version: 8.07.14
Release: 1
License: Proprietary
Group: System Environment/Base
URL: https://www.broadcom.com/products/storage/raid-controllers
Source0: https://docs.broadcom.com/docs-and-downloads/raid-controllers/raid-controllers-common-files/%{version_dash}_MegaCLI.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires: dos2unix
ExclusiveArch: %{ix86} x86_64
Obsoletes: MegaCli <= 1.01.24-0
Provides: MegaCli = %{version}-%{release}

%description
LSI Logic / Avago / Broadcom MegaCLI.


%prep
%setup -q -c
# We have an rpm inside a zip...
rpm2cpio Linux/MegaCli-%{version}-1.noarch.rpm | cpio -dim
# Convert from iso8859-1/dos to utf-8/unix
iconv -f iso8859-1 -t utf-8 -o tmp %{version}_MegaCLI.txt
dos2unix tmp
mv tmp MegaCli.txt


%build


%install
rm -rf %{buildroot}
%ifarch %{ix86}
install -p -D -m 0755 opt/MegaRAID/MegaCli/MegaCli \
    %{buildroot}%{_sbindir}/MegaCli
%endif
%ifarch x86_64
install -p -D -m 0755 opt/MegaRAID/MegaCli/MegaCli64 \
    %{buildroot}%{_sbindir}/MegaCli
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc MegaCli.txt
%{_sbindir}/MegaCli


%changelog
* Fri Mar 31 2023 Matthias Saou <matthias@saou.eu> 8.07.14-1
- Update to 8.07.14 ... from 2014. Yes, storcli is the way to go!

* Mon Apr 11 2011 Matthias Saou <http://freshrpms.net/> 8.00.46-2
- Update to 8.00.46.
- Remove bigbrother script and egwn readme about how to enable it : puppet!
- Include the libsysfs.so.2.0.2 in /opt/lsi since the tool complains otherwise.

* Wed Jun  9 2010 Matthias Saou <http://freshrpms.net/> 4.00.11-1
- Update to 4.00.11.

* Fri Feb 29 2008 Matthias Saou <http://freshrpms.net/> 1.01.40-2
- Include bigbrother monitoring script and README.egwn file.

* Fri Feb  1 2008 Matthias Saou <http://freshrpms.net/> 1.01.40-1
- Update to 1.01.40.

* Thu Jan 24 2008 Matthias Saou <http://freshrpms.net/> 1.01.39-1
- Update to 1.01.39.
- We now have a native 64bit binary, yeah!

* Wed Sep 12 2007 Matthias Saou <http://freshrpms.net/> 1.01.24-1
- Initial RPM release.

