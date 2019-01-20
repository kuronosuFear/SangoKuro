# SangoKuro
Translation tools for Yo-kai Sangokushi

Hello! This is kuronosuFear here and I hope you enjoy these translation tools that I made for Yo-kai Sangokushi!

Download link (includes 64-bit Windows compiled executables): https://github.com/kuronosuFear/SangoKuro/releases/download/v1.1/SangoKuro.7z

Usage:

Sangokushi-LinkDataXtractor
 - Searches for "LINKDATA_A.BIN" in the current directory
 - Places extracted files in the "<current directory>\Sangokushi-Xtracted" folder

Sangokushi-LinkDataRebuilder
 - Searches for "<current directory>\Sangokushi-Xtracted" folder
 - Rebuilds the contents of the directory as "LINKDATA_A.BIN-new" in the current directory

Sangokushi-GenerateTSVFiles
 - Searches for "<current directory>\Sangokushi-Xtracted" folder
 - Generates TSV (Tab-separated-values) for all scripts identified and groups them according to type
 - It saves the TSV files in the current directory

Sangokushi-GenerateTranslatedFiles
 - Exports the translated text from the TSV files to "<current directory>\Sangokushi-Translated" folder
