# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%{?scl:          %scl_package         php-FiftyOneDegreesHashEngine}

%global gh_commit   6a8191db2de1c50e2acc959738ef8db36f6b3377
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    51Degrees
%global gh_project  device-detection-php-onpremise
%global pecl_name   FiftyOneDegreesHashEngine
%global with_zts    0%{?_with_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini

# Extract commit hash with 'git submodule status'
# https://github.com/51Degrees/device-detection-cxx
%global cxx_dd_commit 3cda350cebbbfc64069149ef3bf2cef5e1b93199
%global cxx_dd_short  %(c=%{cxx_dd_commit}; echo ${c:0:7})
# https://github.com/51Degrees/common-cxx
%global cxx_c_commit  d63b291826b8282b36f08d397847335a69d1a0a8
%global cxx_c_short   %(c=%{cxx_c_commit}; echo ${c:0:7})

Summary:       Client extension for 51Degrees Device-Detection
Name:          %{?scl_prefix}php-%{pecl_name}
Version:       4.3.3
%if 0%{?gh_date:1}
Release:       1.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:       2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif
License:       EUPL 1.2
URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:       https://github.com/%{gh_owner}/device-detection-cxx/archive/%{cxx_dd_commit}/device-detection-cxx-%{cxx_dd_short}.tar.gz
Source2:       https://github.com/%{gh_owner}/common-cxx/archive/%{cxx_c_commit}/common-cxx-%{cxx_c_short}.tar.gz

BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel > 7
#BuildRequires: %{?scl_prefix}php-tokenizer
BuildRequires: libatomic

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Client extension for 51Degrees Device-Detection.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -n %{gh_project}-%{gh_commit} -a 1 -a 2
rmdir device-detection-cxx-%{cxx_dd_commit}/src/common-cxx
mv common-cxx-%{cxx_c_commit} device-detection-cxx-%{cxx_dd_commit}/src/common-cxx
rmdir on-premise/device-detection-cxx
mv device-detection-cxx-%{cxx_dd_commit} on-premise/device-detection-cxx
mv on-premise NTS

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension = %{pecl_name}.so

; Configuration
FiftyOneDegreesHashEngine.data_file = ''
FiftyOneDegreesHashEngine.required_properties = 'BrowserName,BrowserVendor,BrowserVersion,DeviceType,HardwareVendor'
EOF


%build
%{?dtsenable}

cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    PHP7=1
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
    PHP7=1
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
#%{__php} -c ../%{ini_name} --modules | grep %{pecl_name}
#%{__php} --no-php-ini \
#    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
#    --modules | grep %{pecl_name}

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
%doc readme.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Nov  2 2021 Matthias Saou <matthias@saou.eu> 4.3.3-1
- Update to 4.3.3.
- Remove incorrect SWIG=1 that makes the build fail.
- Add new libatomic build requirement.

* Thu Jun 10 2021 Matthias Saou <matthias@saou.eu> 4.2.4-2
- Update to 4.2.4, cxx to latest stables too.

* Mon Feb 22 2021 Matthias Saou <matthias@saou.eu> 4.2.0-1
- Update to 4.2.0.

* Wed Aug 12 2020 Matthias Saou <matthias@saou.eu> 4.1.0-1
- Initial RPM release.

