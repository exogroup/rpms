# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%{?scl:          %scl_package         php-aerospike}

#global gh_commit   a4c3dd6f88f0a5d544986a5546c8de072200e6e4
#global gh_short    %%(c=%%{gh_commit}; echo ${c:0:7})
#global gh_date     20231025
%global gh_owner    aerospike
%global gh_project  php-client
%global pecl_name   aerospike
%global with_zts    0%{?_with_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini
#global prever      -beta

Summary:       Aerospike PHP Client
Name:          %{?scl_prefix}php-%{pecl_name}
Version:       1.2.0
%if 0%{?gh_date:1}
Release:       1.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif
License:       ASL 2.0
URL:           https://github.com/%{gh_owner}/%{gh_project}
# We build a self-contained tarball with prep-source.sh for offline build
Source0:       %{gh_project}-%{version}%{?prever}-vendor.tar.gz
Source99:      prep-source.sh

BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel > 8.1
#BuildRequires: cargo >= 1.74
BuildRequires: cargo
# For ext-php-rs
BuildRequires: clang-devel
# For aerospike v0.1.0
BuildRequires: protobuf-compiler

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Client extension for Aerospike.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package -n aerospike-connection-manager
Summary:       Aerospike Connection Manager (Local Daemon)
BuildRequires: golang
# We run "make proto" in prep-source.sh to avoid requiring this on el9
#BuildRequires: golang-google-grpc
#BuildRequires: golang-google-protobuf
Obsoletes:  aerospike-local-daemon < 1.1.0

%description -n aerospike-connection-manager
Aerospike Connection Manager used by the PHP extension to connect to Aerospike.


%prep
%setup -q -n %{gh_project}-%{version}%{?prever}-vendor
mkdir NTS
mv Cargo.* build.rs src NTS/
# This daemon/asld_kvs.proto is referenced by build.rs
mkdir NTS/aerospike-connection-manager
cp -a aerospike-connection-manager/asld_kvs.proto NTS/aerospike-connection-manager/

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension = %{pecl_name}.so
EOF


%build
%{?dtsenable}
export CFLAGS="%{optflags}"

cd NTS
PHP_CONFIG=%{_bindir}/%{?scl_prefix}php-config cargo build

%if %{with_zts}
cd ../ZTS
PHP_CONFIG=%{_bindir}/%{?scl_prefix}zts-php-config cargo build
%endif

# Aerospike Local Daemon
cd ../aerospike-connection-manager
# Don't use 'make build' as it's missing a build-id
%gobuild .


%install
%{?dtsenable}

# Install the NTS stuff
install -D -m 0755 NTS/target/debug/lib%{pecl_name}_php.so \
  %{buildroot}%{php_extdir}/%{pecl_name}.so
install -D -m 0644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
install -D -m 0755 ZTS/target/debug/lib%{pecl_name}_php.so \
  %{buildroot}%{php_ztsextdir}/%{pecl_name}.so
install -D -m 0644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Aerospike Local Daemon
install -D -m 0755 aerospike-connection-manager/asld %{buildroot}%{_sbindir}/asld


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
  --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
  --modules | grep %{pecl_name}
#: Upstream test suite for NTS extension - Requires server running
#%{__php} --no-php-ini \
#  --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
#  ../test.php

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
  --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
  --modules | grep %{pecl_name}
#: Upstream test suite for NTS extension - Requires server running
#%{__ztsphp} --no-php-ini \
#  --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
#  ../test.php
%endif


%files
#license LICENSE
%doc README.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files -n aerospike-connection-manager
%license aerospike-connection-manager/LICENSE
%doc aerospike-connection-manager/README.md
%{_sbindir}/asld


%changelog
* Mon May 26 2025 Matthias Saou <matthias@saou.eu> 1.2.0-1
- Update to 1.2.0.

* Mon Nov 11 2024 Matthias Saou <matthias@saou.eu> 1.1.0-1
- Update to 1.1.0.
- Rename aerospike-local-daemon to aerospike-connection-manager.

* Mon Feb 26 2024 Matthias Saou <matthias@saou.eu> 0.5.0-1
- Update to 0.5.0.

* Tue Jan  9 2024 Matthias Saou <matthias@saou.eu> 0.4.0-1
- Update to 0.4.0.

* Mon Nov 20 2023 Matthias Saou <matthias@saou.eu> 0.3.0-1
- Remove patch, ext-php-rs 0.10.4 now includes a proper fix.
- Tweak ... tag prefixed with "v" again, and suffixed with "-alpha"...

* Wed Nov 15 2023 Matthias Saou <matthias@saou.eu> 0.2.0-2
- Include patch to fix aarch64 build.

* Mon Oct 30 2023 Matthias Saou <matthias@saou.eu> 0.2.0-1
- Update to 0.2.0.

* Sun Oct  1 2023 Matthias Saou <matthias@saou.eu> 0.1.0-1
- Update to the PHP 8.1+ ext-php-rs (Rust) based extension.

* Tue Mar  2 2021 Matthias Saou <matthias@saou.eu> 7.5.2-1
- Initial RPM release.

