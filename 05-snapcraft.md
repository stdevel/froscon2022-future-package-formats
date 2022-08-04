class: center, middle
name: snapcraft

# Snapcraft

---

## Snapcraft

.left-column75[

- 2014 von Canonical vorgestellt
- Fokus auf Desktop-Anwendungen, Serverdienste und Drucker-Stack
  - ursprünglich für **IoT** entwickelt
  - nutzt systemd-Features wie **Socket Activation**
- **Runtime** benötigt, Installation notwendig
  - Hintergrunddienst `snapd` aktualisiert Snaps automatisch
  - lässt sich **nicht** deaktivieren, maximal um 60 Tage verzögern

]

.right-column25[

![:img Snap Logo, 100%](imgs/snap.png)

]

---

## Snapcraft

.left-column75[

- Apps werden in **Sandbox** ausgeführt
  - Rechte via **XDG Desktop Portals** und AppArmor
  - kein SELinux-Support bisher.red[*]
  - auch Themes müssen dediziert verteilt werden
- viele Anwendungen im **proprietären** [Snap Store](https://snapcraft.io/)
  - automatisches Testen der Apps auf Malware
  - trotzdem gab es 2018 Apps mit Cryptominer

.footnote[.red[*] EPEL bietet [`snapd-selinux`](https://centos.pkgs.org/8/epel-x86_64/snapd-selinux-2.56.2-1.el8.noarch.rpm.html)]

]

.right-column25[

![:img Snap Logo, 100%](imgs/snap.png)

]

---

## Snapcraft

.left-column75[

- SquashFS-Image mit `.snap`-Dateiendung
  - enthält Anwendung und benötigte Bibliotheken
  - Image wird eingehängt, Dateien on-demand entpackt
  - unterstützt **XZ** (Standard, geringere Größe) und **LZO** (größer aber schneller zu entpacken)
- nicht nur für Ubuntu, auch für RHEL- und Debian-artig, sowie Fedora, openSUSE, Solus und ArchLinux
- bietet **transaktionale Updates**

]

.right-column25[

![:img Snap Logo, 100%](imgs/snap.png)

]

---

## Snap! - Marketing is a dancer

- **Snap** - Anwendung + Abhängigkeiten, damit diese ohne Anpassungen auf verschiedenen Plattformen läuft
- **`snapd`** - Hintergrunddienst, verwaltet Snaps automatisch
- **Snap Store** - Online-Store, zentral, proprietär
- **Snapcraft** - Framework/Anwendung zum Bauen von Anwendungen
- **Channel** - Veröffentlichungskanal: `<track>/<risk>/<branch>`
  - `track`: ein unterstütztes Release, z.B. `latest`, `insider`
  - `risk`: Stabilität; `stable`, `candidate`, `beta` oder `edge`
  - `branch`: Entwicklungszweig; z.B. `fix-bug-1337`
  - Beispiele: `latest/stable`, `insider/edge`

---

## Neverending Story: Snap + Firefox

- Canonical entschied sich ab Ubuntu 21.10 Firefox primär als Snap anzubieten
  - seit Ubuntu 22.04 wird Firefox **ausschließlich** als Snap angeboten
- **Vorteil**: Mozilla paketiert Firefox, weniger Verantwortung für Canonical
--

- Nachteil: deutlich **langsamere** Firefox-Startzeiten
  - Kaltstart: 21s vs. 8s
  - Normaler Start: 2.9s vs 8.5s
  - Jetstream2-Benchmark: 64.804 vs 67.563

.footnote[.red[*] getestet auf i7-8850H @ 2 vCPUs, 2 GB RAM; siehe auch [Blogpost](https://cstan.io/?p=13062)]

???

- Tests auf potenter Hardware, ältere/schwächere Hardware deutlich langsamer (*~45 Sekunden auf i3-Geräten*)
- Feedback in Community eindeutig sehr negativ

---

## Neverending Story: Snap + Firefox

.left-column75[

- Canonical hat zunächst die [Entscheidung gerechtfertigt](https://ubuntu.com/blog/how-are-we-improving-firefox-snap-performance-part-1)
  - zusätzliche Sicherheit durch weitere Sandbox
- Paket entpackt beim ersten Start **alle 98** verfügbaren Sprachpakete
- Es wurde die **XZ**-Kompression verwendet
- Das Firefox 100.0-Snap aktivierte die Compilerflags **PGO** und **LTO** aktiviert
  - leicht schnellere Lauf-/Startzeiten
- Bei RPi/AMD wurden die falschen GPU-Treiber erkannt ==> ineffizientes **Software rendering**

]

.right-column25[

![:img Yo dawg, 100%](imgs/sandbox.jpg)

]

???

- **P**rofile-**G**uided **O**ptimization
- **L**ink **T**ime **Optimzation**

---

## Neverending Story: Snap + Firefox

- Canonical und Mozilla haben Snaps überarbeitet
  - Firefox lädt nur noch benötigte Übersetzungen herunter
  - GTK-Snaps nutzen nun LZO statt XZ.red[*]
--

- Weitere geplante Optimierungen:
  - SquashFS Dekomprimierung ist unter Ubuntu **single-threaded**
  - Anpassung der Kernelmodul-Konfiguration notwendig
  - **Pre-Caching** für GTK-Anwendungen geplant

.footnote[.red[*] auch andere Snaps sollten dadurch profitieren]

---

## Snap-Pakete erstellen

- Metadaten werden in **YAML**-Datei definiert
  - Name des Pakets
  - Version und Beschriebung
  - Berechtigungsmodell (`strict`, `devmode`, `classic`)
- Erfordert installiertes [Multipass](https://multipass.run/).red[*]
  - erstellt Ubuntu VMs unter Linux, macOS und Windows
- Erstellt eine `.snap`-Datei

.footnote[.red[*] Poor man's [Vagrant](https://vagrantup.com)]

---

class: small

### Beispiel

```yaml
name: test-offlineimap-dummy
version: '1.0'
summary: OfflineIMAP
description: |
  OfflineIMAP is software that downloads your email mailbox(es) as local
  Maildirs. OfflineIMAP will synchronize both sides via IMAP.
confinement: devmode
base: core18
parts:
  test-offlineimap-dummy:
    plugin: python
    python-version: python2
    source: https://github.com/snapcraft-docs/offlineimap.git
    stage-packages:
      - python-six
apps:
  test-offlineimap-dummy:
    command: bin/offlineimap
```

---

### Beispiel

Zur Erstellung muss die Datei `snapcraft.yaml` im einen sinnvoll benannten Unterordner liegen:

```shell
$ cd test-offlineimap-dummy
$ snapcraft
```

Hierbei wird eine Ubuntu-Instanz via **LXD** gestartet.

Die fertige Datei kann dann auf Systemen installiert werden:

```shell
# snap install --devmode --dangerous *.snap
```
