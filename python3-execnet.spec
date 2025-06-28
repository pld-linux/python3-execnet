#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# pytest based tests [use network, need some environment]

%define 	module	execnet
Summary:	Rapid multi-Python deployment
Summary(pl.UTF-8):	Szybkie wdrożenia na wielu Pythonach
Name:		python3-%{module}
Version:	2.1.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/execnet/
Source0:	https://files.pythonhosted.org/packages/source/e/execnet/%{module}-%{version}.tar.gz
# Source0-md5:	f533366fb5b8fd802a9c4d15d6ca9796
URL:		https://codespeak.net/execnet/
BuildRequires:	python3-build
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
BuildRequires:	python3-py
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-timeout
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
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
%py3_build_pyproject

%if %{with tests}
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_timeout" \
%{__python3} -m pytest testing --timeout=20
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/execnet
%{py3_sitescriptdir}/execnet-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,example,*.html,*.js}
%endif
