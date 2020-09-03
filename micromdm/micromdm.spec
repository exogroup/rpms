%undefine _missing_build_ids_terminate_build

Name:       micromdm
Version:    1.6.0
Release:    1%{?dist}
Summary:    MicroMDM is a Mobile Device Management server for Apple Devices
#Group:      Applications/System
License:    MIT
URL:        https://github.com/micromdm/micromdm
Source0:    https://github.com/micromdm/micromdm/releases/download/v%{version}/micromdm_v%{version}.zip 
Source1:    micromdm.service
Source2:    micromdm.serviceenvironmentfile.conf
Requires(pre): shadow-utils
%{?systemd_requires}
BuildRequires: systemd

%description
Not a product!
MicroMDM is not a full featured device management product.
The mission of MicroMDM is to enable a secure and scalable MDM deployment for
Apple Devices, and expose the full set of Apple MDM commands and responses
through an API.
But it is more correct to think of MicroMDM as a lower level dependency for
one or more products, not a solution that lives on its own.

%prep
%setup -q -n build

%build

%install
mkdir -p %{buildroot}/opt/micromdm/bin/
mkdir -p %{buildroot}/opt/micromdm/db/
mkdir -p %{buildroot}/opt/micromdm/filerepo/
mkdir -p %{buildroot}/opt/micromdm/service/
install -D -p -m 0755 linux/micromdm %{buildroot}/opt/micromdm/bin/micromdm
install -D -p -m 0755 linux/mdmctl   %{buildroot}/opt/micromdm/bin/mdmctl
install -D -p -m 0644 micromdm.db    %{buildroot}/opt/micromdm/db/micromdm.db
install -D -p -m 0644 %{SOURCE2}     %{buildroot}/opt/micromdm/service/serviceenvironmentfile.conf
install -D -p -m 0644 %{SOURCE1}     %{buildroot}%{_unitdir}/micromdm.service 

%pre
getent group micromdm >/dev/null || groupadd -r micromdm
getent passwd micromdm >/dev/null || \
    useradd -r -g micromdm -d /opt/micromdm -s /sbin/nologin \
    -c "MicroMDM Server" micromdm
exit 0


%post
%systemd_post micromdm.service

%preun
%systemd_preun micromdm.service

%postun
%systemd_postun_with_restart micromdm.service

%files
%defattr(-,micromdm,micromdm,-)
%dir /opt/micromdm/
/opt/micromdm/bin/
%config(noreplace) /opt/micromdm/db/
%config(noreplace) /opt/micromdm/service/
/opt/micromdm/filerepo/
/opt/micromdm/bin/micromdm
/opt/micromdm/bin/mdmctl
%{_unitdir}/micromdm.service

%changelog
* Wed Aug 19 2020 Vincent Tamet <vincent.tamet@exoclick.com> - 1.6.0-1
- Initial release
