#
# TODO:
#		- classpathx (spec or source1+subpkg?)
#
Summary:	GNU Classpath (Essential Libraries for Java)
Name:		classpath
Version:	0.10
Release:	0.1
Epoch:		0
License:	GPL v2
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/classpath/%{name}-%{version}.tar.gz
# Source0-md5:	a59a5040f9c1237dbf27bfc668919943
URL:		http://www.gnu.org/software/classpath/classpath.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.7
BuildRequires:	gcc-java
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gtk+2-devel >= 2.2
BuildRequires:	libart_lgpl-devel >= 2.1.0
BuildRequires:	libtool >= 1.4.2
BuildRequires:	texinfo >= 4.2
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	java-sun-jre
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Classpath (Essential Libraries for Java) is a project to create
free core class libraries for use with virtual machines and compilers
for the Java language. It includes all native methods and core classes
necessary for a completely functional Java runtime.

%prep
%setup -q

%build
#%%{__gettextize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
%configure \
	--with-gcj \
	--enable-java \
	--enable-jni \
	--disable-cni \
	--enable-gtk-peer \
	--enable-load-library \
	--disable-debug
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
#attr(755,root,root) %{_bindir}/*
#{_datadir}/%{name}
