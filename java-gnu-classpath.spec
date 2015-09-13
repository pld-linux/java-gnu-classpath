#
# TODO:
# - split (awt-gtk, midi-alsa, midi-dssi, ???-qt, ???-gconf, ???-gstreamer, browser???)
#
# NOTE:
# - do not package gjdoc. This version of gjdoc is devel. See gjdoc.spec for
#   stable version.
#
# Conditional build:
%bcond_with	gcj		# use gcj instead of jdk  [broken]
%bcond_with	gjdoc		# build gjdoc here (instead of external gjdoc package)
%bcond_with	webplugin	# build gcjwebplugin [uses obsolete NPAPI]
%bcond_with	apidocs		# prepare API documentation (over 200MB)

%define		srcname	classpath
Summary:	GNU Classpath (Essential Libraries for Java)
Summary(pl.UTF-8):	GNU Classpath (Najważniejsze biblioteki dla Javy)
Name:		java-gnu-classpath
Version:	0.99
Release:	2
License:	GPL v2+ with linking exception
Group:		Libraries/Java
Source0:	http://ftp.gnu.org/gnu/classpath/%{srcname}-%{version}.tar.gz
# Source0-md5:	0ae1571249172acd82488724a3b8acb4
Patch0:		%{srcname}-info.patch
URL:		http://www.gnu.org/software/classpath/classpath.html
BuildRequires:	GConf2-devel >= 2.6.0
BuildRequires:	QtCore-devel >= 4.1.0
BuildRequires:	QtGui-devel >= 4.1.0
BuildRequires:	alsa-lib-devel
# cantrl, runantlr or antlr
%{?with_gjdoc:BuildRequires:	antlr >= 2.7.1}
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.9
BuildRequires:	cairo-devel >= 1.1.8
BuildRequires:	dssi-devel
BuildRequires:	freetype-devel >= 2
%{?with_gcj:BuildRequires:	gcc-java >= 5:4.0.2}
BuildRequires:	gdk-pixbuf2-devel >= 2.0
%if %{with apidocs} && %{without gjdoc}
BuildRequires:	gjdoc
%endif
BuildRequires:	glib2-devel >= 1:2.2
BuildRequires:	gmp-devel >= 3.1
BuildRequires:	gstreamer0.10-devel >= 0.10.10
BuildRequires:	gstreamer0.10-plugins-base-devel >= 0.10.10
BuildRequires:	gtk+2-devel >= 2:2.8
%{!?with_gcj:BuildRequires:	jdk >= 1.5}
BuildRequires:	libmagic-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 1:2.6.8
BuildRequires:	libxslt-devel >= 1.1.11
BuildRequires:	pango-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	qt4-build >= 4.3.3-3
BuildRequires:	texinfo >= 4.2
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
# pkgconfig: one of mozilla-plugin, ((mozilla-)?firefox|xulrunner|seamonkey|iceape)-{plugin,xpcom}
%{?with_webplugin:BuildRequires:	xulrunner-devel >= 1.8}
BuildRequires:	zip
Requires:	jpackage-utils
Provides:	jre-X11
Provides:	jre-alsa
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# JNI_GetCreatedJavaVMs
%define		skip_post_check_so	libxmlj.so.*

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
Annotated reference of GNU Classpath libraries programming interface
including:
- class lists
- class members
- namespaces

%description apidocs -l pl.UTF-8
Dokumentacja interfejsu programowania bibliotek GNU Classpath z
przypisami. Zawiera:
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

%package tools
Summary:	Shared Java tools
Summary(pl.UTF-8):	Współdzielone narzędzia Javy
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Provides:	jar
Provides:	java-jre-tools
Provides:	java-shared
Obsoletes:	fastjar
Obsoletes:	jar
Obsoletes:	java-jre-tools
Obsoletes:	java-shared

%description tools
Java tools - GNU Classpath implementation.

%description tools -l pl.UTF-8
Narzędzia Javy - implementacja GNU Classpath.

%package tools-devel
Summary:	Shared Java development tools
Summary(pl.UTF-8):	Współdzielone narzędzia programistyczne Javy
Group:		Development/Languages/Java
Requires:	%{name}-tools = %{version}-%{release}

%description tools-devel
Java development tools - GNU Classpath implementation.

%description tools-devel -l pl.UTF-8
Narzędzia programistyczne Javy - implementacja GNU Classpath.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1

%build
ECJ_JAR=$(find-jar ecj)

%configure \
	JAVAC="%{?with_gcj:gcj -C}%{!?with_gcj:javac}" \
	MOC=moc-qt4 \
	--disable-Werror \
	--enable-debug%{!?debug:=no} \
	%{!?with_gjdoc:--disable-gjdoc} \
	--enable-gstreamer-peer \
	--enable-gtk-peer \
	--enable-jni \
	--enable-load-library \
	%{?with_webplugin:--enable-plugin} \
	--enable-qt-peer \
	--enable-xmlj \
	--with-gjdoc%{!?with_apidocs:=no} \
	--with-javah=%{?with_gcj:gcjh}%{!?with_gcj:javah} \
	--with-ecj-jar=$ECJ_JAR \
	--disable-examples

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{srcname}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s %{_datadir}/classpath/glibj.zip $RPM_BUILD_ROOT%{_javadir}/glibj.jar
ln -s %{_datadir}/classpath/tools.zip $RPM_BUILD_ROOT%{_javadir}/tools.jar

%if %{with apidocs}
cp -afr doc/api/html/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# native modules for Java, no need for .la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/classpath/*.la

# no binary here, belongs to gcc-java
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/gcjh.1

%if %{without gjdoc}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/gjdoc.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post apidocs
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKYOU TODO
%dir %{_libdir}/classpath
%{?with_webplugin:%attr(755,root,root) %{_libdir}/classpath/libgcjwebplugin.so}
%attr(755,root,root) %{_libdir}/classpath/libgconfpeer.so
%attr(755,root,root) %{_libdir}/classpath/libgjsmalsa.so
%attr(755,root,root) %{_libdir}/classpath/libgjsmdssi.so
%attr(755,root,root) %{_libdir}/classpath/libgstreamerpeer.so
%attr(755,root,root) %{_libdir}/classpath/libgtkpeer.so
%attr(755,root,root) %{_libdir}/classpath/libjavaio.so*
%attr(755,root,root) %{_libdir}/classpath/libjavalang.so*
%attr(755,root,root) %{_libdir}/classpath/libjavalangmanagement.so*
%attr(755,root,root) %{_libdir}/classpath/libjavalangreflect.so*
%attr(755,root,root) %{_libdir}/classpath/libjavamath.so
%attr(755,root,root) %{_libdir}/classpath/libjavanet.so*
%attr(755,root,root) %{_libdir}/classpath/libjavanio.so*
%attr(755,root,root) %{_libdir}/classpath/libjavautil.so*
%attr(755,root,root) %{_libdir}/classpath/libjawt.so
%attr(755,root,root) %{_libdir}/classpath/libqtpeer.so
%attr(755,root,root) %{_libdir}/classpath/libxmlj.so*
%dir %{_datadir}/classpath
%{_datadir}/classpath/glibj.zip
%{_datadir}/classpath/tools.zip
%{_javadir}/glibj.jar
%{_javadir}/tools.jar
# Following files are in /usr/lib, not in %{_libdir}.
%dir /usr/lib/security
/usr/lib/security/classpath.security
/usr/lib/logging.properties

%files tools
%defattr(644,root,root,755)
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

%files tools-devel
%defattr(644,root,root,755)
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
%if %{with gjdoc}
%attr(755,root,root) %{_bindir}/gjdoc
%{_mandir}/man1/gjdoc.1*
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
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
