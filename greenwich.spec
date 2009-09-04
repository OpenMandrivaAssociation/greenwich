%define version	0.8.2
%define release  %mkrel 2

Name: 	 	greenwich
Summary: 	A graphical whois client
Version: 	%{version}
Release: 	%{release}
Source:		http://jodrell.net/files/greenwich/%{name}-%{version}.tar.gz
URL:		http://jodrell.net/projects/greenwich/
License:	GPLv2+
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	imagemagick
# may be used but not crucial (according to author)
Suggests:	perl-IP-Country
Requires(post,preun):	GConf2 >= 2.3.3
BuildArch:	noarch

%description
Greenwich is a graphical whois client for GNOME. It is written in Perl
and makes use of the GNOME bindings for Perl.

Greenwich transparently handles almost all gTLDs, first- and
second-level ccTLDs and whois servers run by private domain registries
(like CentralNic).  It can also do lookups against IP addresses.

%prep
%setup -q

# fix file permissions
find -type f -perm +0111 -print0 | xargs -0 -r file | grep -v executable | cut -d: -f1 | xargs -r chmod -x

%build
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}/man1

%find_lang %name

#menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Icon=%{name}
Name=Greenwich
Comment=Whois client
Categories=Network;
EOF

#icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir} \
         $RPM_BUILD_ROOT%{_miconsdir}
install -m 644 -D       share/greenwich.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 share/greenwich.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 share/greenwich.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

#install schemas into gconf later
install -m 644 -D share/greenwich.schema $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas/greenwich.schemas

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%post_install_gconf_schemas greenwich
%endif

%preun
%preun_uninstall_gconf_schemas "$1"

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc ChangeLog LICENSE README
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/*
/usr/lib/greenwich
%{_datadir}/%name
%{_datadir}/applications/*
#%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%{_iconsdir}/*/*/apps/%name.png
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

