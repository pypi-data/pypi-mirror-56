linky

# What

An databaseless file categorizer using symlinks.

This allows for a file to have multiple categories without agonizing too much about folder structure.

# Why

Programs often use databases to keep meta information about files. These databases:
 
 - are often stored in places one might not expect
 - have a custom schema  
 - are incompatibilities between databases  
   e.g postgres vs mariadb vs sqlite vs nosql vs etc.

All of which make migrations from program to program difficult. 
Now, of course this program will suffer from that particular problem too, however
 it will be possible to manually maintain the folder structure and links mentioned below. 

# How

Consider this existing directory

```
# The linked root
.
### Base folder that contains the data
├── .base
####### Configuration folder
│   ├── .linky
│   │   └── categories.yaml
│   ├── Last Christmas (2019)
│   │   ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv
│   │   └── subs
│   │       ├── cmn.srt
│   │       ├── de.srt
│   │       ├── eng.srt
│   │       └── nl.srt
│   └── The Hurt Locker (2008)
│       └── The.Hurt.Locker.2008.1080p.BRrip.mkv
### A category (or tag group) folder in the linked root
├── Actors
####### A tag folder
│   ├── Anthony Mackie
│   │   └── The Hurt Locker (2008)
│   │       └── The.Hurt.Locker.2008.1080p.BRrip.mkv -> ../../../.base/The Hurt Locker (2008)/The.Hurt.Locker.2008.1080p.BRrip.mkv
####### Another tag folder
│   ├── Emilia Clarke
│   │   └── Last Christmas (2019)
│   │       ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv -> ../../../.base/Last Christmas (2019)/Last.Christmas.2019.4k.HEVC.YIFY.mkv
│   │       └── subs
│   │           ├── cmn.srt -> ../../../../.base/Last Christmas (2019)/subs/cmn.srt
│   │           ├── de.srt -> ../../../../.base/Last Christmas (2019)/subs/de.srt
│   │           ├── eng.srt -> ../../../../.base/Last Christmas (2019)/subs/eng.srt
│   │           └── nl.srt -> ../../../../.base/Last Christmas (2019)/subs/nl.srt
│   ├── Emma Thompson
│   │   └── Last Christmas (2019)
│   │       ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv -> ../../../.base/Last Christmas (2019)/Last.Christmas.2019.4k.HEVC.YIFY.mkv
│   │       └── subs
│   │           ├── cmn.srt -> ../../../../.base/Last Christmas (2019)/subs/cmn.srt
│   │           ├── de.srt -> ../../../../.base/Last Christmas (2019)/subs/de.srt
│   │           ├── eng.srt -> ../../../../.base/Last Christmas (2019)/subs/eng.srt
│   │           └── nl.srt -> ../../../../.base/Last Christmas (2019)/subs/nl.srt
│   ├── Guy Pearce
│   │   └── The Hurt Locker (2008)
│   │       └── The.Hurt.Locker.2008.1080p.BRrip.mkv -> ../../../.base/The Hurt Locker (2008)/The.Hurt.Locker.2008.1080p.BRrip.mkv
│   ├── Jeremy Renner
│   │   └── The Hurt Locker (2008)
│   │       └── The.Hurt.Locker.2008.1080p.BRrip.mkv -> ../../../.base/The Hurt Locker (2008)/The.Hurt.Locker.2008.1080p.BRrip.mkv
│   └── Madison Ingoldsby
│       └── Last Christmas (2019)
│           ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv -> ../../../.base/Last Christmas (2019)/Last.Christmas.2019.4k.HEVC.YIFY.mkv
│           └── subs
│               ├── cmn.srt -> ../../../../.base/Last Christmas (2019)/subs/cmn.srt
│               ├── de.srt -> ../../../../.base/Last Christmas (2019)/subs/de.srt
│               ├── eng.srt -> ../../../../.base/Last Christmas (2019)/subs/eng.srt
│               └── nl.srt -> ../../../../.base/Last Christmas (2019)/subs/nl.srt
└── Watched
    ├── Unwatched
    │   └── Last Christmas (2019)
    │       ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv -> ../../../.base/Last Christmas (2019)/Last.Christmas.2019.4k.HEVC.YIFY.mkv
    │       └── subs
    │           ├── cmn.srt -> ../../../../.base/Last Christmas (2019)/subs/cmn.srt
    │           ├── de.srt -> ../../../../.base/Last Christmas (2019)/subs/de.srt
    │           ├── eng.srt -> ../../../../.base/Last Christmas (2019)/subs/eng.srt
    │           └── nl.srt -> ../../../../.base/Last Christmas (2019)/subs/nl.srt
    └── Watched
        └── The Hurt Locker (2008)
            └── The.Hurt.Locker.2008.1080p.BRrip.mkv -> ../../../.base/The Hurt Locker (2008)/The.Hurt.Locker.2008.1080p.BRrip.mkv
```

linky works by keeping all files in a common, hidden folder called `.base`.
All siblings of in the folder tree will link their files to the base folder.
It is thus possible to have a file in multiple categories like 
 Watched, Rating, Size, Actors etc.

# [Docs][]

For more information on the nomenclature and inner workings.

# Development

See [HACKING.md](./HACKING.md)

[Docs]: ./docs/index.md
