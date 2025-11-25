# ngram_mester

En enkel kommandolinje-app for å generere n-gram-statistikk fra tekstfiler.

## Bruk

Installer avhengigheter (kun standardbibliotek i dag) og kjør:

```bash
python main.py --input path/til/tekstfil.txt --output analyser/utfil.tsv --n 3
```

Kommandoen over genererer tre filer i mappen `analyser/`:

- `utfil_n1.tsv`
- `utfil_n2.tsv`
- `utfil_n3.tsv`

Hver fil inneholder n-gram og forekomster for respektive n-verdi. Oppgi et nytt
basenavn via `--output` for å skrive til andre filstier; nødvendig mappestruktur
opprettes automatisk.
