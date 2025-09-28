# Building My Own Virtual.Forest.Mind

This is the story of how i ended up with "virtual.forest.mind", my personal alternative to OneNote.

```bash
 python .\vfm.py -help
usage: vfm.py [-h] {init,new,stats} ...

Virtual Forest Mind CLI

positional arguments:
  {init,new,stats}
    init            Initialize directories and config
    new             Create a new note
    stats           Output statistics: number of notes, most active space, total words.

options:
  -h, --help        show this help message and exit
```

## Personal Knowledge Management: Goals

What is the end goal of note-taking?
* Shareability - this allows every notebook to be uploaded independent of other notebooks, or as a whole
* Flexibility and scalability - combine notes, folders, or split them
* Version control

### Final Decision

I settled on creating a plaintext/Markdown note-taking environment as the means of recording and tracking notes, because nothing in my search for a new note-taking app came close to OneNote (that Office-style ribbon is convenient) and the notebook style that I'm familiar with. I have been playing around with [*Foam*](https://foambubble.github.io/foam/) and [*Obsidian*](https://obsidian.md/), as well as a custom Python script `vfm/vfm.py` in [virtual.forest.mind repository](https://github.com/sjrahimian/virtual.forest.mind).

(Read all about the journey.)[./note-my-journey-in-note-taking.md]

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
