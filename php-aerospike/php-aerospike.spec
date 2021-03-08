# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%{?scl:          %scl_package         php-aerospike}

%global gh_commit   f6931abc8826e48df71cf9c778bd5657ada13b41
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date     20200729
%global gh_owner    aerospike
%global gh_project  aerospike-client-php
%global pecl_name   aerospike
%global with_zts    0%{?_with_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini

# Log level TRACE|DEBUG|INFO|WARN|ERROR|OFF
%define as_log_level OFF

Summary:       Aerospike PHP Client
Name:          %{?scl_prefix}php-%{pecl_name}
Version:       7.5.2
%if 0%{?gh_date:1}
Release:       1.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif
License:       ASL 2.0
URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel > 7
#BuildRequires: %{?scl_prefix}php-tokenizer
BuildRequires: compat-aerospike-client-c-devel >= 4.6.0
BuildRequires: compat-aerospike-client-c-devel < 5.0.0
BuildRequires: libev-devel

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


%prep
%setup -q -n %{gh_project}-%{gh_commit}
mv src NTS

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
# Replicate build.sh overrides
CFLAGS="%{optflags} -std=gnu99 -D__AEROSPIKE_PHP_CLIENT_LOG_LEVEL__=AS_LOG_LEVEL_%{as_log_level}"
LDFLAGS="-laerospike -lcrypto -lssl -lev" # -Wl,-Bdynamic ? -lrt ?

cd NTS
%{_bindir}/phpize
%configure \
    --enable-aerospike \
    --with-php-config=%{_bindir}/php-config \
    PHP7=1 SWIG=1
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-aerospike \
    --with-php-config=%{_bindir}/zts-php-config \
    PHP7=1 SWIG=1
make %{?_smp_mflags}
%endif


%install
%{?dtsenable}

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

#: Upstream test suite  for NTS extension
#TEST_PHP_EXECUTABLE=%{__php} \
#TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
#NO_INTERACTION=1 \
#REPORT_EXIT_STATUS=1 \
#%{__php} -n run-tests.php --show-diff || : ignore

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

#: Upstream test suite  for ZTS extension
#TEST_PHP_EXECUTABLE=%{__ztsphp} \
#TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
#NO_INTERACTION=1 \
#REPORT_EXIT_STATUS=1 \
#%{__ztsphp} -n run-tests.php --show-diff
%endif


%files
%license LICENSE
%doc README.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Mar  2 2021 Matthias Saou <matthias@saou.eu> 7.5.2-1
- Initial RPM release.

