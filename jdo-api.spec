%{?_javapackages_macros:%_javapackages_macros}
%global namedreltag -rc1
%global namedversion %{version}%{?namedreltag}
Name:          jdo-api
Version:       3.1
Release:       0.5.rc1.1
Summary:       JDO 3.1 API
Group:         Development/Java
License:       ASL 2.0
URL:           https://db.apache.org/jdo/
# svn export http://svn.apache.org/repos/asf/db/jdo/tags/3.1-rc1/ jdo-api-3.1-rc1
# find jdo-api-3.1-rc1/ -name "*.jar" -delete
# find jdo-api-3.1-rc1/ -name "*.class" -delete
# tar cJf jdo-api-3.1-rc1.tar.xz jdo-api-3.1-rc1
Source0:       %{name}-%{namedversion}.tar.xz

BuildRequires: java-devel
BuildRequires: mvn(javax.transaction:jta)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.maven.shared:maven-shared-components:pom:)

%if 0
# copy-jdori-jars module deps
BuildRequires: mvn(com.mchange:c3p0)
BuildRequires: mvn(log4j:log4j)
# Circular deps
BuildRequires: mvn(org.datanucleus:datanucleus-api-jdo)
BuildRequires: mvn(org.datanucleus:datanucleus-api-jpa)
BuildRequires: mvn(org.datanucleus:datanucleus-core)
BuildRequires: mvn(org.datanucleus:datanucleus-rdbms)
# jdo-exectck module deps
BuildRequires: mvn(commons-collections:commons-collections)
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.derby:derby)
BuildRequires: mvn(org.apache.derby:derbytools)
BuildRequires: mvn(org.apache.maven:maven-plugin-api)
BuildRequires: mvn(org.springframework:spring-core)
BuildRequires: mvn(org.springframework:spring-beans)
# jdo-tck module deps
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(org.hibernate.javax.persistence:hibernate-jpa-2.0-api)
%endif

# Test deps
BuildRequires: mvn(junit:junit)

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-site-plugin

BuildArch:     noarch

%description
The Java Data Objects (JDO) API is a standard interface
based Java model abstraction of persistence, developed as
Java Specification Requests (JSR 12 and 243) under the
auspices of the Java Community Process.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}

%pom_xpath_set "pom:project/pom:dependencyManagement/pom:dependencies/pom:dependency[pom:groupId = 'javax.transaction' ]/pom:artifactId" jta parent-pom
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'javax.transaction' ]/pom:artifactId" jta api

%if 0
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'javax.transaction' ]/pom:artifactId" jta tck
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:artifactId = 'c3p0' ]/pom:groupId" com.mchange copyjdorijars
%pom_remove_dep org.apache.geronimo.specs:geronimo-jpa_2.0_spec tck
%pom_add_dep org.hibernate.javax.persistence:hibernate-jpa-2.0-api tck
%pom_remove_dep org.apache.geronimo.specs:geronimo-jpa_2.0_spec exectck
%pom_add_dep org.hibernate.javax.persistence:hibernate-jpa-2.0-api exectck
%endif

%pom_disable_module copyjdorijars
%pom_disable_module exectck
%pom_disable_module tck

# unavailable test resources
rm -r api/test/java/javax/jdo/EnhancerTest.java \
 api/test/java/javax/jdo/PMFMapMapTest.java

%build

%mvn_file :%{name} %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt README.html

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-0.5.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 3.1-0.4.rc1
- Use Requires: java-headless rebuild (#1067528)

* Mon Dec 2 2013 Pete MacKinnon <pmackinn@redhat.com> 3.1-0.3.rc1
- dist bump for new build

* Thu Sep 26 2013 Pete MacKinnon <pmackinn@redhat.com> 3.1-0.2.rc1
- minor updates from review

* Fri Sep 20 2013 gil cattaneo <puntogil@libero.it> 3.1-0.1.rc1
- initial rpm
