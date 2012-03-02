%define major	1
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary: GNOME control center
Name: gnome-control-center
Version: 3.2.2
Release: 1
License: GPLv2+
Group: Graphical desktop/GNOME
URL: http://www.gnome.org/softwaremap/projects/control-center/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	shared-mime-info
BuildRequires:	cups-devel
BuildRequires:	pkgconfig(cheese-gtk) >= 2.91.91.1
BuildRequires:	pkgconfig(colord) >= 0.1.8
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.23.0
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.14
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.1.0
BuildRequires:	pkgconfig(gnome-settings-daemon) >= 0.97
BuildRequires:	pkgconfig(goa-backend-1.0)
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

Requires: gnome-settings-daemon >= 2.21.5
Requires(post): shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils

%description
GNOME Control-center is a configuration tool for easily
setting up your GNOME environment.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries

%description -n %{libname}
Dynamic libraries used by GNOME Control Center

%package -n %{develname}
Summary:	Development libraries, include files for GNOME control center
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development libraries, include files for GNOME Control Center

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--disable-scrollkeeper

%make

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name '*.la' -exec rm -f {} \;
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache

%{find_lang} %{name}-2.0 --with-gnome --all-name

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--remove-category="PersonalSettings" \
	--add-category="X-MandrivaLinux-System-Configuration-GNOME" \
	--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%files -f %{name}-2.0.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/xdg/autostart/gnome-sound-applet.desktop
%{_sysconfdir}/xdg/menus/gnomecc.menu
%{_libdir}/control-center-1/panels/libbackground.so
#{_libdir}/control-center-1/panels/libbluetooth.so
%{_libdir}/control-center-1/panels/libcolor.so
%{_libdir}/control-center-1/panels/libdate_time.so
%{_libdir}/control-center-1/panels/libdisplay.so
%{_libdir}/control-center-1/panels/libinfo.so
%{_libdir}/control-center-1/panels/libkeyboard.so
%{_libdir}/control-center-1/panels/libmedia.so
%{_libdir}/control-center-1/panels/libmouse-properties.so
%{_libdir}/control-center-1/panels/libonline-accounts.so
%{_libdir}/control-center-1/panels/libpower.so
%{_libdir}/control-center-1/panels/libprinters.so
%{_libdir}/control-center-1/panels/libregion.so
%{_libdir}/control-center-1/panels/libscreen.so
%{_libdir}/control-center-1/panels/libsound.so
%{_libdir}/control-center-1/panels/libuniversal-access.so
%{_libdir}/control-center-1/panels/libuser-accounts.so
%{_libdir}/control-center-1/panels/libwacom-properties.so
%{_libdir}/control-center-1/panels/libnetwork.so
%{_bindir}/gnome-control-center
%{_bindir}/gnome-sound-applet
%{_datadir}/applications/*
%{_datadir}/desktop-directories/*
%{_datadir}/gnome-control-center/
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/sounds/gnome/default/*
%{_datadir}/pixmaps/faces

%files -n %{libname}
%{_libdir}/libgnome-control-center.so.%{major}*

%files -n %{develname}
%doc ChangeLog
%{_libdir}/*.so
%{_datadir}/pkgconfig/*

