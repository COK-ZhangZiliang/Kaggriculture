# Third-party notices

## Kaggriculture public 8C/4S route and market schedule

`main.py` contains a compressed, re-serialized economic route reconstructed
from public Kaggriculture replays of Nikita Lugovoy's submission `55440039`:

- episodes `92165990`, `92185587`, and `92223213`;
- majority-reconstruction reference:
  [V16-RC5-R5A High-Score 8C/4S Recovery](https://www.kaggle.com/code/boatlee/v16-rc5-r5a-high-score-8c-4s-recovery);
- reference artifact SHA-256:
  `7f87c941af3050d0f21376f2843b324d7a06a1a8c050fa554cf07a769e5c937c`;
- accessed 2026-08-13.

The evidence-gated premium counter retains only the public premium-sale
schedule from:

- [Kaggriculture: Breaking the Tie](https://www.kaggle.com/code/andrewsokolovsky/kaggriculture-breaking-the-tie);
- reference artifact SHA-256:
  `df4e899ad535754cf2ddbd3c16e48085916b0cd2baa5182a1a2cfc6a856abae5`;
- accessed 2026-08-13.

Kaggle describes the source of its public Notebook corpus as Apache 2.0
licensed. The applicable license text is included at
[`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt); see also Kaggle's
[Meta Kaggle Code data card](https://www.kaggle.com/datasets/kaggle/meta-kaggle-code).
The Kaggle submission archive carries this notice as
`THIRD_PARTY_NOTICES.txt` and the same full license text as
`LICENSE-APACHE-2.0.txt`, both at the root alongside `main.py`.

The route was changed by majority-selecting public replay actions, serializing
them as compact JSON, and recompressing them. The second source was reduced to
83 premium-sale schedule entries; its field and terminal tapes are not
included. This repository adds per-seat state, weed and partial-purchase
recovery, general-product H1 lead/repayment, evidence-gated H7
prepayment/repayment, malformed-observation protection, tests, and packaging.
The source Notebooks document further public replay and research lineage; that
provenance remains part of this attribution.

This notice covers the third-party portion only. It does not set a license for
the repository's independently written code.
