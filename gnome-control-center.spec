%define pkgname control-center
%define lib_major	1
%define lib_name	%mklibname gnome-window-settings %{lib_major}


Summary: GNOME control center
Name: gnome-%{pkgname}
Version: 2.18.0
Release: %mkrel 4
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
BuildRequires:	automake1.8
BuildRequires:	autoconf
BuildRequires:  gnome-doc-utils libxslt-proc
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
BuildRequires:	shared-mime-info
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%{version}.tar.bz2
Source1: backgrounds.xml
# gw from Fedora: replace gnome-search-tool by beagle/tracker
Patch: control-center-2.17.90-search.patch
Patch3: gnome-control-center-2.13.5-naming.patch
# (fc) 2.8.1-1mdk fix logout keybinding
Patch7: gnome-control-center-2.8.1-logout.patch
# (fc) 2.8.2-3mdk enable more multimedia keys
Patch11: gnome-control-center-2.8.2-multimedia.patch
# (fc) 2.8.2-5mdk fix keybinding when keysim aren't available
Patch13: gnome-control-center-2.8.2-badkeysim.patch
# (fc) 2.10.2-2mdk display icons when control-center is not started from GNOME (Mdk bug #16767)
Patch16: gnome-control-center-2.17.3-menulocation.patch
# (fc) 2.18.0-2mdv fix multimedia key window position (GNOME bug #400915) (SVN)
Patch17: gnome-control-center-2.18.0-multimediakeyswindowposition.patch
# (fc) 2.18.0-2mdv fix gthread warning in sound config (GNOME bug #416239) (SVN)
Patch18: gnome-control-center-2.18.0-soundgthread.patch
# (fc) 2.18.0-2mdv disable color revert when using default (GNOME bug #417423)
Patch19: gnome-control-center-2.18.0-disablerevert.patch
# gw this takes a parameter and shouldn't be in the menu
Patch20: control-center-2.18.0-dont-display-theme-installer.patch
# (fc) 2.18.0-4mdv don't crash if dbus isn't running (SVN) (GNOME bug #411504)
Patch21: gnome-control-center-2.18.0-fixdbuscrash.patch

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

%package -n %{lib_name}
Summary:	%{summary}
Group:		%{group}

Provides:	libgnome-window-settings = %{version}-%{release}

%description -n %{lib_name}
Dynamic libraries used by GNOME Control Center


%package -n %{lib_name}-devel
Summary:	Static libraries, include files for GNOME control center
Group:		Development/GNOME and GTK+

Provides:	libgnome-window-settings-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}

%description -n %{lib_name}-devel
Static libraries, include files for GNOME Control Center

%prep
%setup -q -n %{pkgname}-%{version}
%patch -p1 -b .search
%patch3 -p1 -b .naming
%patch7 -p1 -b .logout
%patch11 -p1 -b .multimedia
%patch13 -p1 -b .badkeysim
%patch16 -p1 -b .menulocation
%patch17 -p1 -b .multimediakeyswindowposition
%patch18 -p1 -b .soundgthread
%patch19 -p1 -b .disablerevert
%patch20 -p1 -b .hide-install-theme
%patch21 -p1 -b .fixdbuscrash

%build
%configure2_5x --enable-aboutme --disable-scrollkeeper --enable-gstreamer=0.10

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std UPDATE_MIME_DATABASE=true
rm -f %buildroot%_datadir/applications/mimeinfo.cache

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): icon="gnome-control-center" title="GNOME Control Center" needs="gnome" section="System/Configuration/GNOME" command="%{_bindir}/gnome-control-center" startup_notify="false" xdg="true"
?package(%{name}): icon="accessibility-directory" title="Accessibility" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-accessibility-keyboard-properties" icon="gnome-settings-accessibility-keyboard" longtitle="Set your keyboard accessibility preferences" kde_filename="gnome-accessibility-keyboard-properties" title="Keyboard" needs="gnome" section="System/Configuration/GNOME/Accessibility" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-background-properties" icon="gnome-settings-background" longtitle="Customize your desktop background" title="Background" needs="gnome" kde_filename="gnome-background-properties" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-sound-properties" icon="gnome-settings-sound" longtitle="Enable sound and associate sounds with events" title="Sound" needs="gnome" kde_filename="gnome-sound-properties" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-keyboard-properties" icon="gnome-dev-keyboard" longtitle="Set your keyboard preferences" title="Keyboard" needs="gnome" kde_filename="gnome-keyboard-properties" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-mouse-properties" icon="gnome-dev-mouse-optical" longtitle="Set your mouse preferences" title="Mouse" needs="gnome" section="System/Configuration/GNOME" kde_filename="gnome-mouse-properties" startup_notify="true" xdg="true"
?package(%{name}): icon="advanced-directory" longtitle="Advanced Settings" title="Advanced" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-ui-properties" icon="gnome-settings-ui-behavior" longtitle="Customize the appearance of toolbars and menubars in applications" title="Menus & Toolbars" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-theme-manager" icon="gnome-settings-theme" longtitle="Select themes for various parts of the desktop" title="Theme" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-font-properties" icon="gnome-settings-font" longtitle="Select fonts for the desktop" title="Font" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-keybinding-properties" icon="gnome-settings-keybindings" longtitle="Assign shortcut keys to commands" title="Keyboard Shortcuts" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-network-preferences" icon="stock_proxy" longtitle="Network proxy preferences" title="Network proxy" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-default-applications-properties" icon="gnome-settings-default-applications" longtitle="Select your default applications" title="Preferred Applications" needs="gnome" section="System/Configuration/GNOME/Advanced" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-window-properties" icon="gnome-window-manager" longtitle="Window Properties" title="Windows" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-at-properties" icon="gnome-settings-accessibility-technologies" longtitle="Enable support for GNOME assistive technologies at login" title="Assistive Technology Support" needs="gnome" section="System/Configuration/GNOME/Accessibility" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-display-properties" icon="display-capplet" longtitle="Change screen resolution" title="Screen Resolution" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
?package(%{name}): command="%{_bindir}/gnome-about-me" icon="user-info" longtitle="Set your personal information" title="About Me" needs="gnome" section="System/Configuration/GNOME" startup_notify="true" xdg="true"
EOF

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
rm -f $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/*.{la,a} \
 $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/*.{la,a} \
 $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/*.{la,a} \
 $RPM_BUILD_ROOT%{_datadir}/applications/mimeinfo.cache

%clean
rm -rf $RPM_BUILD_ROOT

%post
%define schemas apps_gnome_settings_daemon_default_editor apps_gnome_settings_daemon_keybindings apps_gnome_settings_daemon_screensaver desktop_gnome_font_rendering fontilus themus
%post_install_gconf_schemas %schemas
%{update_menus}
%update_desktop_database
%update_mime_database
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %schemas

%postun
%{clean_menus}
%clean_desktop_database
%clean_mime_database
%clean_icon_cache hicolor

%post -p /sbin/ldconfig -n %{lib_name}

%postun -p /sbin/ldconfig -n %{lib_name}


%files -f %{pkgname}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/*
%config(noreplace) %{_sysconfdir}/xdg/menus/gnomecc.menu
%config(noreplace) %{_sysconfdir}/gnome-vfs-2.0/modules/*
%_bindir/gnome-about-me
%_bindir/gnome-accessibility-keyboard-properties
%_bindir/gnome-at-properties
%_bindir/gnome-background-properties
%_bindir/gnome-control-center
%_bindir/gnome-default-applications-properties
%_bindir/gnome-display-properties
%_bindir/gnome-font-properties
%_bindir/gnome-font-viewer
%_bindir/gnome-keybinding-properties
%_bindir/gnome-keyboard-properties
%_bindir/gnome-mouse-properties
%_bindir/gnome-network-preferences
%_bindir/gnome-sound-properties
%_bindir/gnome-theme-manager
%_bindir/gnome-theme-thumbnailer
%_bindir/gnome-thumbnail-font
%_bindir/gnome-typing-monitor
%_bindir/gnome-ui-properties
%_bindir/gnome-window-properties
%_bindir/themus-theme-applier
%_datadir/icons/hicolor/*/*/*
%{_libexecdir}/gnome-settings-daemon
%{_libdir}/nautilus/extensions-1.0/*.so
%{_libdir}/gnome-vfs-2.0/modules/*.so
%{_libdir}/window-manager-settings/*.so
%_datadir/dbus-1/services/*
%{_datadir}/gnome-background-properties
%{_datadir}/applications/*
%{_datadir}/gnome/cursor-fonts
%{_datadir}/desktop-directories/*
%{_datadir}/pixmaps/*
%_datadir/control-center/
%{_menudir}/*
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%_datadir/mime/packages/*

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/libgnome-window-settings.so.%{lib_major}*
%_libdir/libslab.so.0*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*a
%{_libdir}/pkgconfig/*


