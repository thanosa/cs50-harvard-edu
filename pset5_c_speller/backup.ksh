#!/bin/sh

ts=$(date "+%Y%m%d_%H%M%S")

mkdir -p backups
cp dictionary.c backups/dictionary.c.${ts}_${1}
