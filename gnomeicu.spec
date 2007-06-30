%define version 0.99.10

%define enable_applet 1
%{?_with_applet: %define enable_applet 1}

%define enable_socks 0
#{?_with_plf: #define enable_socks 1}

Name:		gnomeicu
Version:	%{version}
Release:	%mkrel 3
License:	GPL
Summary:	Gnome ICQ communications program 
Group:		Networking/Instant messaging
URL:		http://gnomeicu.sourceforge.net
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

Source:		http://download.sourceforge.net/%{name}/%{version}/src/%{name}-%{version}.tar.bz2
# Icon themes from http://gnomeicu.sf.net/themes/
Source10:	%{name}-eureka.tar.bz2
Source11:	%{name}-mugz.tar.bz2
Source12:	%{name}-penguin.tar.bz2

# (fc) 0.98.126-2mdk use DTD compliant OMF file
Patch0:		gnomeicu-0.98.126-omffix.patch.bz2

Requires(pre):		scrollkeeper >= 0.3.5
Requires(pre):		GConf2 >= 2.3.3
BuildRequires:	ImageMagick
BuildRequires:	gdbm-devel
BuildRequires:	scrollkeeper >= 0.3.5
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	gtkspell-devel >= 2.0.4
BuildRequires:	perl-XML-Parser
BuildRequires:	intltool
BuildRequires:  desktop-file-utils
%if %enable_applet
BuildRequires: gnome-panel-devel
%endif

%if %enable_socks
BuildRequires:	socks5-devel
%endif

%description
GnomeICU is a clone of Mirabilis' popular ICQ.
The original source was taken from Matt Smith's mICQ.

This GTK2 version includes:
- server-side storage
- file send
- contact history
- invisible and ignore lists
- command line interface capability
- icon themes

%if 0
*** Build Options:
--with plf    Enable SOCKSv5 support (default disabled)
                (Get it from PLF: http://plf.zarb.org/)
%endif

%if %enable_applet
%package applet
Summary: Applet for GnomeICU ICQ client
Group: %{group}
Requires: %{name} = %{version}-%{release}

%description applet
GnomeICU is a clone of Mirabilis' popular ICQ.

This package allows GnomeICU to be embedded in GNOME panel.
%endif


%prep
%setup -q
libtoolize --copy --force
autoreconf --force
aclocal
%patch0 -p1 -b .omffix

%build
%configure2_5x \
%if %enable_applet
	--enable-applet \
%endif
%if %enable_socks
	--enable-socks5 \
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# mdk menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): \
command="%{_bindir}/gnomeicu" \
icon="%{name}.png" \
longtitle="GNOME ICQ communications program" \
needs="x11" \
section="Internet/Instant Messaging" \
startup_notify="true" \
title="GnomeICU" \
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Internet-InstantMessaging" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


# convert source icon into mdk menu icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir} \
	 $RPM_BUILD_ROOT%{_liconsdir} \
	 $RPM_BUILD_ROOT%{_miconsdir}
install -m 0644         %name.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 %name.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 %name.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

# icon themes
echo 'Default icons' > $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/Default/gnomeicu-info
tar --bzip2 -xf %{SOURCE10} -C $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/mugz
tar --bzip2 -xf %{SOURCE11} -C $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/mugz
tar --bzip2 -xf %{SOURCE12} -C $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/
find $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/ -type d -print0 | xargs -0 chmod 0755
find $RPM_BUILD_ROOT%{_datadir}/gnomeicu/icons/ -type f -print0 | xargs -0 chmod 0644

%find_lang %name --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gnomeicu.schemas > /dev/null

%preun
if [ $1 -eq 0 ]; then
 GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gnomeicu.schemas > /dev/null
fi

%postun
%clean_menus
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi

%files -f %name.lang
%defattr(-,root,root,755)
%doc AUTHORS ChangeLog COPYING CREDITS INSTALL MAINTAINERS NEWS README* TODO
%config(noreplace) %{_sysconfdir}/sound/events/GnomeICU.soundlist
%{_sysconfdir}/gconf/schemas/gnomeicu.schemas
%{_bindir}/%name
%{_bindir}/%name-client
%{_datadir}/applications/*.desktop
%{_datadir}/%name
%{_datadir}/omf/*
%{_datadir}/pixmaps/*
%{_datadir}/sounds/*
%{_menudir}/*
%{_iconsdir}/%name.png
%{_liconsdir}/%name.png
%{_miconsdir}/%name.png

%if %enable_applet
%files applet
%defattr(-,root,root,755)
%{_libdir}/bonobo/servers/*.server
%{_libexecdir}/gnomeicu-applet
%{_datadir}/gnome-2.0/ui/*.xml
%endif
