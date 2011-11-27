%define pkgname control-center
%define lib_major	1
%define libname	%mklibname gnome-window-settings %{lib_major}
%define develname %mklibname -d gnome-window-settings

Summary: GNOME control center
Name: gnome-%{pkgname}
Version: 3.2.2
Release: 1
License: GPLv2+
Group: Graphical desktop/GNOME
URL: http://www.gnome.org/softwaremap/projects/control-center/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
Source1: backgrounds.xml

BuildRequires:	desktop-file-utils
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	shared-mime-info
BuildRequires:	cups-devel
BuildRequires:	pkgconfig(cheese-gtk) >= 2.91.91.1
BuildRequires:	pkgconfig(colord) >= 0.1.8
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.23.0
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.14
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.1.0
BuildRequires:	pkgconfig(gnome-settings-daemon) >= 0.97
BuildRequires:	pkgconfig(goa-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.13
BuildRequires:	pkgconfig(libgnome-menu-3.0)
BuildRequires:	pkgconfig(libgnomekbd) >= 2.91.91
BuildRequires:	pkgconfig(libgnomekbdui) >= 2.91.91
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(libnm-glib) >= 0.8.992
BuildRequires:	pkgconfig(libnm-glib-vpn) => 0.8.992
BuildRequires:	pkgconfig(libnm-util) >= 0.8.992
BuildRequires:	pkgconfig(libnm-gtk) >= 0.8.992
BuildRequires:	pkgconfig(libnotify) >= 0.7.3
BuildRequires:	pkgconfig(libpulse) >= 0.9.16
BuildRequires:	pkgconfig(libpulse-mainloop-glib) >= 0.9.16
BuildRequires:	pkgconfig(libxklavier) >= 5.1
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(NetworkManager) >= 0.8.992
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.97
BuildRequires:	pkgconfig(upower-glib) >= 0.9.1
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi) >= 1.2

#BuildRequires:  evolution-data-server-devel >= 1.5.3
#BuildRequires:  libmetacity-private-devel >= 2.23.1
#BuildRequires:  nautilus-devel >= 2.9.0
#BuildRequires:  libxxf86misc-devel                                             
#BuildRequires:  libxscrnsaver-devel
#BuildRequires:  gnome-panel-devel
#BuildRequires:  gnome-common
#BuildRequires:	gettext-devel
#BuildRequires:  unique-devel
#BuildRequires:  librsvg-devel

Requires: gnome-settings-daemon >= 2.21.5
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

%package -n %{develname}
Summary:	Development libraries, include files for GNOME control center
Group:		Development/GNOME and GTK+
Provides:	libgnome-window-settings-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname -d gnome-window-settings 1
Conflicts:	%{mklibname -d gnome-main-menu} <= 0.9.12-2mdv2009.1

%description -n %{develname}
Development libraries, include files for GNOME Control Center

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-scrollkeeper \
	--disable-static

%make

%install
rm -rf %{buildroot}
%makeinstall_std UPDATE_MIME_DATABASE=true
find %{buildroot} -name '*.la' -exec rm -f {} \;
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache

%{find_lang} %{pkgname}-2.0 --with-gnome --all-name
for omf in $(ls %{buildroot}%{_datadir}/omf/*/*.omf|fgrep -v -- -C.omf);do 
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%{buildroot}!!)" >> %{pkgname}-2.0.lang
done

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="PersonalSettings" \
  --add-category="X-MandrivaLinux-System-Configuration-GNOME" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --remove-category="X-MandrivaLinux-System-Configuration-GNOME" \
  --add-category="X-MandrivaLinux-System-Configuration-GNOME-Accessibility" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/at-properties.desktop 

# does this matter anymore?
mkdir -p %{buildroot}%{_datadir}/gnome-background-properties
cp %{SOURCE1} %{buildroot}%{_datadir}/gnome-background-properties/

%post
%define schemas control-center fontilus gnome-control-center

%preun
%preun_uninstall_gconf_schemas %schemas

%files -f %{pkgname}-2.0.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/control-center.schemas
%{_sysconfdir}/gconf/schemas/fontilus.schemas
%{_sysconfdir}/gconf/schemas/gnome-control-center.schemas
%config(noreplace) %{_sysconfdir}/xdg/menus/gnomecc.menu
%config(noreplace) %{_sysconfdir}/xdg/autostart/gnome-at-session.desktop
%{_bindir}/gnome-about-me
%{_bindir}/gnome-appearance-properties
%{_bindir}/gnome-at-mobility
%{_bindir}/gnome-at-properties
%{_bindir}/gnome-at-visual
%{_bindir}/gnome-control-center
%{_bindir}/gnome-default-applications-properties
%{_bindir}/gnome-display-properties
%{_bindir}/gnome-font-viewer
%{_bindir}/gnome-keybinding-properties
%{_bindir}/gnome-keyboard-properties
%{_bindir}/gnome-mouse-properties
%{_bindir}/gnome-network-properties
%{_bindir}/gnome-thumbnail-font
%{_bindir}/gnome-typing-monitor
%{_bindir}/gnome-window-properties
%{_libdir}/window-manager-settings/libmetacity.so
%{_sbindir}/gnome-display-properties-install-systemwide
%{_datadir}/polkit-1/actions/org.gnome.randr.policy
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/gnome-background-properties
%{_datadir}/applications/*
%{_datadir}/desktop-directories/*
%{_datadir}/gnome-control-center/
%dir %{_datadir}/gnome/cursor-fonts/
%{_datadir}/gnome/cursor-fonts/*
%{_datadir}/mime/packages/gnome-theme-package.xml
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf

%files -n %{libname}
%{_libdir}/libgnome-window-settings.so.%{lib_major}*

%files -n %{develname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/pkgconfig/*

