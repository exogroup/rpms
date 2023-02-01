Summary: RabbitMQ Delayed Message Plugin
Name: rabbitmq-delayed-message-exchange
Version: 3.11.1
Release: 1%{?dist}
License: MPLv2.0
URL: https://github.com/rabbitmq/rabbitmq-delayed-message-exchange
Source0: https://github.com/rabbitmq/rabbitmq-delayed-message-exchange/releases/download/%{version}/rabbitmq_delayed_message_exchange-%{version}.ez
BuildArch: noarch
Requires: rabbitmq-server >= 3.11.0

%description
This plugin adds delayed-messaging (or scheduled-messaging) to RabbitMQ.


%prep


%build


%install
mkdir -p %{buildroot}/usr/lib/rabbitmq/plugins
install -p -m 0644 %{SOURCE0} %{buildroot}/usr/lib/rabbitmq/plugins/


%files
/usr/lib/rabbitmq/plugins/rabbitmq_delayed_message_exchange-%{version}.ez


%changelog
* Wed Feb  1 2023 Matthias Saou <matthias@saou.eu> 3.11.1-1
- Update to 3.11.1.

* Thu May 21 2020 David Castañeda <edupr91@gmail.com> 3.8.0-1
- Initial RPM release.

