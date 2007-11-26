%define version	0.8.1
%define release 1mdk

Name: 	 	greenwich
Summary: 	A graphical whois client
Version: 	%{version}
Release: 	%{release}
Source:		http://jodrell.net/files/greenwich/%{name}-%{version}.tar.bz2
Patch0:		greenwich-0.8.0-no-install-schema.patch.bz2
URL:		http://jodrell.net/projects/greenwich/
License:	GPL
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ImageMagick
# may be used but not crucial (according to author)
#Requires:	perl-IP-Country
Prereq:		GConf2 >= 2.3.3
BuildArch:	noarch

%description
Greenwich is a graphical whois client for GNOME. It is written in Perl
and makes use of the GNOME bindings for Perl.

Greenwich transparently handles almost all gTLDs, first- and
second-level ccTLDs and whois servers run by private domain registries
(like CentralNic).  It can also do lookups against IP addresses.

%prep
%setup -q
%patch0 -p1 -b .no-install-schemas

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
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="%{name}" icon="%{name}.png" needs="x11" title="Greenwich" longtitle="Whois client" section="Internet/Other"
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

%post
%update_menus
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
for SCHEMA in greenwich; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/${SCHEMA}.schemas > /dev/null
done

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  for SCHEMA in greenwich; do
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/${SCHEMA}.schemas > /dev/null
  done
fi

%postun
%clean_menus

%files -f %name.lang
%defattr(-,root,root)
%doc ChangeLog LICENSE README
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/*
%{_libdir}/%name
%{_datadir}/%name
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%{_menudir}/%name
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

