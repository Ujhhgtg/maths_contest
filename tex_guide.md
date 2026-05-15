# Tex Compilation Guide

## Prepare

### Windows

1. Install [scoop](https://scoop.sh)
2. `scoop install miktex`

### Arch Linux

1. `yay -S texlive-meta texlive-langchinese perl-file-homedir`

## Compile

### Windows

1. `xelatex ./论文正文.tex` hit install for all package installation prompted

### Arch Linux

1. `xelatex ./论文正文.tex`

## Format

### Arch Linux

1. `latexindent ./论文正文.tex > ./论文正文.fmt.tex && mv ./论文正文.fmt.tex ./论文正文.tex`
