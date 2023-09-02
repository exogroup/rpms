# This spec file does *NOT* try to follow the Fedora Rust Packaging Guidelines

# Exclude input files from mangling
%global __brp_mangle_shebangs_exclude_from ^/usr/src/.*$

Summary: Distributed object storage service tailored for self-hosting
Name: garage
Version: 0.8.3
Release: 1%{?dist}
License: GPLv2+
URL: https://garagehq.deuxfleurs.fr/
# We build a self-contained tarball with prep-source.sh for offline build
Source0: garage-%{version}-vendor.tar.gz
Source1: garage.toml.sh
Source2: garage.sysconfig
Source3: garage.service
Source999: prep-source.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
ExclusiveArch: x86_64 aarch64
BuildRequires: rust-packaging >= 21
BuildRequires: pkgconfig(libzstd)
BuildRequires: pkgconfig(libsodium)
BuildRequires: systemd
BuildRequires: openssl
%{?systemd_requires}

%description
Garage is an S3-compatible distributed object storage service designed for
self-hosting at a small-to-medium scale.
Garage is designed for storage clusters composed of nodes running at different
physical locations, in order to easily provide a storage service that
replicates data at these different locations and stays available even when some
servers are unreachable. Garage also focuses on being lightweight, easy to
operate, and highly resilient to machine failures.


%prep
%setup -q -n %{name}-%{version}-vendor


%build
cargo --offline build \
  --release \
  --no-default-features \
  --features system-libs,metrics,lmdb


%install
rm -rf %{buildroot}
install -D -m 0755 target/release/garage %{buildroot}%{_sbindir}/garage
install -D -m 0644 %{SOURCE2} %{buildroot}/etc/sysconfig/garage
install -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/garage.service
sh %{SOURCE1} > %{buildroot}/etc/garage.toml
mkdir -p %{buildroot}/var/lib/garage


%pre
/usr/bin/getent group garage >/dev/null || \
  /usr/sbin/groupadd -r garage
/usr/bin/getent passwd garage >/dev/null || \
  /usr/sbin/useradd -r -g garage -M -d /var/lib/garage -s /sbin/nologin -c "Garage Data Store" garage


%post
%systemd_post garage.service

%preun
%systemd_preun garage.service

%postun
%systemd_postun_with_restart garage.service


%files
%license LICENSE
%doc README.md
%config(noreplace) %attr(0640,root,garage) /etc/garage.toml
%config(noreplace) %attr(0640,root,garage) /etc/sysconfig/garage
%{_sbindir}/garage
%{_unitdir}/garage.service
%dir %attr(0770,garage,garage) /var/lib/garage/


%changelog
* Fri Sep  1 2023 Matthias Saou <matthias@saou.eu> 0.8.3-1
- Initial RPM release.

