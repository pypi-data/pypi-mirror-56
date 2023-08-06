PoProofRead is a simple application for fast and easy proofreading and
commenting of po and podiff files.

# Introduction

PoProofRead is made for the task of reviewing and commenting on the contents
of po or podiff files. It does this by allowing the user to easily:

 * Move through the parts of the file with a single keypress
 * Start writing a comment without any activation of editing
 * Save the current state of the proofreading work
 * Output only the parts of the file that there are comments to
 * Switch below of inline commenting for each individual part

# Installation

PoProofRead can be installed with pip from from PyPI with the command:

```shell
pip install poproofread
```

## System requirements

### Ubuntu

In order to install poproofread with pip on an ubuntu system, a set of system
packaged will need to be installed. This can be achieved with the command:

```shell
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
```

# License information

PoProofRead is released under the GNU GPL version 3 license.