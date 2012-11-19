vimpyre list_installed
======================

* vim-scripts/ack.vim
* vim-scripts/bufexplorer.zip
* vim-scripts/DrawIt
* vim-scripts/fugitive.vim
* vim-scripts/The-NERD-tree
* vim-scripts/UltiSnips
* altercation/vim-colors-solarized
* nvie/vim-flake8
* jistr/vim-nerdtree-tabs

Perl command to install bundle list:
    cat README.md | perl -ne '/\* (.*)$/ && print qq{vimpyre install $1\n};'
