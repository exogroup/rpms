# EXOGROUP RPMs

This repository contains the source files used to build rpm packages that are,
have been, or will be in use at EXOGROUP. They are usually targeted at the
latest Red Hat Enterprise Linux (RHEL) or CentOS release at the time they are
published.

* Some [EPEL](https://fedoraproject.org/wiki/EPEL) packages may be required.
* Some [Remirepo](http://rpms.remirepo.net/) packages may be required.
* Some packages are not proper builds, using binary releases as source, only
  adding user creation, systemd service, etc.
* Some packages are so closely tied to others that they will have their rpm
  build files inside the same directory.
* Packages try to follow the [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
  as much as possible.
* Packages are built using [Mock](https://github.com/rpm-software-management/mock),
  which is why all files are in the same directory.

For general rpm packaging help, see: https://rpm-packaging-guide.github.io/

