%define debug_package %{nil}

Summary: LSI Logic MegaCLI
Name: megacli
Version: 8.00.46
Release: 2
License: Proprietary
Group: System Environment/Base
URL: http://www.lsilogic.com/
Source0: http://www.lsi.com/DistributionSystem/AssetDocument/%{version}_Linux_MegaCLI.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires: dos2unix
ExclusiveArch: %{ix86} x86_64
Obsoletes: MegaCli <= 1.01.24-0
Provides: MegaCli = %{version}-%{release}

%description
LSI Logic MegaCLI.


%prep
%setup -q -c
# The same readme.txt is inside the following zip...
rm -f readme.txt
# We have rpms inside a zip inside a zip...
unzip MegaCliLin.zip
rpm2cpio MegaCli-%{version}-1.i386.rpm | cpio -dim
rm -f readme.txt
rpm2cpio Lib_Utils-*.noarch.rpm | cpio -dim
# Convert from iso8859-1/dos to utf-8/unix
iconv -f iso8859-1 -t utf-8 -o tmp %{version}_Linux_MegaCLI.txt
dos2unix tmp
mv tmp MegaCli.txt


%build


%install
rm -rf %{buildroot}
%ifarch %{ix86}
install -p -D -m 0755 opt/MegaRAID/MegaCli/MegaCli \
    %{buildroot}%{_sbindir}/MegaCli
install -p -D -m 0755 opt/lsi/3rdpartylibs/libsysfs.so.2.0.2 \
    %{buildroot}/opt/lsi/3rdpartylibs/libsysfs.so.2.0.2
%endif
%ifarch x86_64
install -p -D -m 0755 opt/MegaRAID/MegaCli/MegaCli64 \
    %{buildroot}%{_sbindir}/MegaCli
install -p -D -m 0755 opt/lsi/3rdpartylibs/x86_64/libsysfs.so.2.0.2 \
    %{buildroot}/opt/lsi/3rdpartylibs/x86_64/libsysfs.so.2.0.2
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc MegaCli.txt
%{_sbindir}/MegaCli
/opt/lsi


%changelog
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

