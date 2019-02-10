H's Dotfile Manager
===================

HDM is a tiny dotfile manager that lets you:
- Organize your dotfiles into *modules*
- Use a different set of modules on different machines (based on the hostname)
- Optionally configure your dotfiles using JSON

HDM makes use of GNU Stow and requires it to be installed.

## Dependencies

- GNU Stow
- Python (>3.4)

## Installation

Copy `hdm.py` to a directory in your `PATH`

## Usage

    Usage: hdm [options] DIRECTORY

    Options:
      -h, --help    show this help message and exit
      -d, --delete  Remove configurations
      -r, --reload  Reload configurations


The dotfiles in your `$HOME` are likely organized like this:

    /home/user
    ├── .config
    │   ├── alacritty
    │   │   └── alacritty.yml
    │   └── i3
    │       └── config
    ├── .vimrc
    └── .zshrc

Create a new directory inside your `$HOME`, name it anything you like, and create a subdirectory inside it, name it
`default` or `raw`, and move your dotfiles inside it. Subdirectories inside your *dotfiles* directory are called 
*modules*. 

Your *dotfiles* folder should now look like this:

    ~/dotfiles
    └── default
        ├── .config
        │   ├── alacritty
        │   │   └── alacritty.yml
        │   └── i3
        │       └── config
        ├── .vimrc
        └── .zshrc

Now, run:

    hdm ~/dotfiles

You can organize the dotfiles into *modules* instead.

    ~/dotfiles
    ├── alacritty
    │   └── .config
    │       └── alacritty
    │           └── alacritty.yml
    ├── i3
    │   └── .config
    │       └── i3
    │           └── config
    ├── vim
    │   └── .vimrc
    └── zsh
        └── .zshrc

And run the command again. Before you make changes to the directory structure, however, make sure to run:

    hdm ~/dotfiles --delete

HDM lets you choose the modules that you want to link. To do that, create a *hdmrc.json* file in your dotfiles directory
with the following contents:

    {
        "*": [
            "alacritty",
            "i3",
            "vim"
        ]
    }

HDM will link `alacritty`, `i3`, `vim` and ignore `zsh`. The `*` is a wildcard and matches every machine.
If you want to include modules based on the hostname of the machine, you can do this:

    {
        "*": [
            "alacritty",
            "i3",
            "vim"
        ],
        "user-pc": [
            "polybar/pc"
            "zsh"
        ],
        "user-latpop": [
            "polybar/laptop"
        ]
    } 

And arrange your `dotfiles` directory like so:

    ~/dotfiles
    ├── alacritty
    │   └── .config
    │       └── alacritty
    │           └── alacritty.yml
    ├── hdmrc.json
    ├── i3
    │   └── .config
    │       └── i3
    │           └── config
    ├── polybar
    │   ├── laptop
    │   │   └── .config
    │   │       └── polybar
    │   │           └── config
    │   └── pc
    │       └── .config
    │           └── polybar
    │               └── config
    ├── vim
    │   └── .vimrc
    └── zsh
        └── .zshrc

Included in the repo is a template you can use.

*Made with tears in Asgard*

