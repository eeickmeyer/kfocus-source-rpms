%global commit 536acf3b28c0a68dff9c5573cb48541c84dff657

Name:           kfocus-common
Version:        26.04.12~beta1
Release:        2%{?dist}
Summary:        Common libraries and application menu for Kubuntu Focus tools
License:        GPL-2.0-or-later
URL:            https://github.com/eeickmeyer/kfocus-source
Source0:        https://github.com/eeickmeyer/kfocus-source/archive/%{commit}.tar.gz
Patch0:         kfocus-common-screen-size.patch
BuildArch:      noarch
Requires:       bc
Requires:       kdialog
Requires:       v4l-utils

%description
Common shell and Python libraries, desktop menu data, and icons used by
Kubuntu Focus tools.

%prep
%autosetup -n kfocus-source-%{commit} -p1

%build

%install
install -d %{buildroot}%{_prefix}/lib/kfocus
cp -a package-main/usr/lib/kfocus/lib \
    %{buildroot}%{_prefix}/lib/kfocus/
install -d %{buildroot}%{_prefix}/lib/kfocus/conf
install -pm 0644 \
    package-main/usr/lib/kfocus/conf/etc_logrotate.d_kfocus \
    %{buildroot}%{_prefix}/lib/kfocus/conf/
install -pm 0644 \
    package-main/usr/lib/kfocus/conf/etc_rsyslog.d_10-kfocus.conf \
    %{buildroot}%{_prefix}/lib/kfocus/conf/
install -pm 0644 \
    package-main/usr/lib/kfocus/conf/etc_xdg_menus_applications-merged_kfocus.menu \
    %{buildroot}%{_prefix}/lib/kfocus/conf/

install -d %{buildroot}%{_datadir}/desktop-directories
install -pm 0644 package-main/usr/share/desktop-directories/kfocus.directory \
    %{buildroot}%{_datadir}/desktop-directories/
install -Dpm 0644 \
    package-main/usr/share/icons/hicolor/scalable/apps/kfocus-bug-tools.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/kfocus-bug-tools.svg

install -d %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
ln -s %{_prefix}/lib/kfocus/conf/etc_xdg_menus_applications-merged_kfocus.menu \
    %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/kfocus.menu
install -d %{buildroot}%{_sysconfdir}/rsyslog.d
ln -s %{_prefix}/lib/kfocus/conf/etc_rsyslog.d_10-kfocus.conf \
    %{buildroot}%{_sysconfdir}/rsyslog.d/10-kfocus.conf
install -d %{buildroot}%{_sysconfdir}/logrotate.d
ln -s %{_prefix}/lib/kfocus/conf/etc_logrotate.d_kfocus \
    %{buildroot}%{_sysconfdir}/logrotate.d/kfocus

%files
%license COPYING
%{_prefix}/lib/kfocus/lib/
%{_prefix}/lib/kfocus/conf/etc_logrotate.d_kfocus
%{_prefix}/lib/kfocus/conf/etc_rsyslog.d_10-kfocus.conf
%{_prefix}/lib/kfocus/conf/etc_xdg_menus_applications-merged_kfocus.menu
%{_datadir}/desktop-directories/kfocus.directory
%{_datadir}/icons/hicolor/scalable/apps/kfocus-bug-tools.svg
%{_sysconfdir}/xdg/menus/applications-merged/kfocus.menu
%{_sysconfdir}/rsyslog.d/10-kfocus.conf
%{_sysconfdir}/logrotate.d/kfocus

%changelog
* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.12~beta1-2
- Fix XE Gen 3 screen-size fallback and install its detection tools

* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.12~beta1-1
- Package common libraries and menu assets for Fedora
