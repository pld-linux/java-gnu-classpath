Summary:	GNU Classpath (Essential Libraries for Java)
Summary(pl):	GNU Classpath (Najwa¿niejsze biblioteki dla Javy)
Name:		classpath
Version:	0.12
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	ce1f7fbe6f2e3b738bae3b46f01a9670
URL:		http://www.gnu.org/software/classpath/classpath.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.7
BuildRequires:	jikes >= 1.18
BuildRequires:	gcc-c++
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gtk+2-devel >= 2.4
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

%build
%configure \
	--enable-static \
	--with-jikes \
	--enable-java \
	--enable-jni \
	--disable-cni \
	--enable-gtk-peer \
	--enable-load-library \
	--disable-debug

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}{/classpath/*,}
for f in libgtkpeer libjavaio libjavalang libjavalangreflect libjavanet libjavanio libjavautil; do
	perl -pi -e "s:^libdir='.*:libdir='%{_libdir}':" $RPM_BUILD_ROOT%{_libdir}/$f.la
done
mv -f $RPM_BUILD_ROOT{%{_datadir}/classpath/glibj.zip,%{_javadir}}

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
%{_infodir}/*

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
