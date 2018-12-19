# SangoKuro
Translation tools for Yo-kai Watch Sangokushi

Hello! This is kuronosuFear here and I hope you enjoy these translation tools that I made for Yo-kai Watch Sangokushi!

Usage:

Sangokushi-LinkDataXtractor
 - Searches for "LINKDATA_A.BIN" in the same directory
 - Places extracted files in the "<current directory>\Sangokushi-Xtracted" folder

Sangokushi-LinkDataRebuilder
 - Searches for "<current directory>\Sangokushi-Xtracted" folder
 - Rebuilds the contents of the directory as "LINKDATA_A.BIN-new" in the same directory

Sangokushi-GenerateTSVFiles
 - Searches for "<current directory>\Sangokushi-Xtracted" folder
 - Generates TSV (Tab-separated-values) for all scripts identified and groups them according to type
 - It saves the TSV files in the current directory

Sangokushi-GenerateTranslatedFiles
 - Exports the translated text from the TSV files to "<current directory>\Sangokushi-Translated" folder
