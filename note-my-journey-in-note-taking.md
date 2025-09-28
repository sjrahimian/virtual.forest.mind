# Building My Own Virtual.Forest.Mind

This is the story of how i ended up with "virtual.forest.mind", my personal alternative to OneNote.

## Introduction

I came up with this template after a few days of reading and researching on note-taking and *personal knowledge management* (PKM), as well as different applications, PARA, [Zettelkasten](https://sacredkarailee.medium.com/understanding-zettelkasten-notes-d7eb3fae0c45), and it's [fleeting/reference/permanent notes](https://writing.bobdoto.computer/zettelkasten/), [second brain](https://www.ssp.sh/brain/second-brain/), [digital gardens](), plaintext, wiki, etc. Learning all that was fascinating and after reflecting a bit, I realized that creating a note vault, second brain, digital garden — whatever you want to call it — will be modelled to some extent on how that individual processes, organizes, and stores information; that is to say the virtual, physical, and mental environments are all *reflections* of one another (and while an apriori hierarchy could be established, they also simultaneously influence each other). This did not make it any less difficult for me to know where exactly to start, especially when learning about PKM. Needless to say, I was still confused and doubtful about what I need.

[*Is the concept of Personal Knowledge Management flawed?* by ElrioVanPutten](https://www.reddit.com/r/ObsidianMD/comments/zkefis/is_the_concept_of_personal_knowledge_management), [*Networked Thought* by jzhao.xyz](https://jzhao.xyz/posts/networked-thought), and [*Stop Procrastinating With Note-Taking Apps Like Obsidian, Roam, Logseq* by Sam Matla](https://www.youtube.com/watch?v=baKCC2uTbRc) were important material that provided well-thought opposing views to the note-taking rabbit hole. I had been drawn in by all the note-taking "glitter", and lost sight of __*means*__ and __*ends*__. It was still a worthwhile learning, but definitely can get caught up in the hype, and not end up writing. Ultimately I concluded that taking notes and concocting a structure is a personal endeavour, the initial step in building an organic environment that meets one's requirements, flow, use case, groove, feng shui, etc., i.e., find what works for you and start.

## PKM: Journey & Goals

These are questions I asked of myself and my answers which helped me think about the tools and structure. Hopefully the questions will be of use to you too:

1. Do you currently use note-taking software, and why do you want to change?
   * Replace OneNote (and be free)
     * It is one well-rounded note-taking application and the primary reason I'm still on Windows, while I'd prefer to switch Linux (needs to be platform independent).
     * Using OneNote allowed me to preserve that familiar "notebook" structure, which is great for lectures, with the added benefit of drawing, pictures & OCR, search, attaching files, and formatting all in the same application.
   * Proprietary format
     * What happens if the software is discontinued?
     * Hard to share outside raw files.
   * Telemetry
     * Most apps today, even big open-source ones, collect some form of telemetry; I'd like to control that as best I can.
2. How are notes taken currently? What is the structure?
   * 1st structure: traditional mode of note-taking
     * Similar with notebooks, followed by sections and pages.
     * I'd like to keep this structure for some material.
   * 2nd structure: write, collect, & retrieve.
     * Akin to an [infinite hammerspace](https://tvtropes.org/pmwiki/pmwiki.php/Main/Hammerspace) for notes; anything and everything placed in there can be retrieved later when needed, e.g., quotes from thinkers, books, etc., without having to give much thought to file categories (notes should still include backlinks).
3. What is the end goal of note-taking?
   * Shareability - this allows every notebook to be uploaded independent of other notebooks, or as a whole
   * Flexibility and scalability - combine notes, folders, or split them
   * Version control

### Final Decision

I settled on creating a plaintext/Markdown note-taking environment as the means of recording and tracking notes, because nothing in my search for a new note-taking app came close to OneNote (that Office-style ribbon is convenient) and the notebook style that I'm familiar with. I have been playing around with [*Foam*](https://foambubble.github.io/foam/) and [*Obsidian*](https://obsidian.md/), as well as a custom Python script `vfm/vfm.py` in [virtual.forest.mind repository](https://github.com/sjrahimian/virtual.forest.mind).

These two articles were helpful in deciding to move away from an particular application:

* [*How I'm able to take notes in mathematics lectures using LaTeX and Vim* by Gilles Castel](https://castel.dev/post/lecture-notes-1/)
* [*How to Build a Zettelkasten: The simple way* by gsilvapt](https://gsilvapt.me/posts/building-a-zettelkasten-the-simple-way/)

### Design

Instead of finding *one* application that will contain all notes, I've decided to take a lesson from the world of software development, where each project (or notebook in this case) is it's own directory, and treat each note-taking endeavor as a self-contained project.

This is how the folder structure looks like:

#### Version 1.0

```text
mybooks.root/
├── book-1-name/
│   ├── .git/
│   ├── assets
│   │   ├── images/
│   │   └── files/
|   :
│   ├── sections-and-pages...
|   :
│   ├── README.md
|   └── .gitignore
|
├── book-2-name/
│   ├── assets (if any)/
│   │   ├── images/
│   │   └── files/
|   :
│   ├── sections-and-pages...
|   :
│   └── README.md
|   :
├── book-N-name/
|   :
├── mybooks.help/
│   ├── scripts/
│   └── templates/
├── .git/
└── .gitignore
```

#### Version 2.0

That's way to complicated; let's make it simpler. Presenting version 2.0 that can grow as needed:

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
