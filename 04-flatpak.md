class: center, middle
name: flatpak

# Flatpak

---

## Flatpak

.left-column75[

- 2007 erstmalig als **Glick** vorgestellt.red[*]
- seit 2016 als Flatpak bekannt
- Fokus auf Desktop-Anwendungen
- benötigt Runtime
- Installation benötigt
- startet Anwendungen in **Sandbox**-Umgebung
  - Rechteverwaltung via **XDG-Portals**
  - Konfiguration über DE oder [Flatseal](https://github.com/tchx84/Flatseal)

.footnote[.red[*] spätere Iterationen hießen _Glick 2_, _bundler_ und _xdg-app_]

]

.right-column25[

![:img Flatpak-Logo, 90%](imgs/flatpak.png)

]

---

## Flatpak

.left-column75[

- verwendet **OSTree**- oder OCI-Images
- ca. 2.300 Anwendungen auf [Flathub](https://flathub.org/)
  - **dezentrale** Stores vorhanden (elementaryOS, Pop!_OS)
- Updates als neues Images
- derzeit auf [36 Distributionen](https://flatpak.org/setup/) unterstützt
  - auf einigen schon vorinstalliert

]

.right-column25[

![:img Flatpak-Logo, 90%](imgs/flatpak.png)

]

---

## Flatpak einrichten

Flatpak-Runtime installieren:

```shell
# yum install flatpak
# apt-get install flatpak
# zypper install flatpak
# pacman -S flatpak
```

Store hinzufügen:

```shell
$ flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

Anwendungen installieren:

```shell
$ flatpak install flathub com.github.tchx84.Flatseal
```

---

class: small, center, middle

### Flatseal

![:img Flatseal, 75%](imgs/flatseal.png)

---

class: small, center, middle

### Integration in Pop!_Shop

![:img Pop!_Shop-Integration, 75%](imgs/popshop.png)

---

## Flatpak erstellen

- SDK mit `flatpak-builder` benötigt
  - kann via Flatpak installiert werden
- **YAML**-Manifest definiert Quellen (u.a. `archive`, `git`, `file`, `patch`) und Build-Module
- u.a. [unterstützte Buildsysteme](https://docs.flatpak.org/en/latest/manifests.html?highlight=buildsystem#supported-build-systems):
  - `autotools`, `cmake`, `meson`, `qmake`,...
--

- Erstellen und **Testen** des Pakets
- Paket in **Repository** hinterlegen
- Repository zu lokalen Quellen hinzufügen und Paket **installieren**

---

### Beispiel

Installieren des SDK:

```shell
$ flatpak install org.freedesktop.Sdk
```

Erstellen der Anwendung und des Manifests:

`hello.sh`:

```shell
#!/bin/sh
echo "Ohai FrOSCon"
```

---

### Beispiel

`org.flatpak.Hello.yml`:

```yaml
app-id: org.flatpak.Hello
runtime: org.freedesktop.Platform
runtime-version: '21.08'
sdk: org.freedesktop.Sdk
command: hello.sh
modules:
  - name: hello
    buildsystem: simple
    build-commands:
      - install -D hello.sh /app/bin/hello.sh
    sources:
      - type: file
        path: hello.sh
```

---

class: small

### Beispiel

Erstellen des Pakets:

```shell
$ flatpak-builder build-dir org.flatpak.Hello.yml
Downloading sources
Initializing build dir
Committing stage init to cache
Starting build of org.flatpak.Hello
========================================================================
Building module hello in /home/cstankow/Dokumente/Lab/Flatpak/.flatpak-builder/build/hello-1
========================================================================
Running: install -D hello.sh /app/bin/hello.sh
Committing stage build-hello to cache
Cleaning up
Committing stage cleanup to cache
Finishing app
Please review the exported files and the metadata
Committing stage finish to cache
Pruning cache
```

---

### Beispiel

Anschließend existiert ein neuer Ordner `build-dir`:

```shell
$ tree build-dir/
build-dir/
├── export
├── files
│   ├── bin
│   │   └── hello.sh
│   └── manifest.json
├── metadata
└── var
    ├── lib
    ├── run -> /run
    └── tmp
```

---

### Beispiel

Testen der Anwendung:

```shell
$ flatpak-builder --user --install --force-clean build-dir org.flatpak.Hello.yml
Emptying app dir 'build-dir'
Downloading sources
Starting build of org.flatpak.Hello
...
Installing app/org.flatpak.Hello/x86_64/master
Pruning cache
```

```shell
$ flatpak run org.flatpak.Hello
Ohai FrOSCon
```

---

### Beispiel

Anwendung in Repository veröffentlichen:

```shell
$ flatpak-builder --repo=repo --force-clean build-dir org.flatpak.Hello.yml
...
Exporting org.flatpak.Hello to repo
Commit: 3217d6e09036fbd0165014daae6fc3c8ead90868294d2d56e57a633714829fe4
```

Repository einhängen und Anwendung installieren:

```shell
$ flatpak --user remote-add --no-gpg-verify tutorial-repo repo
$ flatpak --user install tutorial-repo org.flatpak.Hello
Installation complete.
$ flatpak run org.flatpak.Hello 
Ohai FrOSCon
```
