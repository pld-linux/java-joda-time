# TODO:
# - take a closer look at tests
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif
#
%include	/usr/lib/rpm/macros.java

%define		srcname		joda-time
Summary:	Java JDK Date and Time replacement
Name:		java-joda-time
Version:	1.6
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/project/joda-time/joda-time/%{version}/%{srcname}-%{version}-src.tar.gz
# Source0-md5:	8e59de208eb994010575e34179f2b580
URL:		http://joda-time.sourceforge.net/
BuildRequires:	ant
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
# NOT only for tests. If not present ant will try to download it.
BuildRequires:	java-junit
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
# for %{_javadir}
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Joda-Time provides a library of classes to replace the Java JDK Date
and Time classes including formatting. It is based around the ISO8601
datetime standard, but also provides full support for other calendar
systems, such as Gregorian and Buddhist.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%prep
%setup -q -n %{srcname}-%{version}-src

%build
export JAVA_HOME="%{java_home}"

JUNIT_JAR=$(find-jar junit)

%ant -Djunit.jar=$JUNIT_JAR
%{?with_javadoc:%ant -Djunit.jar=$JUNIT_JAR javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a build/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
