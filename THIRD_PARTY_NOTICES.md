# Third-party notices

## Public-behavior route reconstruction

`main.py` contains two compressed, re-serialized action routes reconstructed
from opponent actions visible in 111 public Kaggriculture episode replays:

- the low route is a component-wise majority over 61 episodes whose opponent
  ended with 10 cows and 4 sheep;
- the high route uses the low prefix through step 167 and a component-wise
  majority over nine episodes whose opponent ended with 6 cows and 8 sheep;
- farmer actions, each hand slot, and the complete market list were voted
  separately, normalized as JSON, and recompressed.

This is a majority reconstruction of observable behavior. It is not source-code
copying from every replay participant, does not establish that a participant
used a named public Notebook, and does not recover any participant's current
or private submission binary. Public replay identity and public Notebook
artifact identity are therefore kept as separate provenance claims.

## Apache-2.0 public Notebook references

The following Kaggle Notebook pages displayed an Apache 2.0 license when
accessed on 2026-08-17. Their downloaded artifacts were inspected as mechanism
references and used as hash-pinned local opponents:

### V17 10C/4S

- [V17-R1-RC2 High-Score 10C/4S Market Storage](https://www.kaggle.com/code/boatlee/v17-r1-rc2-high-score-10c-4s-market-storage)
- downloaded `main.py` SHA-256:
  `ccf2aefdadd600d3e6fcaad2879a310eb15bbd14183fc2deeff9bb2525697b9a`
- downloaded `submission.tar.gz` SHA-256:
  `d5e2ef7a24ecb279d2d0a16efae7f7de9bc23efdc71518d5800d51ec2abf43f7`

### Public shop-routed mixture of experts

- [Rank Top10: Read the Market, Choose the Farm](https://www.kaggle.com/code/indarkarhana/rank-top10-read-the-market-choose-the-farm)
- downloaded `main.py` SHA-256:
  `d39dba50793d9777c990347443bf0c481c78adaea86055f6f6b0600dcfcd9f2e`
- downloaded `submission.tar.gz` SHA-256:
  `a5f0e99ef483408fb524e7ae7c9c2df0c71fd849a30e4fcc54ef50fc166e3ee8`

These downloads support artifact-level inspection and local evaluation only.
Similar behavior in a public episode is not proof that the episode executed
the downloaded bytes.

## Retained controller lineage

V4 retains controller and market-schedule lineage previously attributed to:

- [V16-RC5-R5A High-Score 8C/4S Recovery](https://www.kaggle.com/code/boatlee/v16-rc5-r5a-high-score-8c-4s-recovery),
  reference `main.py` SHA-256
  `7f87c941af3050d0f21376f2843b324d7a06a1a8c050fa554cf07a769e5c937c`;
- [Kaggriculture: Breaking the Tie](https://www.kaggle.com/code/andrewsokolovsky/kaggriculture-breaking-the-tie),
  reference `main.py` SHA-256
  `df4e899ad535754cf2ddbd3c16e48085916b0cd2baa5182a1a2cfc6a856abae5`.

The earlier 8C/4S action tape is no longer the current V4 production route.
V4 retains bounded weed and cow-placement repair plus the reduced public
premium-sale schedule, then adds independent per-seat route selection,
route-aware purchase reconciliation, quantity-conserving repayment, malformed
observation protection, tests, packaging, and evidence controls.

## License copy and distribution

The applicable Apache 2.0 license text is included at
[`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt). The Kaggle submission
archive carries this notice as `THIRD_PARTY_NOTICES.txt` and the same full
license text as `LICENSE-APACHE-2.0.txt`, both at the archive root beside
`main.py`.

This notice covers the attributed third-party portions only. It does not set a
license for the repository's independently written code or imply that public
episode data itself is licensed under Apache 2.0.
