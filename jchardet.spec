%{?scl:%scl_package jchardet}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 3

Name:           %{?scl_prefix}jchardet
Version:        1.1
Release:        12.%{baserelease}%{?dist}
Summary:        Java port of Mozilla's automatic character set detection algorithm

Group:          Development/Libraries
License:        MPLv1.1
URL:            http://jchardet.sourceforge.net/
Source0:        http://download.sourceforge.net/jchardet/%{version}/jchardet-%{version}.zip
Source1:        http://repo1.maven.org/maven2/net/sourceforge/%{pkg_name}/%{pkg_name}/1.0/%{pkg_name}-1.0.pom
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}maven-local

%description
jchardet is a java port of the source from Mozilla's automatic charset
detection algorithm. The original author is Frank Tang. What is available
here is the java port of that code. The original source in C++ can be found
from http://lxr.mozilla.org/mozilla/source/intl/chardet/. More information can
be found at http://www.mozilla.org/projects/intl/chardet.html.

%package javadoc
Summary:    API documentation for %{pkg_name}
Group:      Documentation
Requires:   %{?scl_prefix_java_common}jpackage-utils

%description javadoc
%{summary}.

%prep
%{?scl:scl enable %{scl} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

cp %{SOURCE1} pom.xml
# fix up the provided version
sed -i 's:<version>1.0</version>:<version>1.1</version>:' pom.xml

# remove distributionManagement.status from pom (maven stops build
# when it's there)
sed -i '/<distributionManagement>/,/<\/distributionManagement>/ d' pom.xml

# create proper dir structure
mkdir -p src/main/java/org/mozilla/intl/chardet
mv src/*java src/main/java/org/mozilla/intl/chardet
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} %{scl} - << "EOF"}
set -e -x
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 1.1-12.3
- Fix directory ownership
- Resolves rhbz#1418384

* Fri Jan 20 2017 Michael Simacek <msimacek@redhat.com> - 1.1-12.2
- Build for rh-maven33
- Related: rhbz#1414193

* Fri Jan 20 2017 Mat Booth <mat.booth@redhat.com> - 1.1-12.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Orion Poplawski <orion@cora.nwra.com> - 1.1-9
- Require java-headless (bug #1068252)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Orion Poplawski <orion@cora.nwra.com> - 1.1-7
- Update to current Java guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Apr 29 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-2
- Build with maven and provide maven metadata
- Add javadoc subpackage

* Fri Apr 22 2011 Orion Poplawski <orion@cora.nwra.com> - 1.1-1
- Initial package
