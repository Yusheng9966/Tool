#!/bin/sh
git config --global diff.external git-diff-wrapper.sh
git config --global diff.tool tortoise

git config --global difftool.tortoise.cmd 'tortoise.sh "$LOCAL" "$REMOTE"'
git config --global difftool.propmt fase
