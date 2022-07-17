class: center, middle
name: motivation

# Motivation

---

## Motivation

- TODO
- TODO

---

## Klassische Paketverwaltung

- Die Auswahl an Linux-Paketmanagern ist groß:
  - RPM (*`yum`, `dnf`, `zypper`*)
  - DEB (*`apt`, `apt-get`*)
  - Arch (*`pacman`*)
--

- Neben vorkompilierten Paketen gibt es auch zusätzliche quellenbasierte.red[*] Paket-Manager:
  - **AUR** (*Arch User Repository*)
  - CRUX Ports
  - **Portage** (*Gentoo Linux*)

.footnote[.red[*] Paket wird vor Installation kompiliert]

---

class: small

## Überblick

| | AppImage | Flatpak | Snapcraft |
| - | -------- | ------- | --------- |
| Erschienen | 2004 | 2007 | 2014 |
| Autor:in | Simon Peter, Community | Flatpak-Team | Canonical |
| Fokus | Desktop | Desktop | Desktop, Dienste, Drucker-Stack |
| Runtime benötigt? | Nein | Ja | Ja |
| Installation notwendig? | Nein | Ja | Ja
| Sandbox | Nein | Ja | Ja |
| Format | SquashFS | OSTree/OCI | SquashFS |
| Rechteverwaltung | Nein | Ja (XDG) | Ja (XDG, AppArmor) |
| Store | [AppImageHub](https://appimage.github.io/apps/) | [Flathub](https://flathub.org/) | [Snapcraft](https://snapcraft.io/) |
| Angebot | ca. 1.300 Apps | ca. 1.300 Apps | ??? |
| Updates | Neues Image bzw. Delta | Neues Image | Transaktionelle Updates |
