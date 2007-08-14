%define pkgname control-center
%define lib_major	1
%define libname	%mklibname gnome-window-settings %{lib_major}
%define libnamedev %mklibname -d gnome-window-settings

Summary: GNOME control center
Name: gnome-%{pkgname}
Version: 2.19.90
Release: %mkrel 1
License: GPL
Group: Graphical desktop/GNOME
BuildRequires:  evolution-data-server-devel >= 1.5.3
BuildRequires:	gnome-desktop-devel >= 2.1.0
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:  libmetacity-private-devel
BuildRequires:  nautilus-devel >= 2.9.0
BuildRequires:  libxklavier-devel >= 2.91
BuildRequires:  libxxf86misc-devel
BuildRequires:  gnome-menus-devel >= 2.11.1
BuildRequires:  libgstreamer-plugins-base-devel
BuildRequires:  libxscrnsaver-devel
BuildRequires:	hal-devel
BuildRequires:	libgnomekbd-devel
BuildRequires:	gnome-panel-devel
BuildRequires:	librsvg-devel
BuildRequires:  desktop-file-utils
BuildRequires:  perl-XML-Parser
BuildRequires:	scrollkeeper
BuildRequires:	automake1.8
BuildRequires:	autoconf
BuildRequires:  gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
BuildRequires:	shared-mime-info
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Source1: backgrounds.xml
# gw from Fedora: replace gnome-search-tool by beagle/tracker
Patch: gnome-control-center-2.19.1-search.patch
Patch3: gnome-control-center-2.13.5-naming.patch
# (fc) 2.8.1-1mdk fix logout keybinding
Patch7: gnome-control-center-2.8.1-logout.patch
# (fc) 2.8.2-3mdk enable more multimedia keys
Patch11: gnome-control-center-2.8.2-multimedia.patch
# (fc) 2.10.2-2mdk display icons when control-center is not started from GNOME (Mdk bug #16767)
Patch16: gnome-control-center-2.17.3-menulocation.patch
# gw this takes a parameter and shouldn't be in the menu                       
Patch20: gnome-control-center-2.19.6-hide-install-theme.patch

Requires: gstreamer0.10-plugins-base
Requires: gstreamer0.10-plugins-good
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

Requires: gnome-screensaver
Requires: gnome-desktop >= 2.1.4
Requires: gnome-themes
Requires: metacity
Requires(post): shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils

%description
GNOME Control-center is a configuration tool for easily
setting up your GNOME environment.

%package -n %{libname}
Summary:	%{summary}
Group:		%{group}

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
%patch -p1 -b .search
%patch3 -p1 -b .naming
%patch7 -p1 -b .logout
%patch11 -p1 -b .multimedia
%patch16 -p1 -b .menulocation
%patch20 -p1 -b .hide-install-theme

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
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/accessibility-keyboard.desktop $RPM_BUILD_ROOT%{_datadir}/applications/at-properties.desktop 

%{find_lang} %{pkgname}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/*/*-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %{pkgname}-2.0.lang
done


mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/*.{la,a} \
 $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/*.{la,a} \
 $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/*.{la,a} \
 $RPM_BUILD_ROOT%{_datadir}/applications/mimeinfo.cache \
 $RPM_BUILD_ROOT/var/lib/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%post
%define schemas apps_gnome_settings_daemon_default_editor apps_gnome_settings_daemon_keybindings apps_gnome_settings_daemon_screensaver desktop_gnome_font_rendering fontilus themus
%post_install_gconf_schemas %schemas
%{update_menus}
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%preun
%preun_uninstall_gconf_schemas %schemas

%postun
%{clean_menus}
%clean_desktop_database
%clean_icon_cache hicolor
%clean_mime_database

%post -p /sbin/ldconfig -n %{libname}

%postun -p /sbin/ldconfig -n %{libname}


%files -f %{pkgname}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/*
%config(noreplace) %{_sysconfdir}/xdg/menus/gnomecc.menu
%config(noreplace) %{_sysconfdir}/gnome-vfs-2.0/modules/*
%_bindir/gnome-about-me
%_bindir/gnome-accessibility-keyboard-properties
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
%_bindir/gnome-network-preferences
%_bindir/gnome-sound-properties
%_bindir/gnome-theme-thumbnailer
%_bindir/gnome-thumbnail-font
%_bindir/gnome-typing-monitor
%_bindir/gnome-window-properties
%_bindir/themus-theme-applier
%_datadir/icons/hicolor/*/*/*
%{_libexecdir}/gnome-settings-daemon
%{_libdir}/nautilus/extensions-1.0/*.so
%{_libdir}/gnome-vfs-2.0/modules/*.so
%{_libdir}/window-manager-settings/*.so
%_datadir/dbus-1/services/*
%{_datadir}/gnome-background-properties
%{_datadir}/gnome/autostart/gnome-at-session.desktop
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
%_datadir/pkgconfig/gnome-keybindings.pc
