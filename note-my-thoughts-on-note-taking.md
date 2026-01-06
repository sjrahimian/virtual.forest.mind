# Virtual.Forest.Mind CLI Tool

## Summary

Learnings and thoughts on the matter of note-taking, and how "virtual.forest.mind" came to be.

## Introduction

After a few days of reading and researching on note-taking and *personal knowledge management* (PKM), as well as different applications, [Zettelkasten](https://sacredkarailee.medium.com/understanding-zettelkasten-notes-d7eb3fae0c45), and it's [fleeting/reference/permanent notes](https://writing.bobdoto.computer/zettelkasten/), [PARA/second brain](https://www.ssp.sh/brain/second-brain/), [digital gardens](), plaintext, wiki, etc. Learning all that was fascinating and after reflecting a bit, I realized that creating a note vault, second brain, digital garden — whichever method and whatever you want to call it — will be modelled to some extent on how an individual processes, organizes, and stores information; that is to say there are different methods and tools for different people (there is no "one size fits all"). Furthermore the virtual, physical, and mental models of how someone organizes information are all *reflections* of one another (and while an *a priori* hierarchy could be established, they will also simultaneously influence each other). This did not make it any less difficult for me to know where exactly to start my own PKM. I was still confused and doubtful about which PKM method and tools where right for me, and so I kept searching.

[*Is the concept of Personal Knowledge Management flawed?* by ElrioVanPutten](https://www.reddit.com/r/ObsidianMD/comments/zkefis/is_the_concept_of_personal_knowledge_management), [*Networked Thought* by jzhao.xyz](https://jzhao.xyz/posts/networked-thought), and [*Stop Procrastinating With Note-Taking Apps Like Obsidian, Roam, Logseq* by Sam Matla](https://www.youtube.com/watch?v=baKCC2uTbRc) were important material that provided well-thought opposing views to the note-taking rabbit hole. I had been drawn in by all the note-taking "glitter", and lost sight of __*means*__ and __*ends*__. It was still a worthwhile learning, but one can get caught up in the hype, and end up never writing. Ultimately I concluded that taking notes and concocting a structure is a personal endeavour, the initial step in building an organic environment that meets one's requirements, flow, use case, groove, feng shui, etc., i.e., **find what works for you and just start__.

## PKM: Journey & Goals

These are questions I asked of myself and my answers which helped me think about the tools and structure. Hopefully the questions will be of use to you too:

1. Do you currently use note-taking software, and why do you want to change?
   * Replace OneNote (and be free)
     * It is one well-rounded note-taking application and the primary reason I'm still on Windows, so my note-taking tools need to be OS independent.
     * Using OneNote allowed me to preserve that familiar "notebook" structure, which is great for lectures, with the added benefit of drawing, pictures & OCR, search, attaching files, and formatting all in the same application.
       * While it would hard to replicate many of the features, OneNote essentially is a wrapper that included everything in one neat application. I'll have to use multiple tools or custom scripts, but the end result should be the same.
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
     * Akin to an [infinite hammerspace](https://tvtropes.org/pmwiki/pmwiki.php/Main/Hammerspace) for notes; anything and everything placed in there can be retrieved later when needed, e.g., quotes from thinkers, books, etc., without having to give much thought to folder categories. Instead organization and identification would be captured via backlinks and tagging.
3. What is the end goal of note-taking?
   * Ease and simplicity to note-taking (*less is more* mentality)
   * Shareability - this allows every "page" to be uploaded independent of other "folders", or as a whole
   * Flexibility and scalability - combine notes, folders, or split them
   * Version control

### Final Decision

I settled on creating a plaintext/Markdown note-taking environment as the means of recording and tracking notes, because nothing in my search for a new note-taking app came close to OneNote (that Office-style ribbon is convenient) and the notebook style that I'm familiar with, but OneNote is limited to Windows and shackles the data in a proprietary format. I have been playing around with [*Foam*](https://foambubble.github.io/foam/) and [*Obsidian*](https://obsidian.md/), as well as my own custom Python script `vfm/vfm.py` in [virtual.forest.mind repository](https://github.com/sjrahimian/virtual.forest.mind).

This material was helpful in deciding to move away from any one particular application:

* [*How I'm able to take notes in mathematics lectures using LaTeX and Vim* by Gilles Castel](https://castel.dev/post/lecture-notes-1/)
* [*How to Build a Zettelkasten: The simple way* by gsilvapt](https://gsilvapt.me/posts/building-a-zettelkasten-the-simple-way/)
* [*Simple, Non-Commercial, Open Source Notes*](https://www.youtube.com/watch?v=XRpHIa-2XCE)

### Design

Instead of finding *one* application that will contain all notes, I've decided to take a lesson from the world of software development, where each project (or notebook in this case) is it's own directory, and treat each note-taking endeavor as a self-contained project.

This is the folder structure based on that idea:

#### Version 1.0

```text
mybooks.root/
├── book-1-name/
│   ├── .git/
│   ├── assets
│   │   ├── images/
│   │   └── files/
|   :
│   ├── sub-sections-and-pages...
|   :
│   ├── README.md
|   └── .gitignore
|
├── book-2-name/
│   ├── assets (if any)/
│   │   ├── images/
│   │   └── files/
|   :
│   ├── sub-sections-and-pages...
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
