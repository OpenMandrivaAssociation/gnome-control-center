%define pkgname control-center
%define lib_major	1
%define libname	%mklibname gnome-window-settings %{lib_major}
%define libnamedev %mklibname -d gnome-window-settings

Summary: GNOME control center
Name: gnome-%{pkgname}
Version: 2.26.0
Release: %mkrel 3
License: GPLv2+
Group: Graphical desktop/GNOME
BuildRequires:  evolution-data-server-devel >= 1.5.3
BuildRequires:	gnome-desktop-devel >= 2.25.1
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:  libmetacity-private-devel >= 2.23.1
BuildRequires:  nautilus-devel >= 2.9.0
BuildRequires:  eel-devel
BuildRequires:  libxklavier-devel >= 2.91
BuildRequires:  libxxf86misc-devel                                             
BuildRequires:  gnome-menus-devel >= 2.11.1
BuildRequires:  libgstreamer-plugins-base-devel
BuildRequires:  libxscrnsaver-devel
BuildRequires:	hal-devel
BuildRequires:	libgnomekbd-devel
BuildRequires:  gnome-panel-devel
BuildRequires:  gnome-settings-daemon-devel
BuildRequires:	policykit-gnome-devel
BuildRequires: librsvg-devel                                                   
BuildRequires: libcanberra-devel
BuildRequires:  desktop-file-utils
BuildRequires: scrollkeeper
BuildRequires:	automake1.8
BuildRequires:	autoconf
BuildRequires:  gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
BuildRequires:	shared-mime-info
BuildRequires:  gnome-common
BuildRequires:	gettext-devel
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Source1: backgrounds.xml
Patch: gnome-control-center-2.25.3-fix-format-strings.patch
Patch3: gnome-control-center-2.19.91-naming.patch
# (fc) 2.10.2-2mdk display icons when control-center is not started from GNOME (Mdk bug #16767)
Patch16: gnome-control-center-2.17.3-menulocation.patch
# (fc) 2.23.6-2mdv force default dpi to 96, don't use X server value
Patch17: gnome-control-center-2.23.6-forcedpi.patch
# (fc) 2.23.90-3mdv user usermode to change password (Fedora)
Patch18: gnome-control-center-2.25.2-passwd.patch
# (fc) 2.23.90-3mdv allow to change gecos field (Fedora)
Patch19: gnome-control-center-2.25.90-gecos.patch
# (fc) 2.23.90-3mdv fix gecos field display on non-UTF8 locale
Patch20: gnome-control-center-2.23.90-nonutf8.patch
# (cg) 2.26.0-3mdv support touchpads (patch from fedora)
Patch21: gnome-control-center-2.26.0-support-touchpads.patch

Requires: gstreamer0.10-plugins-base
Requires: gstreamer0.10-plugins-good
Requires: gnome-settings-daemon >= 2.21.5
Obsoletes: %{pkgname}
Provides: %{pkgname}
Obsoletes: themus
Provides: themus
Obsoletes: fontilus
Provides: fontilus
Obsoletes: drwright
Provides: drwright
Obsoletes: metatheme
Provides: metatheme
Obsoletes: metacity-setup
Provides: metacity-setup

Obsoletes: %{name}-plus
Obsoletes: xalf
Provides: xalf
Provides: %{name}-plus

BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.gnome.org/softwaremap/projects/control-center/

Requires(post): shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils

%description
GNOME Control-center is a configuration tool for easily
setting up your GNOME environment.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries

Provides:	libgnome-window-settings = %{version}-%{release}

%description -n %{libname}
Dynamic libraries used by GNOME Control Center


%package -n %{libnamedev}
Summary:	Static libraries, include files for GNOME control center
Group:		Development/GNOME and GTK+

Provides:	libgnome-window-settings-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Obsoletes: %mklibname -d gnome-window-settings 1

%description -n %{libnamedev}
Static libraries, include files for GNOME Control Center

%prep
%setup -q -n %{name}-%{version}
%patch -p1
%patch3 -p1 -b .naming
%patch16 -p1 -b .menulocation
%patch17 -p1 -b .forcedpi
%patch18 -p1 -b .passwd
%patch19 -p1 -b .gecos
%patch20 -p1 -b .nonutf8
%patch21 -p1 -b .touchpads

#needed by patch18
autoreconf -fi

%build
%configure2_5x --enable-aboutme --enable-gstreamer=0.10

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std UPDATE_MIME_DATABASE=true
rm -f %buildroot%_datadir/applications/mimeinfo.cache

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="PersonalSettings" \
  --add-category="X-MandrivaLinux-System-Configuration-GNOME" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-category="X-MandrivaLinux-System-Configuration-GNOME" \
  --add-category="X-MandrivaLinux-System-Configuration-GNOME-Accessibility" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/at-properties.desktop 

%{find_lang} %{pkgname}-2.0 --with-gnome --all-name
for omf in $(ls %buildroot%_datadir/omf/*/*.omf|fgrep -v -- -C.omf);do 
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %{pkgname}-2.0.lang
done


mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/*.{la,a} \
 $RPM_BUILD_ROOT%{_datadir}/applications/mimeinfo.cache \
 $RPM_BUILD_ROOT/var/lib/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%post
%define schemas control-center fontilus
%if %mdkversion < 200900
%post_install_gconf_schemas %schemas
%{update_menus}
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_desktop_database
%clean_icon_cache hicolor
%clean_mime_database
%endif

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{libname}
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{libname}
%endif


%files -f %{pkgname}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/control-center.schemas
%{_sysconfdir}/gconf/schemas/fontilus.schemas
%config(noreplace) %{_sysconfdir}/xdg/menus/gnomecc.menu
%config(noreplace) %{_sysconfdir}/xdg/autostart/gnome-at-session.desktop
%_bindir/gnome-about-me
%_bindir/gnome-appearance-properties
%_bindir/gnome-at-mobility
%_bindir/gnome-at-properties
%_bindir/gnome-at-visual
%_bindir/gnome-control-center
%_bindir/gnome-default-applications-properties
%_bindir/gnome-display-properties
%_bindir/gnome-font-viewer
%_bindir/gnome-keybinding-properties
%_bindir/gnome-keyboard-properties
%_bindir/gnome-mouse-properties
%_bindir/gnome-network-properties
%_bindir/gnome-thumbnail-font
%_bindir/gnome-typing-monitor
%_bindir/gnome-window-properties
%_datadir/icons/hicolor/*/*/*
%{_libdir}/window-manager-settings/*.so
%{_datadir}/gnome-background-properties
%{_datadir}/applications/*
%_datadir/mime/packages/*
%{_datadir}/gnome/cursor-fonts
%{_datadir}/desktop-directories/*
%_datadir/gnome-control-center/
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/libgnome-window-settings.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(-, root, root)
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*a
%{_libdir}/pkgconfig/*
%_datadir/pkgconfig/*
