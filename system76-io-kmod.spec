%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%global tag master
%global ref heads
%endif

Name:     system76-io-kmod
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  akmod module for controlling System76 Io board
License:  GPLv2
URL:      https://github.com/pop-os/system76-io-dkms

Source:   %{url}/archive/refs/%{ref}/%{tag}.tar.gz

BuildRequires: kmodtool

%description
Kernel module for controlling the System76 Io board, which is used in System76's Thelio desktop line.

This driver provides hwmon interfaces for fan control, and tells the Io board when the system is suspending. Decisions on fan speeds are made in system76-power.

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
%setup -c system76-io-dkms-${tag}

for kernel_version  in %{?kernel_versions} ; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -a system76-io-dkms-master/*.c system76-io-dkms-master/Makefile _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/system76-io.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/system76-thelio-io.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/system76-io.ko
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/system76-thelio-io.ko
done
%{?akmod_install}

%changelog
{{{ git_dir_changelog }}}
