%global     commit f889fd09f2d8d55819dd53785e8bd895866e6628
%global     commit_short %(c=%{commit}; echo ${c:0:7})

Name:		fake-hwclock
Version:	0.11
Release:	1.%{commit_short}%{?dist}
Summary:	Save/restore system clock on machines without working RTC hardware
License:	GPLv2
URL:        https://git.einval.com/cgi-bin/gitweb.cgi?p=%{name}.git
Source0:	https://git.einval.com/cgi-bin/gitweb.cgi?p=%{name}.git;a=snapshot;h=%{commit};sf=tgz#/%{name}-%{version}-%{commit_short}.tar.gz
BuildArch:      noarch
BuildRequires:  systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd


%description
%{name} sets and queries a fake "hardware clock" which stores the
time in a file. This program may be run by the system administrator
directly but is typically run by systemd (to load the time on startup and
save it on shutdown) and cron (to save the time hourly).

If no command is given then %{name} acts as if the save command was used.


%prep
%autosetup -n %{name}-%{commit_short}


%build


%install
install -D -m 755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -m 644 %{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8
install -D -m 644 etc/default/%{name} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 debian/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
touch %{buildroot}%{_sysconfdir}/%{name}.data


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license COPYING
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}*
%config(noreplace) %{_sysconfdir}/default/%{name}
%ghost %{_sysconfdir}/%{name}.data
%{_unitdir}/%{name}.service


%changelog
* Sun Oct 16 2016 Vaughan <devel at agrez dot net> - 0.11-1.f889fd0
- Update to latest git commit: f889fd09f2d8d55819dd53785e8bd895866e6628

* Fri Jun 05 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 0.9-1
- Initial release.
