%global recipes_ver 6.2.2

Name:          deployer
Version:       6.8.0
Summary:       A deployment tool for PHP
Release:       1
License:       MIT
URL:           https://deployer.org/
Source0:       https://deployer.org/releases/v%{version}/deployer.phar
Source1:       https://github.com/deployphp/recipes/archive/%{recipes_ver}.tar.gz
BuildArch:     noarch
BuildRequires: php-cli >= 7.2

%description
A deployment tool for PHP.


%prep
%setup -q -T -c -a 1
cp %{SOURCE0} .
cp /etc/php.ini .
sed -i 's/^;phar.readonly = On/phar.readonly = Off/' php.ini


%build
mkdir recipes
mv recipes-%{recipes_ver}/recipe recipes
php -c php.ini /usr/bin/phar add -f deployer.phar recipes


%install
install -D -p -m 755 deployer.phar %{buildroot}%{_bindir}/%{name}


%files
%{_bindir}/%{name}


%changelog
* Thu May 06 2021 Michał Lisowski <michal@exads.com> - 6.8.0-1
- Initial RPM release


