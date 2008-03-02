#
# TODO: split (awt-gtk, midi-alsa, midi-dssi, ???-qt, ???-gconf, ???-gstreamer, browser???, tools, devel-tools)
#
# Conditional build:
%bcond_with	gcj	# use gcj instead of jdk  [broken]
%bcond_with	apidocs	# prepare API documentation (over 200MB)
#
Summary:	GNU Classpath (Essential Libraries for Java)
Summary(pl.UTF-8):	GNU Classpath (Najważniejsze biblioteki dla Javy)
Name:		classpath
Version:	0.97
Release:	0.1
License:	GPL v2+ with linking exception
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	a0680ca786d790fbbc99e365a501745a
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/classpath/classpath.html
BuildRequires:	QtCore-devel >= 4.1.0
BuildRequires:	QtGui-devel >= 4.1.0
BuildRequires:	GConf2-devel >= 2.6.0
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.7
BuildRequires:	cairo-devel >= 1.1.8
BuildRequires:	dssi
%{?with_gcj:BuildRequires:	gcc-java >= 5:4.0.2}
%{?with_apidocs:BuildRequires:	gjdoc}
BuildRequires:	gstreamer-devel >= 0.10.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.10
BuildRequires:	gtk+2-devel >= 2:2.8
%{!?with_gcj:BuildRequires:	jdk >= 1.5}
BuildRequires:	libmagic-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1.4.2
BuildRequires:	libxml2-devel >= 1:2.6.8
BuildRequires:	libxslt-devel >= 1.1.11
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	qt4-build >= 4.3.3-3
BuildRequires:	texinfo >= 4.2
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xulrunner-devel >= 1.8
BuildRequires:	zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Classpath (Essential Libraries for Java) is a project to create
free core class libraries for use with virtual machines and compilers
for the Java language. It includes all native methods and core classes
necessary for a completely functional Java runtime.

%description -l pl.UTF-8
GNU Classpath (najważniejsze biblioteki Javy) to projekt stworzenia
wolnodostępnych bibliotek klas podstawowych do wykorzystania z
wirtualnymi maszynami i kompilatorami języka Java. Zawiera wszystkie
natywne metody i główne klasy niezbędne dla kompletnej funkcjonalności
środowiska Javy.

%package apidocs
Summary:	API documentation
Summary(pl.UTF-8):	Dokumentacja API
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description apidocs
Annotated reference of GNU Classpath libraries programming interface including:
- class lists
- class members
- namespaces

%description apidocs -l pl.UTF-8
Dokumentacja interfejsu programowania bibliotek GNU Classpath z przypisami.
Zawiera:
- listy klas i ich składników
- listę przestrzeni nazw (namespace)

%package devel
Summary:	Development files for GNU Classpath
Summary(pl.UTF-8):	Pliki dla programistów używających GNU Classpath
Group:		Development/Libraries
Obsoletes:	classpath-static
# doesn't require base

%description devel
GNU Classpath (Essential Libraries for Java) - development files.

%description devel -l pl.UTF-8
GNU Classpath (Najważniejsze biblioteki dla Javy) - pliki dla
programistów.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	JAVAC="%{?with_gcj:gcj -C}%{!?with_gcj:javac}" \
	MOC=moc-qt4 \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--enable-gstreamer-peer \
	--enable-gtk-peer \
	--enable-java \
	--enable-jni \
	--enable-load-library \
	--enable-qt-peer \
	--enable-xmlj \
	--with%{!?with_apidocs:out}-gjdoc \
	--with-javah=%{?with_gcj:gcjh}%{!?with_gcj:javah} \
	--disable-examples

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{name}-%{version}-apidocs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with apidocs}
cp -afr doc/api/html/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}-apidocs
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/classpath/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKYOU TODO
%dir %{_libdir}/classpath
%attr(755,root,root) %{_libdir}/classpath/libgcjwebplugin.so
%attr(755,root,root) %{_libdir}/classpath/libgconfpeer.so
%attr(755,root,root) %{_libdir}/classpath/libgjsmalsa.so
%attr(755,root,root) %{_libdir}/classpath/libgjsmdssi.so
%attr(755,root,root) %{_libdir}/classpath/libgstreamerpeer.so
%attr(755,root,root) %{_libdir}/classpath/libgtkpeer.so
%attr(755,root,root) %{_libdir}/classpath/libjavaio.so*
%attr(755,root,root) %{_libdir}/classpath/libjavalang.so*
%attr(755,root,root) %{_libdir}/classpath/libjavalangmanagement.so*
%attr(755,root,root) %{_libdir}/classpath/libjavalangreflect.so*
%attr(755,root,root) %{_libdir}/classpath/libjavanet.so*
%attr(755,root,root) %{_libdir}/classpath/libjavanio.so*
%attr(755,root,root) %{_libdir}/classpath/libjavautil.so*
%attr(755,root,root) %{_libdir}/classpath/libjawt.so
%attr(755,root,root) %{_libdir}/classpath/libqtpeer.so
%attr(755,root,root) %{_libdir}/classpath/libxmlj.so*
%dir %{_libdir}/security
%{_libdir}/security/classpath.security
%{_libdir}/logging.properties
%dir %{_datadir}/classpath
%{_datadir}/classpath/glibj.zip
%{_datadir}/classpath/tools.zip

# tools
%attr(755,root,root) %{_bindir}/gappletviewer
%attr(755,root,root) %{_bindir}/gkeytool
%attr(755,root,root) %{_bindir}/gorbd
%attr(755,root,root) %{_bindir}/grmid
%attr(755,root,root) %{_bindir}/grmiregistry
%attr(755,root,root) %{_bindir}/gtnameserv
%{_mandir}/man1/gappletviewer.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmid.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gtnameserv.1*

# tools-devel
%attr(755,root,root) %{_bindir}/gjar
%attr(755,root,root) %{_bindir}/gjarsigner
%attr(755,root,root) %{_bindir}/gjavah
%attr(755,root,root) %{_bindir}/gnative2ascii
%attr(755,root,root) %{_bindir}/grmic
%attr(755,root,root) %{_bindir}/gserialver
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gnative2ascii.1*
%{_mandir}/man1/gserialver.1*
# no bin
#%{_mandir}/man1/gcjh.1*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}-apidocs
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/jawt.h
%{_includedir}/jawt_md.h
%{_includedir}/jni.h
%{_includedir}/jni_md.h
%{_infodir}/cp-hacking.info*
%{_infodir}/cp-tools.info*
%{_infodir}/cp-vmintegration.info*
