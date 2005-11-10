#
# Conditional build:
%bcond_without	gcj	# use jikes instead of gcj
%bcond_with	apidocs	# prepare API documentation (over 200MB)
#
Summary:	GNU Classpath (Essential Libraries for Java)
Summary(pl):	GNU Classpath (Najwa¿niejsze biblioteki dla Javy)
Name:		classpath
Version:	0.19
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	0b93b1c1dd3d33ef7fb6a47dbb29e41d
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/classpath/classpath.html
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.7
BuildRequires:	gcc-c++
%{?with_gcj:BuildRequires:	gcc-java >= 5:4.0.2}
%{?with_apidocs:BuildRequires:	gjdoc}
BuildRequires:	gtk+2-devel >= 2:2.4
%{!?with_gcj:BuildRequires:	jikes >= 1.18}
BuildRequires:	libtool >= 1.4.2
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	texinfo >= 4.2
BuildRequires:	zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Classpath (Essential Libraries for Java) is a project to create
free core class libraries for use with virtual machines and compilers
for the Java language. It includes all native methods and core classes
necessary for a completely functional Java runtime.

%description -l pl
GNU Classpath (Najwa¿niejsze biblioteki javy) to projekt stworzenia
wolnego j±dra klas bibliotek do wykorzystania z wirtualnymi maszynami
i kompilatorami dla jêzyka Java. Zawiera wszystkie natywne metody i
g³ówne klasy niezbêdne dla kompletnej funkcjonalno¶ci ¶rodowiska Javy.

%package apidocs
Summary:	API documentation
Summary(pl):	Dokumentacja API
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description apidocs
Annotated reference of GNU Classpath libraries programming interface including:
- class lists
- class members
- namespaces

%description apidocs -l pl
Dokumentacja interfejsu programowania bibliotek GNU Classpath z przypisami.
Zawiera:
- listy klas i ich sk³adników
- listê przestrzeni nazw (namespace)

%package devel
Summary:	Development files for GNU Classpath
Summary(pl):	Pliki dla programistów u¿ywaj±cych GNU Classpath
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
GNU Classpath (Essential Libraries for Java) - development files.

%description devel -l pl
GNU Classpath (Najwa¿niejsze biblioteki dla Javy) - pliki dla
programistów.

%package static
Summary:	Static libraries for GNU Classpath
Summary(pl):	Biblioteki statyczne dla GNU Classpath
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
GNU Classpath (Essential Libraries for Java) - static libraries.

%description static -l pl
GNU Classpath (Najwa¿niejsze biblioteki dla Javy) - biblioteki
statyczne.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-cni \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--enable-gtk-peer \
	--enable-java \
	--enable-jni \
	--enable-load-library \
	--enable-static \
	--without-ecj \
%if %{with gcj}
	--with-gcj \
	--without-jikes \
%else
	--without-gcj \
	--with-jikes \
%endif
	--with%{!?with_apidocs:out}-gjdoc \
	--disable-examples

%{__make} \
	pkglibdir=%{_libdir} \
	pkgdatadir=%{_javadir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{name}-%{version}-apidocs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkglibdir=%{_libdir} \
	pkgdatadir=%{_javadir}

%if %{with apidocs}
cp -afr doc/api/html/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}-apidocs
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun	devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKYOU TODO
%attr(755,root,root) %{_libdir}/classpath/libgjsmalsa.so.*.*.*
%attr(755,root,root) %{_libdir}/classpath/libgtkpeer.so.*.*.*
%attr(755,root,root) %{_libdir}/classpath/libjavaio.so.*.*.*
%attr(755,root,root) %{_libdir}/classpath/libjavalang.so.*.*.*
%attr(755,root,root) %{_libdir}/classpath/libjavalangreflect.so.*.*.*
%attr(755,root,root) %{_libdir}/classpath/libjavanet.so.*.*.*
%attr(755,root,root) %{_libdir}/classpath/libjavanio.so.*.*.*
%attr(755,root,root) %{_libdir}/classpath/libjavautil.so.*.*.*
%attr(755,root,root) %{_libdir}/classpath/libjawtgnu.so.*.*.*
%{_datadir}/classpath/glibj.zip

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}-apidocs
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/classpath/libgjsmalsa.so
%attr(755,root,root) %{_libdir}/classpath/libgtkpeer.so
%attr(755,root,root) %{_libdir}/classpath/libjavaio.so
%attr(755,root,root) %{_libdir}/classpath/libjavalang.so
%attr(755,root,root) %{_libdir}/classpath/libjavalangreflect.so
%attr(755,root,root) %{_libdir}/classpath/libjavanet.so
%attr(755,root,root) %{_libdir}/classpath/libjavanio.so
%attr(755,root,root) %{_libdir}/classpath/libjavautil.so
%attr(755,root,root) %{_libdir}/classpath/libjawtgnu.so
%{_libdir}/classpath/libgjsmalsa.la
%{_libdir}/classpath/libgtkpeer.la
%{_libdir}/classpath/libjavaio.la
%{_libdir}/classpath/libjavalang.la
%{_libdir}/classpath/libjavalangreflect.la
%{_libdir}/classpath/libjavanet.la
%{_libdir}/classpath/libjavanio.la
%{_libdir}/classpath/libjavautil.la
%{_libdir}/classpath/libjawtgnu.la
%{_includedir}/*.h
%{_infodir}/*.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/classpath/libgjsmalsa.a
%{_libdir}/classpath/libgtkpeer.a
%{_libdir}/classpath/libjavaio.a
%{_libdir}/classpath/libjavalang.a
%{_libdir}/classpath/libjavalangreflect.a
%{_libdir}/classpath/libjavanet.a
%{_libdir}/classpath/libjavanio.a
%{_libdir}/classpath/libjavautil.a
%{_libdir}/classpath/libjawtgnu.a
