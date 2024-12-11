%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     system76-io
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  akmod module for controlling System76 Io board
License:  GPLv2
URL:      https://github.com/ssweeny/system76-io-akmod

Source:   %{url}/archive/refs/heads/main.tar.gz

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Kernel module for controlling the System76 Io board, which is used in System76's Thelio desktop line.

This driver provides hwmon interfaces for fan control, and tells the Io board when the system is suspending. Decisions on fan speeds are made in system76-power.

%prep
%setup -q -c system76-io-akmod-main

%build
install -D -m 0644 system76-io-akmod-main/%{name}.conf %{buildroot}%{_modulesloaddir}/%{name}.conf

%files
%doc system76-io-akmod-main/README.md
%license system76-io-akmod-main/LICENSE
%{_modulesloaddir}/%{name}.conf

%changelog
{{{ git_dir_changelog }}}
