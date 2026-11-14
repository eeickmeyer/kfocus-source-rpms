%global commit 536acf3b28c0a68dff9c5573cb48541c84dff657

Name:           kfocus-power-bin
Version:        26.04.7
Release:        2%{?dist}
Summary:        Power profile, processor frequency, and fan controls
License:        GPL-2.0-or-later
URL:            https://github.com/eeickmeyer/kfocus-source
Source0:        https://github.com/eeickmeyer/kfocus-source/archive/%{commit}.tar.gz
Source1:        kfocus-power-profile
Patch0:         kfocus-power-bin-cpupower.patch
Patch1:         kfocus-power-bin-fand-driver.patch
Patch2:         kfocus-power-bin-power-profile.patch
BuildRequires:  cmake >= 4.2
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  kf6-kcoreaddons-devel
BuildRequires:  kf6-kiconthemes-devel
BuildRequires:  kf6-kirigami-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-qqc2-desktop-style
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  systemd-devel
Requires:       kernel-tools
Requires:       hicolor-icon-theme
Requires:       kfocus-common
Requires:       kfocus-hw >= 26.04.6-2
Requires:       kf6-qqc2-desktop-style
Requires:       kmod
Requires:       polkit
Requires:       ppd-service
Requires:       systemd

%description
Kubuntu Focus power and fan tools for selecting power profiles, processor
frequency settings, and fan settings.

%prep
%autosetup -n kfocus-source-%{commit} -p1

%build
(cd package-power-bin/kfocus-fand && ./build.sh)
cmake -S package-power-bin -B build \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix}
cmake --build build --parallel

%install
DESTDIR=%{buildroot} cmake --install build

install -Dpm 0644 package-power-bin/debian/copyright \
    %{buildroot}%{_licensedir}/%{name}/copyright
install -Dpm 0755 package-power-bin/kfocus-fand/kfocus-fand \
    %{buildroot}%{_prefix}/lib/kfocus/bin/kfocus-fand
install -Dpm 0755 %{SOURCE1} \
    %{buildroot}%{_prefix}/lib/kfocus/bin/kfocus-power-profile
for utility in kfocus-fan-set kfocus-power-set kfocus-pstate kfocus-pstate-set; do
    install -Dpm 0755 "package-power-bin/usr/lib/kfocus/bin/${utility}" \
        "%{buildroot}%{_prefix}/lib/kfocus/bin/${utility}"
done

install -Dpm 0644 \
    package-power-bin/usr/lib/systemd/system/kfocus-fand.service \
    %{buildroot}%{_unitdir}/kfocus-fand.service
install -Dpm 0644 package-power-bin/usr/share/kfocus/kfocus_fand.d/.keep \
    %{buildroot}%{_datadir}/kfocus/kfocus_fand.d/.keep

install -Dpm 0644 \
    package-power-bin/usr/share/icons/hicolor/scalable/apps/kfocus-bug-fan.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/kfocus-bug-fan.svg
install -Dpm 0644 \
    package-power-bin/usr/share/icons/hicolor/scalable/apps/kfocus-bug-power.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/kfocus-bug-power.svg
install -Dpm 0644 \
    package-power-bin/usr/share/polkit-1/actions/org.kfocus.pkexec.kfocus-fan.policy \
    %{buildroot}%{_datadir}/polkit-1/actions/org.kfocus.pkexec.kfocus-fan.policy
install -Dpm 0644 \
    package-power-bin/usr/share/polkit-1/actions/org.kfocus.pkexec.kfocus-power.policy \
    %{buildroot}%{_datadir}/polkit-1/actions/org.kfocus.pkexec.kfocus-power.policy
install -Dpm 0644 \
    package-power-bin/usr/share/polkit-1/actions/org.kfocus.pkexec.kfocus-pstate.policy \
    %{buildroot}%{_datadir}/polkit-1/actions/org.kfocus.pkexec.kfocus-pstate.policy
install -Dpm 0644 \
    package-power-bin/usr/share/applications/org.kfocus.power.desktop \
    %{buildroot}%{_datadir}/applications/org.kfocus.power.desktop

ln -s kfocus-power-bin %{buildroot}%{_prefix}/lib/kfocus/bin/kfocus-fan
ln -s kfocus-power-bin %{buildroot}%{_prefix}/lib/kfocus/bin/kfocus-power
install -d %{buildroot}%{_bindir}
ln -s %{_prefix}/lib/kfocus/bin/kfocus-fan \
    %{buildroot}%{_bindir}/kfocus-fan
ln -s %{_prefix}/lib/kfocus/bin/kfocus-power \
    %{buildroot}%{_bindir}/kfocus-power
ln -s %{_prefix}/lib/kfocus/bin/kfocus-pstate \
    %{buildroot}%{_bindir}/kfocus-pstate

%post
%systemd_post kfocus-fand.service
if [ "$1" -eq 1 ] && [ -f %{_datadir}/kfocus/kfocus_fand.d/fan_profile_db ]; then
    systemctl enable kfocus-fand.service || exit 1
    if [ -d /run/systemd/system ]; then
        systemctl daemon-reload || exit 1
        systemctl start kfocus-fand.service || exit 1
    fi
fi

# Migrate installations made before the daemon was enabled.
%triggerun -- kfocus-power-bin < 26.04.7-2
if [ "$1" -gt 0 ] && [ -f %{_datadir}/kfocus/kfocus_fand.d/fan_profile_db ]; then
    systemctl enable kfocus-fand.service || exit 1
    if [ -d /run/systemd/system ]; then
        systemctl daemon-reload || exit 1
        systemctl start kfocus-fand.service || exit 1
    fi
fi

%preun
%systemd_preun kfocus-fand.service

%postun
%systemd_postun_with_restart kfocus-fand.service

%files
%license %{_licensedir}/%{name}/copyright
%{_prefix}/lib/kfocus/bin/kfocus-power-bin
%{_prefix}/lib/kfocus/bin/kfocus-power-profile
%{_prefix}/lib/kfocus/bin/kfocus-fand
%{_prefix}/lib/kfocus/bin/kfocus-fan-set
%{_prefix}/lib/kfocus/bin/kfocus-power-set
%{_prefix}/lib/kfocus/bin/kfocus-pstate
%{_prefix}/lib/kfocus/bin/kfocus-pstate-set
%{_prefix}/lib/kfocus/bin/kfocus-fan
%{_prefix}/lib/kfocus/bin/kfocus-power
%{_bindir}/kfocus-fan
%{_bindir}/kfocus-power
%{_bindir}/kfocus-pstate
%{_unitdir}/kfocus-fand.service
%{_datadir}/kfocus/kfocus_fand.d/.keep
%{_datadir}/icons/hicolor/scalable/apps/kfocus-bug-fan.svg
%{_datadir}/icons/hicolor/scalable/apps/kfocus-bug-power.svg
%{_datadir}/polkit-1/actions/org.kfocus.pkexec.kfocus-fan.policy
%{_datadir}/polkit-1/actions/org.kfocus.pkexec.kfocus-power.policy
%{_datadir}/polkit-1/actions/org.kfocus.pkexec.kfocus-pstate.policy
%{_datadir}/applications/org.kfocus.power.desktop

%changelog
* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.7-2
- Configure and start the fan daemon on supported hardware
- Use the power-profiles D-Bus API with either TuneD or power-profiles-daemon

* Sat Nov 14 2026 Kubuntu Focus Team <support@kfocus.org> - 26.04.7-1
- Package power and fan controls for Fedora
- Use Fedora kernel-tools cpupower for CPU frequency controls
