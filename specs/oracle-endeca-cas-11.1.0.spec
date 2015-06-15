#-----------------------------------------------------------------------------
# author: Vina RAKOTONDRAINIBE (RE ENTER SAS)
# 
# Description:
# ---------------
# 
# Spec file to build an Endeca Content Acquisition Service for Oracle guided search 11.1.0.
#
# Pre-requisites:
# ---------------
#
# 1) To install CAS, you need to install Tools and Frameworrk first. So this package will contain
# both CAS and Tools and Framework. There is no workaround at this time as part of the Endeca installation
# process launches tomcat to configure some components.
#
# 2) Prior to installation, you need to create a file called /etc/oraInst.loc which points
# the Tools and Framework installer to a "fake" oracle inventory folder. The content of this file is:
#
# inventory_loc=/tmp/oraInventory
# inst_group=rpmbuild
#
#-----------------------------------------------------------------------------

%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global product    oracle-endeca-cas
%global productdir %{productprefix}/endeca

%global uid 245

#-----------------------------------------------------------------------------
# Main package
#-----------------------------------------------------------------------------
Name:           %{product}
Version:        11.1.0
Release:        0
Summary:        Oracle Guided Search CAS 11.1.0 

Group:          System Environment/Daemons
License:        Proprietary
URL:            http://www.oracle.com
Source0:        endeca-tools-%{version}-%{release}.zip
Source1:        tools_response_11.1.0.txt
Source2:        endeca-cas-%{version}-%{release}.zip
Source3:        cas_silent_11.1.0.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

AutoReqProv:    no

%description
Oracle Guided Search CAS 11.1.0


#-----------------------------------------------------------------------------
%prep


#-----------------------------------------------------------------------------
%build


#-----------------------------------------------------------------------------
%install
export DONT_STRIP=1
rm -rf %{buildroot}

mkdir -p %{buildroot}%{productprefix}

# clean existing oracle inventory folder
rm -rf /tmp/oraInventory \
  && mkdir /tmp/oraInventory \
  && chmod 777 /tmp/oraInventory

export ENDECA_TOOLS_ROOT=%{buildroot}%{productprefix}/endeca/ToolsAndFrameworks/11.1.0
export ENDECA_TOOLS_CONF=%{buildroot}%{productprefix}/endeca/ToolsAndFrameworks/11.1.0/server/workspace

pushd %{buildroot}%{productprefix}
  unzip %{SOURCE0} > /dev/null 2>&1
  cd cd/Disk1/install \
  && ./silent_install.sh %{SOURCE1} ToolsAndFrameworks %{buildroot}%{productprefix}/endeca/ToolsAndFrameworks admin
popd

pushd %{buildroot}%{productprefix}
  rm -rf cd
popd

pushd %{buildroot}%{productprefix}
  unzip %{SOURCE2}
  chmod +x OCcas11.1.0-Linux64.sh \
    && ./OCcas11.1.0-Linux64.sh --target %{buildroot}%{productprefix} < %{SOURCE3} \
    && rm OCcas11.1.0-Linux64.sh
  find $RPM_BUILD_ROOT -type f -exec sed -i "s|${RPM_BUILD_ROOT}||g" {} \;
popd


#-----------------------------------------------------------------------------
%clean
rm -rf %{buildroot}


#-------------------------------------------------------------------------------
%pre
getent passwd endeca > /dev/null || \
  /usr/sbin/useradd -c "Endeca" -s /bin/bash -r -m -u %{uid} \
    -d /opt/endeca endeca 2> /dev/null || :

#-------------------------------------------------------------------------------
%post
chown -R endeca:endeca %{productprefix}/endeca/*

%files
%defattr(-, root, root, -)
%{productdir}


#-----------------------------------------------------------------------------
%changelog
* Fri Jun 12 2015 Vina Rakotondrainibe <vrakoton@re-enter.fr> - 11.1.0
- Initial package creation
