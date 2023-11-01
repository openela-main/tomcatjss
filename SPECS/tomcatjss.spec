################################################################################
Name:             tomcatjss
################################################################################

Summary:          JSS Connector for Apache Tomcat
URL:              http://www.dogtagpki.org/wiki/TomcatJSS
License:          LGPLv2+
BuildArch:        noarch

# For development (i.e. unsupported) releases, use x.y.z-0.n.<phase>.
# For official (i.e. supported) releases, use x.y.z-r where r >=1.
Version:          7.7.1
Release:          1%{?_timestamp}%{?_commit_id}%{?dist}
#global           _phase -alpha1

# To generate the source tarball:
# $ git clone https://github.com/dogtagpki/tomcatjss.git
# $ cd tomcatjss
# $ git archive \
#     --format=tar.gz \
#     --prefix tomcatjss-VERSION/ \
#     -o tomcatjss-VERSION.tar.gz \
#     <version tag>
Source:           https://github.com/dogtagpki/tomcatjss/archive/v%{version}%{?_phase}/tomcatjss-%{version}%{?_phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > tomcatjss-VERSION-RELEASE.patch
# Patch: tomcatjss-VERSION-RELEASE.patch

################################################################################
# Java
################################################################################

%if 0%{?fedora} && 0%{?fedora} <= 32 || 0%{?rhel} && 0%{?rhel} <= 8
%define java_devel java-1.8.0-openjdk-devel
%define java_headless java-1.8.0-openjdk-headless
%define java_home /usr/lib/jvm/jre-1.8.0-openjdk
%else
%define java_devel java-11-openjdk-devel
%define java_headless java-11-openjdk-headless
%define java_home /usr/lib/jvm/jre-11-openjdk
%endif

################################################################################
# Build Dependencies
################################################################################

# jpackage-utils requires versioning to meet both build and runtime requirements
# jss requires versioning to meet both build and runtime requirements
# tomcat requires versioning to meet both build and runtime requirements

# Java
BuildRequires:    ant
BuildRequires:    apache-commons-lang3
BuildRequires:    %{java_devel}
BuildRequires:    jpackage-utils >= 0:1.7.5-15

# SLF4J
BuildRequires:    slf4j
BuildRequires:    slf4j-jdk14

# JSS
BuildRequires:    jss >= 4.9.0, jss < 5.0.0

# Tomcat
%if 0%{?rhel} && ! 0%{?eln}
BuildRequires:    pki-servlet-engine >= 1:9.0.7
%else
BuildRequires:    tomcat >= 1:9.0.7
%endif

################################################################################
# Runtime Dependencies
################################################################################

# Java
Requires:         apache-commons-lang3
Requires:         %{java_headless}
Requires:         jpackage-utils >= 0:1.7.5-15

# SLF4J
Requires:         slf4j
Requires:         slf4j-jdk14

# JSS
Requires:         jss >= 4.9.0, jss < 5.0.0

# Tomcat
%if 0%{?rhel} && ! 0%{?eln}
Requires:         pki-servlet-engine >= 1:9.0.7
%else
Requires:         tomcat >= 1:9.0.7
%endif

# PKI
Conflicts:        pki-base < 10.10.0


%if 0%{?rhel}
# For EPEL, override the '_sharedstatedir' macro on RHEL
%define           _sharedstatedir    /var/lib
%endif

%description
JSS Connector for Apache Tomcat, installed via the tomcatjss package,
is a Java Secure Socket Extension (JSSE) module for Apache Tomcat that
uses Java Security Services (JSS), a Java interface to Network Security
Services (NSS).

################################################################################
%prep
################################################################################

%autosetup -n tomcatjss-%{version}%{?_phase} -p 1

################################################################################
%install
################################################################################

# get Tomcat <major>.<minor> version number
tomcat_version=`/usr/sbin/tomcat version | sed -n 's/Server number: *\([0-9]\+\.[0-9]\+\).*/\1/p'`
app_server=tomcat-$tomcat_version

ant -f build.xml \
    -Dversion=%{version} \
    -Dsrc.dir=$app_server \
    -Djnidir=%{_jnidir} \
    -Dinstall.doc.dir=%{buildroot}%{_docdir}/%{name} \
    -Dinstall.jar.dir=%{buildroot}%{_javadir} \
    install

################################################################################
%files
################################################################################

%license LICENSE

%defattr(-,root,root)
%doc README
%doc LICENSE
%{_javadir}/*

################################################################################
%changelog
* Mon Nov 15 2021 Red Hat PKI Team <rhcs-maint@redhat.com> 7.7.1-1
- Rebase to TomcatJSS 7.7.1

* Mon Jul 26 2021 Red Hat PKI Team <rhcs-maint@redhat.com> 7.7.0-1
- Rebase to TomcatJSS 7.7.0

* Fri Jun 11 2021 Red Hat PKI Team <rhcs-maint@redhat.com> 7.7.0-0.1
- Rebase to TomcatJSS 7.7.0-alpha1

* Tue Nov 17 2020 Red Hat PKI Team <rhcs-maint@redhat.com> 7.6.1-1
- Rebase to TomcatJSS 7.6.1

* Wed Oct 28 2020 Red Hat PKI Team <rhcs-maint@redhat.com> 7.6.0-2
- Bump dependency to JSS 4.8.0
- Remove unsupported platforms

* Tue Oct 20 2020 Red Hat PKI Team <rhcs-maint@redhat.com> 7.6.0-1
- Rebase to TomcatJSS 7.6.0

* Thu Jul 09 2020 Red Hat PKI Team <rhcs-maint@redhat.com> 7.5.0-1
- Rebase to TomcatJSS 7.5.0

* Thu Jun 25 2020 Red Hat PKI Team <rhcs-maint@redhat.com> 7.5.0-0.2
- Rebase to TomcatJSS 7.5.0-a2

* Tue May 26 2020 Red Hat PKI Team <rhcs-maint@redhat.com> 7.5.0-0.1
- Rebase to TomcatJSS 7.5.0-a1

* Thu Oct 31 2019 Red Hat PKI Team <rhcs-maint@redhat.com> 7.4.1-2
- Bump dependency to JSS 4.6.0

* Wed Jun 12 2019 Red Hat PKI Team <rhcs-maint@redhat.com> 7.4.1-1
- Rebase to TomcatJSS 7.4.1

* Wed Apr 24 2019 Red Hat PKI Team <rhcs-maint@redhat.com> 7.4.0-1
- Rebase to TomcatJSS 7.4.0

* Fri Oct 05 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.6-1
- Rebase to TomcatJSS 7.3.6

* Mon Aug 13 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.5-1
- Rebase to TomcatJSS 7.3.5

* Tue Aug 07 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.4-1
- Rebase to TomcatJSS 7.3.4

* Tue Aug 07 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.3-2
- Red Hat Bugzilla #1612063 - Do not override system crypto policy (support TLS 1.3)

* Fri Jul 20 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.3-1
- Rebase to TomcatJSS 7.3.3

* Thu Jul 05 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.2-1
- Rebase to TomcatJSS 7.3.2

* Fri Jun 15 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.1-1
- Fix Tomcat dependencies
- Rebase to TomcatJSS 7.3.1

* Thu Apr 12 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.0-1
- Clean up spec file
- Rebase to TomcatJSS 7.3.0 final

* Thu Mar 15 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 7.3.0-0.2
- Rebase to TomcatJSS 7.3.0 beta
