%undefine _missing_build_ids_terminate_build

Name:       micromdm
Version:    1.9.0
Release:    1%{?dist}
Summary:    API focused Mobile Device Management server for Apple Devices
License:    MIT
URL:        https://github.com/micromdm/micromdm
Source0:    https://github.com/micromdm/micromdm/releases/download/v%{version}/micromdm_v%{version}.zip
Source1:    micromdm.service
Source2:    micromdm.sysconfig
Requires(pre): shadow-utils
%{?systemd_requires}
BuildRequires: systemd

%description
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
# Relevant zip file content, we ignore the 'darwin' directory
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}/var/lib/micromdm/filerepo
install -p -m 0755 linux/* %{buildroot}%{_sbindir}/
# Service and require sysconfig file
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/micromdm.service
install -D -p -m 0640 %{SOURCE2} %{buildroot}/etc/sysconfig/micromdm

%pre
getent group micromdm >/dev/null || groupadd -r micromdm
getent passwd micromdm >/dev/null || \
    useradd -r -g micromdm -d /var/lib/micromdm -s /sbin/nologin \
    -c "MicroMDM Server" micromdm
exit 0


%post
%systemd_post micromdm.service

%preun
%systemd_preun micromdm.service

%postun
%systemd_postun_with_restart micromdm.service

%files
%{_sbindir}/mdmctl
%{_sbindir}/micromdm
%attr(0750,micromdm,micromdm) %dir /var/lib/micromdm/
%attr(0750,micromdm,micromdm) %dir /var/lib/micromdm/filerepo/
%attr(0640,root,micromdm) %config(noreplace) /etc/sysconfig/micromdm
%{_unitdir}/micromdm.service

%changelog
* Wed Apr 20 2022 Vincent Tamet <vincent.tamet@exoclick.com> - 1.9.0-1
* Wed Aug 19 2020 Vincent Tamet <vincent.tamet@exoclick.com> - 1.6.0-1
- Initial release
