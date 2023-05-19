%global recipes_ver 6.2.2

Name:          deployer
Version:       6.9.0
Summary:       Deployment tool with support for popular PHP frameworks
Release:       1
License:       MIT
URL:           https://deployer.org/
Source0:       https://deployer.org/releases/v%{version}/deployer.phar
Source1:       https://github.com/deployphp/recipes/archive/%{recipes_ver}/recipes-%{recipes_ver}.tar.gz
BuildArch:     noarch
BuildRequires: php-cli >= 7.2
Requires:      php-cli >= 7.2

%description
Deployer is a cli tool for deployment of any PHP applications, including
frameworks such as Laravel, Symfony, Zend Framework and many more.


%prep
%setup -q -T -c -a 1
mkdir contrib-recipes
mv recipes-%{recipes_ver}/recipe contrib-recipes/
cp %{SOURCE0} .
# Required setting to be allowed to modify phar files
sed 's/^;phar.readonly = On/phar.readonly = Off/' /etc/php.ini > php.ini


%build
php -c php.ini /usr/bin/phar add -f deployer.phar contrib-recipes


%install
install -D -p -m 755 deployer.phar %{buildroot}%{_bindir}/%{name}


%files
%{_bindir}/%{name}


%changelog
* Fri May 19 2023 Matthias Saou <matthias@saou.eu> 6.9.0-1
- Update to 6.9.0 for PHP 8 compatibility.

* Fri May 14 2021 Michał Lisowski <michal@exads.com> - 6.8.0-2
- php-cli is required at runtime

* Thu May 06 2021 Michał Lisowski <michal@exads.com> - 6.8.0-1
- Initial RPM release

