# Faroese Gold Standard Corpus

This repo contains the ongoing project of creating a gold standard PoS tagged corpus for Faroese.

Faroese texts are tagged with the [Faroese implementation of ABLTagger](https://github.com/hinrikur/far-ABLTagger) and hand corrected, with a middle step of mapping back and forth between Icelandic and Faroese PoS tagging schemes.

## Source corpora

Currently the source corpora for the project are: 

- [Sosialurin Corpus](https://github.com/hinrikur/far-ABLTagger) (Hansen et al. 2004, Hafsteinsson 2020)
- [Faroese Parsed Historical Corpus (FarPaHC)](https://github.com/einarfs/farpahc) - Extracted from [UD release](https://github.com/UniversalDependencies/UD_Faroese-FarPaHC)
- [Faroese Text Corpus (FTS)](https://spraakbanken.gu.se/en/resources/fts)

**TBD:** Further corpora and scope of sampled text from each corpus.

## Directories:

### `correction` - Files undergoing manual correction. 

- `fo_tagged` contains files tagged using Faroese (Sosialurin) tagset.
- `to_correct` contains files ready for manual correction (converted to MIM-GOLD tagset).
- `finished` contains fully corrected files.

### `gold` - (WIP) Directory of "release" version of gold corpus

### `source_corpora`  - Unedited source corpora for the project

### `tagsets` - lists of various tagsets compiled for reference

### `scripts` - various scripts used for pre-processing the source corpora for correction