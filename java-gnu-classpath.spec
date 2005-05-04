#
# Conditional build:
%bcond_without	gcj	# use jikes instead of gcj
%bcond_with	apidocs	# prepare API documentation (over 200MB)
#
Summary:	GNU Classpath (Essential Libraries for Java)
Summary(pl):	GNU Classpath (Najwa¿niejsze biblioteki dla Javy)
Name:		classpath
Version:	0.15
Release:	2.1
License:	GPL v2
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	036c23aec7cb53a43b7b9dc63a92fbbe
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/classpath/classpath.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.7
BuildRequires:	gcc-c++
%{?with_gcj:BuildRequires:	gcc-java}
BuildRequires:	gdk-pixbuf-devel
%{?with_apidocs:BuildRequires:	gjdoc}
BuildRequires:	gtk+2-devel >= 2:2.4
%{!?with_gcj:BuildRequires:	jikes >= 1.18}
BuildRequires:	libart_lgpl-devel >= 2.1.0
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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKYOU TODO
%attr(755,root,root) %{_libdir}/libgtkpeer.so.*.*.*
%attr(755,root,root) %{_libdir}/libjavaio.so.*.*.*
%attr(755,root,root) %{_libdir}/libjavalang.so.*.*.*
%attr(755,root,root) %{_libdir}/libjavalangreflect.so.*.*.*
%attr(755,root,root) %{_libdir}/libjavanet.so.*.*.*
%attr(755,root,root) %{_libdir}/libjavanio.so.*.*.*
%attr(755,root,root) %{_libdir}/libjavautil.so.*.*.*
%{_javadir}/glibj.zip
%{_infodir}/*.info*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}-apidocs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgtkpeer.la
%{_libdir}/libgtkpeer.so
%{_libdir}/libjavaio.la
%{_libdir}/libjavaio.so
%{_libdir}/libjavalang.la
%{_libdir}/libjavalang.so
%{_libdir}/libjavalangreflect.la
%{_libdir}/libjavalangreflect.so
%{_libdir}/libjavanet.la
%{_libdir}/libjavanet.so
%{_libdir}/libjavanio.la
%{_libdir}/libjavanio.so
%{_libdir}/libjavautil.la
%{_libdir}/libjavautil.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libgtkpeer.a
%{_libdir}/libjavaio.a
%{_libdir}/libjavalang.a
%{_libdir}/libjavalangreflect.a
%{_libdir}/libjavanet.a
%{_libdir}/libjavanio.a
%{_libdir}/libjavautil.a
