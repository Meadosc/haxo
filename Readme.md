## Haxo - what's inside my docker image?

<p align="center">
  <img src="icon.jpg"/>
  </p>

**List deb, rpm, pip and npm packages installed in a docker image.**

### Install

```bash
git clone <repo> && cd haxo && pip install .
```

### Usage

```
haxo <pkg_manager> <image:tag> --show
```

This will create a `data` directory and cache the info in the directory.

```
Usage: haxo [OPTIONS] COMMAND [ARGS]...

  Haxo - look inside a docker image.

  This tool can be used to get information on system packages installed in a
  container image using package managers such as apt, dnf, rpm, pip and npm.

Options:
  --help  Show this message and exit.

Commands:
  apt           apt package info.
  apt-licenses  apt packages and licenses info.
  pip           pip package info.
  rpm           rpm package info.
```

- apt packages with Licenses

```bash
haxo apt-licenses <image:tag> --show 
```

This will create a data directory, parse the image and list the licenses.


```bash
--  -------------------  ------------
 0  adduser              GPL-2
 1  apt                  GPL-2
 2  base-files           Artistic
 3  base-passwd          GPL-2
 4  bash                 GPL-3
 5  bsdutils             BSD
 6  bzip2                BSD
 7  coreutils            GPL-3
 8  dash                 BSD
--  -------------------  ------------
```
- apt packages with versions and source package information

```bash
-  -------------------   ------------- ------------------
53  libpam-modules       1.3.1-5ubuntu4           pam
54  libpam-modules-bin   1.3.1-5ubuntu4           pam
55  libpam-runtime       1.3.1-5ubuntu4           pam
56  libpam0g             1.3.1-5ubuntu4           pam
57  libpcre2-8-0         10.34-7                  pcre2
58  libpcre3             2:8.39-12build1          pcre3
59  libprocps8           2:3.3.16-1ubuntu2        procps
60  libseccomp2          2.4.3-1ubuntu1           libseccomp
61  libselinux1          3.0-1build2              libselinux
62  libsemanage-common   3.0-1build2              libsemanage
63  libsemanage1         3.0-1build2              libsemanage
-  -------------------   ------------- ------------------
```
- pip packages with versions and licenses

```bash
-  -------------  ------  --------------------------
0  appdirs        1.4.4   MIT License
1  astor          0.8.1   BSD License
2  colorama       0.4.3   BSD License
3  funcparserlib  0.3.6   MIT
4  hy             0.18.0  DFSG approved, MIT License
5  rply           0.7.7   BSD 3-Clause License
-  -------------  ------  --------------------------
```

- rpm packages with versions and licenses

```bash
-  -------------------------    ----------  ------------------
  0  tzdata                       2019c      Public Domain
  1  python-setuptools-wheel      41.6.0     MIT and (BSD or ASL 2.0)
  2  libssh-config                0.9.4      LGPLv2+
  3  dnf-data                     4.2.21     GPLv2+ and GPLv2 and GPL
  4  fedora-release-container     31         MIT
  5  fedora-release-common        31         MIT
  6  filesystem                   3.12       Public Domain
  7  coreutils-common             8.31       GPLv3+
  8  ncurses-base                 6.1        MIT
  9  libselinux                   2.9        Public Domain
-  -------------------------    ----------  ------------------
```
