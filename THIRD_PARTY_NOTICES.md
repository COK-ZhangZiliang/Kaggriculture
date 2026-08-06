# Third-party notices

## Kaggriculture public economic route

`main.py` contains a compressed, re-serialized 719-action economic route
derived from Kaito Fukami's public Kaggle Notebook:

- [177/180 Fresh Top-30 | v21.1 Conditional Memory](https://www.kaggle.com/code/kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory)
- public artifact SHA-256:
  `d9dc24ce5429ec628ead0621a160bee90725350683d7dfcc4686fcaf511f3aab`
- accessed version last run: 2026-08-06

Kaggle describes the source of its public Notebook corpus as Apache 2.0
licensed. The applicable license text is included at
[`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt); see also Kaggle's
[Meta Kaggle Code data card](https://www.kaggle.com/datasets/kaggle/meta-kaggle-code).
The Kaggle submission archive carries this notice as
`THIRD_PARTY_NOTICES.txt` and the same full license text as
`LICENSE-APACHE-2.0.txt`, both at the root alongside `main.py`.

The route was changed by extracting only the public action sequence,
serializing it as compact JSON, and recompressing it. None of the source
Notebook's Top-30 prototype memory or controller code is included. The
surrounding validation, visible-weed recovery, opponent-exposure ordering,
clone-aware market timing, and terminal-liquidation controller were written
for this repository. The source Notebook documents further public replay and
research lineage; that provenance remains part of this attribution.

This notice covers the third-party portion only. It does not set a license for
the repository's independently written code.
