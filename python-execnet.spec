#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# py.test based tests [use network]

%define 	module	execnet
Summary:	Rapid multi-Python deployment
Summary(pl.UTF-8):	Szybkie wdrożenia na wielu Pythonach
Name:		python-%{module}
Version:	1.5.0
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/execnet/
Source0:	https://files.pythonhosted.org/packages/source/e/execnet/%{module}-%{version}.tar.gz
# Source0-md5:	8df56985c656642cd26d233a1c74837c
URL:		http://codespeak.net/execnet/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools >= 7.0
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-apipkg >= 1.4
BuildRequires:	python-py
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools >= 7.0
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-apipkg >= 1.4
BuildRequires:	python3-py
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
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
Requires:	python3-modules >= 1:3.3

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

%package apidocs
Summary:	API documentation for Python execnet module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona execnet
Group:		Documentation

%description apidocs
API documentation for Python execnet module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona execnet.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python} -m pytest testing
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} -m pytest testing
%endif
%endif

%if %{with doc}
%{__make} -C doc html
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
%doc CHANGELOG.rst ISSUES.txt LICENSE README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG.rst ISSUES.txt LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,example,*.html,*.js}
%endif
