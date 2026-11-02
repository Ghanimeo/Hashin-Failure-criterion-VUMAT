# Stage 1 — Research Brief

**Working title:** Damage initiation and progressive failure criteria for plant fibre composites: are carbon-derived models (Hashin, Puck, LaRC) fit for purpose?
**Target:** Composites Part B: Engineering (review article)
**Status:** Stage 1 (RESEARCH, full mode), pass 2 complete: 13 searches
**Verification level:** Sources below were located by web search, and their existence, venue and gist were confirmed from search metadata and abstracts. Full texts were NOT read. Every entry is tagged `[A]` (abstract or snippet only). Before drafting, each must be upgraded to `[F]` (full text checked).

---

## 1. Research questions

**Primary research question.** To what extent do failure criteria and progressive damage frameworks developed for carbon and glass composites (Hashin, Puck, LaRC, Tsai–Wu) remain physically and predictively valid for plant fibre composites, and what modifications does the evidence support?

**Sub-questions:**
- SQ1. Which assumptions in each criterion are violated by plant fibre composites? These include linear-elastic behaviour up to initiation, deterministic strength, mode separability, a dry and stable matrix, and a single fibre scale.
- SQ2. What is the experimental evidence that ranks the criteria for plant fibre composites, and how strong is it in terms of number of layups, load cases, and biaxial versus uniaxial testing?
- SQ3. How have damage evolution laws been adapted? The candidates are continuum damage mechanics, mesoscale damage theory and fibre-direction inelasticity.
- SQ4. How do strength variability and hygrothermal state propagate into failure prediction?
- SQ5. What would a validated, plant-fibre-specific failure framework need to contain?

## 2. Scope

- **In scope:** flax, hemp, jute and sisal. Unidirectional and woven fabrics, with 3D textiles as a frontier topic. Thermoset and thermoplastic matrices, including bio-based matrices. Quasi-static intralaminar failure, with notched and impact cases as validation examples.
- **Out of scope:** fatigue criteria (cited only as an outlook), short-fibre and injection-moulded composites, and wood.
- **Review type:** a critical narrative review with a structured search protocol (Scopus and Web of Science, 2000–2026, using the term sets in §5). This is not a full PRISMA systematic review, but the search will be reported transparently.

## 3. Preliminary evidence synthesis (by mechanism)

### 3.1 Comparative criterion performance
- The most direct evidence comes from Koh and Madsen [1]. They tested flax laminates in tension and compression across five layups and found that Hashin and Puck give the smallest error against experiment, and that Tsai–Wu and Tsai–Hill perform worse.
- **Limitation:** this is a single material system with uniaxial loading only. **No flax biaxial or cruciform failure envelope was found**, whereas glass/epoxy has such data [2]. The envelope shape in the τ₁₂–σ₂ plane is therefore unvalidated for plant fibre composites, and this is the central gap.

### 3.2 Nonlinearity before initiation (Assumption violation A1)
- Flax/epoxy shows a nonlinear fibre-direction response, which is attributed to progressive reorientation of cellulose microfibrils. Implementations combine Hashin initiation with a VUMAT in Abaqus/Explicit [3].
- Mesoscale damage theory has been modified so that damage and inelastic strain evolve in the fibre direction, in tension [4] and in compression [5]. These frameworks therefore add damage on the fibre side, which carbon-derived models do not need.
- Continuum damage models have reproduced unidirectional flax open-hole tension (reported accuracy for the force–displacement response is about 89–98%) [6]. Anisotropic continuum damage has been applied to flax/PP [7].
- **Implication:** Hashin's initiation surface is being placed onto a material that has already accumulated damage and inelastic strain before any criterion is triggered. As a result, the meaning of "initiation" is ambiguous for plant fibre composites.

### 3.3 Strength variability (Assumption violation A2)
- A pooled dataset of 590 tests reports a coefficient of variation of 2.4–18.8% across flax, jute and carbon laminates. Normal distributions often fit natural-fibre strength groups adequately, with Weibull fits preferred for some groups [8]. Basis values (A and B) have been derived from the same data [9].
- Progressive failure models with Weibull-distributed fibre strengths are highly sensitive to the Weibull parameters and to shear-lag assumptions [10]. A probabilistic strength model exists for flax fabric composites [11], and elementary-fibre individualisation affects unidirectional tensile failure [12].
- **Implication:** using deterministic strength allowables in Hashin or Puck hides the dominant source of prediction error.

### 3.4 Hygrothermal state (Assumption violation A3)
- Moisture causes fibre swelling, matrix plasticisation and interface debonding. Interlaminar shear strength falls faster than tensile strength [13]. Across natural fibre composite systems, tensile strength losses are reported from less than 10% to about 40% [13,14].
- In flax/bio-epoxy the failure mode changes to fibre slip and pull-out [14]. This is a change in mechanism, not just a scaling of strength, so criteria with fixed modes and moisture-scaled strengths may misidentify the active mode.
- Moisture-dependent Hashin models and Weibull strength-degradation models exist **only for carbon** [15,16]. **No moisture-coupled failure criterion has been validated for plant fibre composites.** This is a gap.

### 3.5 Existing reviews (novelty check)
- General reviews of failure criteria [17] and of plant fibre composite mechanical behaviour [18] exist. A 2025 review covers failure behaviour and modelling of natural fibre composites at a broad level [18].
- **No dedicated critical review was found that tests the assumptions of the carbon-derived criteria against plant fibre physics.** The proposed review should therefore be positioned as an assumption-by-assumption audit, not as another survey. *Novelty status: provisionally confirmed. A Scopus check is required.*

### 3.6 Pass 2: what the foundational criteria assume (assumption matrix seed)
- **Hashin [19]:** four separately modelled modes (fibre and matrix, each in tension and compression) built from quadratic stress polynomials, giving a piecewise-smooth failure surface. It implicitly assumes linear-elastic behaviour up to initiation and deterministic strengths.
- **Puck and Schürmann [20]:** Mohr–Coulomb action-plane inter-fibre fracture. Transverse and shear tractions on the fracture plane drive failure, while compression on that plane resists it. It has proven itself in the World-Wide Failure Exercise [23]. However, **its inclination parameters were recommended only for glass/epoxy and carbon/epoxy [24]**, so no calibration exists for plant fibre composites. This is the strongest single argument for the review's thesis.
- **LaRC03 (2D) and LaRC04 (3D) [21,22]:** physically based criteria with no curve-fitting parameters. LaRC03 was derived from Dvorak's fracture-mechanics analysis of cracked plies combined with Puck's action plane. The in-situ strength and kinking models it relies on assume carbon-like fibre misalignment and a matrix whose nonlinear shear behaviour is well characterised. These assumptions have not been examined for plant fibre composites (to verify in the full texts).
- **World-Wide Failure Exercise [23]:** the benchmark exercise for synthetic-fibre composites. **No equivalent exists for natural fibre composites** (gap G6 is now supported by targeted search, not only by not having found one).

### 3.7 Pass 2: contradiction over the origin of tensile nonlinearity (FLAG)
The sources give three competing mechanisms for the bilinear "knee" in flax composites:
- (a) reorientation of cellulose microfibrils plus viscoplasticity of the hemicellulose matrix, which is an intrinsic fibre property [3,25];
- (b) untwisting and stretching of the yarns, as proposed by Shah et al. However, nonlinearity is also seen in untwisted assemblies, which counts against this mechanism [25];
- (c) progressive micromechanical damage, rather than nonlinearity intrinsic to the constituents [26].

The mechanism matters for modelling. Under (a), the knee belongs in the elastic or viscoelastic constitutive law, before any damage. Under (c), it belongs in damage evolution. A Hashin-based VUMAT that lumps the two together will produce non-unique calibrations. **This is a central argument for the review, so it gets its own section.**

### 3.8 Pass 2: fracture energies for damage evolution
- Translaminar fracture toughness of unidirectional flax/epoxy was not reported before Saadati et al. (2020), who measured it in tension and compression with compact-tension tests and infrared thermography [27]. Fibre-direction damage evolution laws borrowed from carbon (G_fc and G_ft) therefore had no flax-specific input until recently.
- Interlaminar toughness: for unidirectional flax/epoxy in mode I, mode II and mixed mode, mode II and mixed mode had not been characterised before 2020 [28]. Plain-weave flax gives about 363, 962 and 649 N/m in mode I, mode II and mixed mode, with fibre/matrix debonding dominant [29]. Fibre bridging and crack branching raise toughness [30]. Cohesive-zone and VCCT models over-predict toughness when secondary delamination occurs [31].
- **Gap G7:** there is no fully calibrated set of cohesive laws and intralaminar fracture energies for any single flax system. As a result, published flax progressive-damage models mix sources.

### 3.9 Pass 2: hemp and jute
- No validated Hashin or Puck progressive-damage model was found for pure hemp or pure jute laminates. The closest is a jute/glass hybrid using Hashin initiation with fracture-energy evolution [32]. **The evidence base is effectively flax-only.** The review should either be scoped explicitly to flax, or present the absence of hemp and jute work as a gap (G8).

## 4. Gap map

| # | Gap | Evidence status |
|---|---|---|
| G1 | No biaxial or multiaxial failure envelopes for plant fibre composites | Not found |
| G2 | Initiation is ill-defined when damage and inelastic strain occur before the criterion is triggered | Implicit in [3–6] |
| G3 | Deterministic criteria applied despite a CV of up to about 19% | [8–11] |
| G4 | Moisture changes the failure mode, but criteria assume fixed modes | [13,14] vs [15,16] |
| G5 | Criteria are calibrated on one layup family and one load type | [1] |
| G6 | No benchmark comparable to the World-Wide Failure Exercise for natural fibre composites | Supported by targeted search [23] |
| G7 | No consistent, fully calibrated set of fracture energies and cohesive laws for any flax system | [27–31] |
| G8 | Hemp and jute: no validated failure-criterion studies on pure (non-hybrid) laminates | [32] |
| G9 | Puck inclination parameters are uncalibrated for plant fibre composites; Koh and Madsen assessed final failure only | [1,24] |

## 5. Search protocol for the next pass

- **Fibre terms:** (flax OR hemp OR jute OR sisal OR "natural fib*" OR "plant fib*")
- **Composite terms:** (composite* OR laminate*)
- **Failure-model terms:** ("failure criteri*" OR Hashin OR Puck OR LaRC OR "Tsai-Wu" OR "progressive damage" OR "continuum damage" OR VUMAT OR UMAT)
- **Filters:** 2000–2026, English, journal articles and reviews.
- **Snowballing:** forward and backward citation chasing from [1], [4] and [8].

## 6. Proposed review structure (for Stage 2)

1. Introduction: field, then gap, then objective
2. Plant fibre composite physics relevant to failure (hierarchy, nonlinearity, scatter, hygroscopy)
3. Failure criteria and their embedded assumptions (an assumption matrix)
4. Evidence audit: criterion performance for plant fibre composites (SQ2)
5. Damage evolution and inelasticity (SQ3)
6. Variability and environment (SQ4)
7. Towards a plant-fibre-specific framework (SQ5), with a VUMAT implementation outline
8. Conclusions and research agenda (G1–G6)

---

## Bibliography (numbered, Vancouver-style; all `[A]`, to be verified in full text)

1. Koh R, Madsen B. Strength failure criteria analysis for a flax fibre reinforced composite. Mech Mater. 2018. https://sites.lafayette.edu/kohr/files/2018/07/Koh-Madsen-2018.pdf `[A]`
2. Failure analysis of fiber-reinforced composite laminates subjected to biaxial loads. Compos Part B. https://www.sciencedirect.com/science/article/abs/pii/S1359836815004758 `[A]` (authors TBC)
3. Tensile and compressive damaged response in flax fibre reinforced epoxy composites. Compos Part A. https://www.sciencedirect.com/science/article/abs/pii/S1359835X16303785 `[A]` (authors TBC)
4. Mesoscale modelling of tensile response and damage evolution in natural fibre reinforced laminates. Compos Part B. 2017. https://www.sciencedirect.com/science/article/abs/pii/S1359836816327184 `[A]`
5. Prediction of the compressive damage response of flax-reinforced laminates using a mesoscale framework. Compos Part A. 2020. https://www.sciencedirect.com/science/article/abs/pii/S1359835X20303912 `[A]`
6. Towards sustainable composite structures: experimental characterisation and damage modelling of unidirectional flax fibre-reinforced polymers. 2025. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12656454/ `[A]`
7. Anisotropic continuum damage model for prediction of failure in flax/polypropylene fabric composites. https://www.researchgate.net/publication/275718350 `[A]`
8. Statistical variability and lower-tail performance assessment of tensile properties in flax, jute, and carbon fiber composite laminates. 2026. https://pmc.ncbi.nlm.nih.gov/articles/PMC13416983/ `[A]`
9. Distribution-aware estimation of A-/B-basis characteristic values for natural-fiber composite laminates from single-source tensile data. Polymers. 2026;18(21):2713. https://www.mdpi.com/2073-4360/18/21/2713 `[A]`
10. The influence of flax fiber size effect on progressive damage models. J Eng Appl Sci. 2025. https://link.springer.com/article/10.1186/s44147-025-00858-8 `[A]`
11. Probabilistic strength modeling of flax-fabric-reinforced polymer composites. https://www.researchgate.net/publication/305727460 `[A]`
12. Effect of flax fibres individualisation on tensile failure of flax/epoxy unidirectional composite. https://www.academia.edu/22323433 `[A]`
13. Hygrothermal ageing and mechanical degradation behaviour of alkali-treated sunn hemp fibre/bio-epoxy composites. Sci Rep. 2026. https://www.nature.com/articles/s41598-026-44819-4 `[A]`
14. Hygrothermal durability and damage evolution of bio-epoxy-based composites reinforced with different fibre types. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12787434/ `[A]`
15. Progressive damage model for composite laminates in hygrothermal environments. https://pmc.ncbi.nlm.nih.gov/articles/PMC12824737 `[A]`
16. An empirical model to predict the strength degradation of the hygrothermal aged CFRP material. Compos Struct. https://www.sciencedirect.com/science/article/abs/pii/S0263822319324298 `[A]`
17. Review of failure criteria of fibrous composite materials. https://www.researchgate.net/publication/229675109 `[A]`
18. Shelly D, et al. Mechanical performance of bio-based fiber reinforced polymer composites: a review. Polym Compos. 2025. https://doi.org/10.1002/pc.30000 `[A]`
19. Hashin Z. Failure criteria for unidirectional fiber composites. J Appl Mech. 1980;47:329–34. doi:10.1115/1.3153664 `[A]`
20. Puck A, Schürmann H. Failure analysis of FRP laminates by means of physically based phenomenological models. Compos Sci Technol. 1998;58:1045–67. `[UNVERIFIED: bibliographic details not confirmed by search; check before citing]`
21. Dávila CG, Camanho PP, Rose CA. Failure criteria for FRP laminates. J Compos Mater. 2005;39(4):323–45. doi:10.1177/0021998305046452 `[A]` (NASA report: NTRS 20040001363)
22. Pinho ST, et al. Failure models and criteria for FRP under in-plane or three-dimensional stress states including shear non-linearity. NASA/TM-2005-213530. 2005. `[A]` (authors and title to be confirmed on NTRS)
23. Hinton MJ, Soden PD. Predicting failure in composite laminates: the background to the exercise. Compos Sci Technol. 1998;58:1001–10. `[A]`
24. A transverse failure criterion for unidirectional composites based on the Puck failure surface theory. https://www.researchgate.net/publication/372757624 `[A]`
25. Thermo-mechanical behaviour of flax-fibre reinforced epoxy laminates for industrial applications. Materials. 2015;8:7524–. doi:10.3390/ma8115384 `[A]`
26. In situ characterization of the damage mechanisms during tensile deformation in sustainable flax-PP spread-tow woven composites. 2025. https://link.springer.com/article/10.1186/s40712-025-00319-3 `[A]` (the claim that damage is the origin of nonlinearity needs attributing in the full text)
27. Saadati Y, et al. Study of translaminar fracture toughness of unidirectional flax/epoxy composite. Compos Part C Open Access. 2020. https://depot-e.uqtr.ca/id/eprint/9989/ `[A]`
28. Saadati Y, et al. A study of the interlaminar fracture toughness of unidirectional flax/epoxy composites. J Compos Sci. 2020;4(2):66. `[A]`
29. Low KO, et al. Interlaminar fracture toughness of a plain weave flax/epoxy composite. https://shdl.mmu.edu.my/7685/ `[A]`
30. Bensadoun F, et al. (interlaminar toughness vs flax architecture), cited via https://hal.univ-reims.fr/hal-02497644v1/document `[secondary citation; locate original]`
31. Ekeoseye et al. Mode II interlaminar fracture of flax/glass hybrid laminates. J Nat Fibers. 2022. https://doaj.org/article/993078e31fac4229bf15aaed75a6d478 `[A]`
32. Jute–glass hybrid epoxy composites: experiments and Hashin-based progressive damage. https://repositorio.ufc.br/ri/handle/riufc/75870 `[A]`
33. New insights into the stiffness and strength of flax composites from Tsai's modulus and the area of the failure envelope. Fibers Polym. 2024. doi:10.1007/s12221-024-00779-y `[A]`
