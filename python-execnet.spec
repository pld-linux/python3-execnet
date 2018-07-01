#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_with	tests	# py.test based tests [use network]

%define 	module	execnet
Summary:	Rapid multi-Python deployment
Summary(pl.UTF-8):	Szybkie wdrożenia na wielu Pythonach
Name:		python-%{module}
Version:	1.4.1
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/e/execnet/%{module}-%{version}.tar.gz
# Source0-md5:	0ff84b6c79d0dafb7e2971629c4d127a
URL:		http://codespeak.net/execnet
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools >= 7.0
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-apipkg
BuildRequires:	python-py
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 7.0
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-apipkg
BuildRequires:	python3-py
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
execnet provides carefully tested means to ad-hoc interact with Python
interpreters across version, platform and network barriers. It
provides a minimal and fast API targetting the following uses:
 - distribute tasks to local or remote processes
 - write and deploy hybrid multi-process applications
 - write scripts to administer multiple hosts

%description -l pl.UTF-8
execnet dostarcza uważnie przetestowane narzędzia do interakcji z
interpreterami Pythona zainstalowanych w różnych wersjach, na różnych
platformach i w różnych sieciach. Zapewnia minimalne i szybkie API
przeznaczone do następujących zastosowań:
 - rozpraszania zadań na lokalne lub zdalne procesy
 - pisania i wdrażania wieloprocesowych aplikacji hybrydowych
 - pisania skryptów do administrowania wieloma hostami

%package -n python3-%{module}
Summary:	Rapid multi-Python deployment
Summary(pl.UTF-8):	Szybkie wdrożenia na wielu Pythonach
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
execnet provides carefully tested means to ad-hoc interact with Python
interpreters across version, platform and network barriers. It
provides a minimal and fast API targetting the following uses:
 - distribute tasks to local or remote processes
 - write and deploy hybrid multi-process applications
 - write scripts to administer multiple hosts

%description -n python3-%{module} -l pl.UTF-8
execnet dostarcza uważnie przetestowane narzędzia do interakcji z
interpreterami Pythona zainstalowanych w różnych wersjach, na różnych
platformach i w różnych sieciach. Zapewnia minimalne i szybkie API
przeznaczone do następujących zastosowań:
 - rozpraszania zadań na lokalne lub zdalne procesy
 - pisania i wdrażania wieloprocesowych aplikacji hybrydowych
 - pisania skryptów do administrowania wieloma hostami

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -mpytest testing
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -mpytest testing
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# no %%py_postclean !
# the source code might be run on a remote machine
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG ISSUES.txt LICENSE README.txt
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG ISSUES.txt LICENSE README.txt
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
