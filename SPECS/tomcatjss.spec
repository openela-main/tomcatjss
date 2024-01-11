################################################################################
Name:             tomcatjss
################################################################################

%global           product_id idm-tomcatjss

# Upstream version number:
%global           major_version 8
%global           minor_version 3
%global           update_version 0

# Downstream release number:
# - development/stabilization (unsupported): 0.<n> where n >= 1
# - GA/update (supported): <n> where n >= 1
%global           release_number 1

# Development phase:
# - development (unsupported): alpha<n> where n >= 1
# - stabilization (unsupported): beta<n> where n >= 1
# - GA/update (supported): <none>
#global           phase

%undefine         timestamp
%undefine         commit_id

Summary:          JSS Connector for Apache Tomcat
URL:              https://github.com/dogtagpki/tomcatjss
License:          LGPLv2+
Version:          %{major_version}.%{minor_version}.%{update_version}
Release:          %{release_number}%{?phase:.}%{?phase}%{?timestamp:.}%{?timestamp}%{?commit_id:.}%{?commit_id}%{?dist}

# To generate the source tarball:
# $ git clone https://github.com/dogtagpki/tomcatjss.git
# $ cd tomcatjss
# $ git archive \
#     --format=tar.gz \
#     --prefix tomcatjss-VERSION/ \
#     -o tomcatjss-VERSION.tar.gz \
#     <version tag>
Source:           https://github.com/dogtagpki/tomcatjss/archive/v%{version}%{?phase:-}%{?phase}/tomcatjss-%{version}%{?phase:-}%{?phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > tomcatjss-VERSION-RELEASE.patch
# Patch: tomcatjss-VERSION-RELEASE.patch

BuildArch:        noarch

################################################################################
# Java
################################################################################

%define java_devel java-17-openjdk-devel
%define java_headless java-17-openjdk-headless
%define java_home %{_jvmdir}/jre-17-openjdk

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
BuildRequires:    jss = 5.3

# Tomcat
%if 0%{?rhel} && ! 0%{?eln}
BuildRequires:    pki-servlet-engine >= 1:9.0.7
%else
BuildRequires:    tomcat >= 1:9.0.7
%endif

%description
JSS Connector for Apache Tomcat, installed via the tomcatjss package,
is a Java Secure Socket Extension (JSSE) module for Apache Tomcat that
uses Java Security Services (JSS), a Java interface to Network Security
Services (NSS).

################################################################################
%package -n %{product_id}
################################################################################

Summary:          JSS Connector for Apache Tomcat

# Java
Requires:         apache-commons-lang3
Requires:         %{java_headless}
Requires:         jpackage-utils >= 0:1.7.5-15

# SLF4J
Requires:         slf4j
Requires:         slf4j-jdk14

# JSS
Requires:         jss = 5.3

# Tomcat
%if 0%{?rhel} && ! 0%{?eln}
Requires:         pki-servlet-engine >= 1:9.0.7
%else
Requires:         tomcat >= 1:9.0.7
%endif

Obsoletes:        tomcatjss < %{version}-%{release}
Provides:         tomcatjss = %{version}-%{release}
Provides:         tomcatjss = %{major_version}.%{minor_version}
Provides:         %{product_id} = %{major_version}.%{minor_version}

# PKI
Conflicts:        pki-base < 10.10.0


%if 0%{?rhel}
# For EPEL, override the '_sharedstatedir' macro on RHEL
%define           _sharedstatedir    /var/lib
%endif

%description -n %{product_id}
JSS Connector for Apache Tomcat, installed via the tomcatjss package,
is a Java Secure Socket Extension (JSSE) module for Apache Tomcat that
uses Java Security Services (JSS), a Java interface to Network Security
Services (NSS).

################################################################################
%prep
################################################################################

%autosetup -n tomcatjss-%{version}%{?phase:-}%{?phase} -p 1

################################################################################
%build
################################################################################

export JAVA_HOME=%{java_home}

./build.sh \
    %{?_verbose:-v} \
    --name=%{product_id} \
    --work-dir=%{_vpath_builddir} \
    --version=%{version} \
    --jni-dir=%{_jnidir} \
    dist

################################################################################
%install
################################################################################

./build.sh \
    %{?_verbose:-v} \
    --name=%{product_id} \
    --work-dir=%{_vpath_builddir} \
    --version=%{version} \
    --java-dir=%{_javadir} \
    --doc-dir=%{_docdir} \
    --install-dir=%{buildroot} \
    install

################################################################################
%files -n %{product_id}
################################################################################

%license LICENSE

%defattr(-,root,root)
%doc README
%doc LICENSE
%{_javadir}/*

################################################################################
%changelog
* Fri Feb 10 2023 Red Hat PKI Team <rhcs-maint@redhat.com> - 8.3.0-1
- Rebase to Tomcat JSS 8.3.0

* Wed Nov 30 2022 Red Hat PKI Team <rhcs-maint@redhat.com> - 8.3.0-0.2.beta1
- Rebase to Tomcat JSS 8.3.0-beta1

* Thu Jun 30 2022 Red Hat PKI Team <rhcs-maint@redhat.com> - 8.2.0-1
- Rebase to Tomcat JSS 8.2.0

* Mon May 02 2022 Red Hat PKI Team <rhcs-maint@redhat.com> - 8.2.0-0.3.beta2
- Rebase to Tomcat JSS 8.2.0-beta2
- Rename packages to idm-tomcatjss

* Mon Apr 18 2022 Red Hat PKI Team <rhcs-maint@redhat.com> - 8.2.0-0.2.beta1
- Rebase to Tomcat JSS 8.2.0-beta1

* Tue Oct 05 2021 Red Hat PKI Team <rhcs-maint@redhat.com> - 8.0.0-1
- Rebase to Tomcat JSS 8.0.0

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 8.0.0-0.2.alpha1
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Jun 25 2021 Red Hat PKI Team <rhcs-maint@redhat.com> - 8.0.0-0.1
- Rebase to Tomcat JSS 8.0.0-alpha1
