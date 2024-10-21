Name:           git-auto-commiter
Version:        1.0.1
Release:        1%{?dist}
Summary:        A simple auto-commiter for git as a cli tool

License:        MIT
URL:            https://github.com/MFactor1/git-auto-commiter
Packager:       Matthew Nesbitt
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       bash
Requires:       python3
Requires:       python3-gevent

%description
A simple cli tool for automating frequent git commits

%prep
%autosetup

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/gac
cp gaccli.pyc $RPM_BUILD_ROOT/%{_datadir}/gac
cp gacmain.pyc $RPM_BUILD_ROOT/%{_datadir}/gac
cp gaccmd.pyc $RPM_BUILD_ROOT/%{_datadir}/gac
cp gacworker.pyc $RPM_BUILD_ROOT/%{_datadir}/gac
cp LICENSE $RPM_BUILD_ROOT/%{_datadir}/gac
cp VERSION $RPM_BUILD_ROOT/%{_datadir}/gac
cat << EOF > $RPM_BUILD_ROOT/%{_datadir}/gac/gac
#!/bin/bash
/usr/bin/env python3 %{_datadir}/gac/gaccli.pyc "\$@"
EOF
cat << EOF > $RPM_BUILD_ROOT/%{_datadir}/gac/gac_daemon.service
[Unit]
Description=git-auto-commiter (GAC) daemon
After=network.target

[Service]
ExecStart=/usr/bin/env python3 %{_datadir}/gac/gacmain.pyc
Restart=always
User=$USER
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

%files
%license %{_datadir}/gac/LICENSE
%attr(0755, root, root) %{_datadir}/gac

%post
ln -s %{_datadir}/gac/gac %{_bindir}/gac
ln -s %{_datadir}/gac/gac_daemon.service %{_unitdir}/gac_daemon.service
sudo systemctl daemon-reload

%postun
rm %{_bindir}/gac
rm %{_unitdir}/gac_daemon.service
sudo systemctl daemon-reload

%changelog
* Sun Oct 20 2024 MFactor1 <mingsqu@gmail.com>
- 
