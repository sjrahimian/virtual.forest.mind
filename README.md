# Virtual.Forest.Mind CLI Tool

Provides commands to create, search, and open Markdown notes in user-defined spaces, using a configuration file for paths and editor settings.

```bash
python .\vfm.py --help
usage: vfm.py [-h] {init,new,stats,search} ...

Virtual Forest Mind CLI

positional arguments:
  {init,new,stats,search}
    init                Initialize directories and config
    new                 Create a new note
    stats               Output statistics: number of notes, most active space, total words.
    search              egrep-like search in a space/path. Usage: vfm.py search [target] pattern

options:
  -h, --help            show this help message and exit
```

## Personal Knowledge Management: Goals

What is the end goal of note-taking?

* Ease and simplicity to note-taking (*less is more* mentality)
* Shareability
* Flexibility and scalability
* Version control

### Why Another PKM Tool?

I have been playing around with [*Foam*](https://foambubble.github.io/foam/) and [*Obsidian*](https://obsidian.md/), but having my own custom Python script `vfm/vfm.py` gave some minor control over certain details of the PKM, as well as meeting the ease and simplicity goal. I'll likely use a combination of the my script and Foam or Obsidian.

If you're interested, see [*my thoughts on note-taking*](./note-my-thoughts-on-note-taking.md) for a more detailed review on note-taking.

Presenting a simple structure that can grow as needed:

```text
virtual.forest.mind/
├── vfm.private/
│   ├── subdir-1, ..., subdir-N
│   └── For private material that is not to be shared...
|
├── vfm.public/
│   ├── subdir-1, ..., subdir-N
│   └── For material that I would like to share or publish...
|   :
├── vfm.space/
│   ├── subdir-1, ..., subdir-N
│   └── Hammerspace space for Zettelkasten style notes that do not need any organization.
├── .git/
└── .gitignore 
```

## License

GNU GPLv3
