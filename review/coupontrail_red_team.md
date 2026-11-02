# CouponTrail: Red-Team Review

Date: 2026-11-02. Evidence labels used throughout:
- **[V] Verified:** a cited source states it.
- **[I] Inference:** reasoned from cited evidence.
- **[A] Assumption:** must be tested in interviews.

Following the rule I was given, a capability that simply isn't mentioned on a vendor's website is **not** treated as missing.

---

## Part 1: Challenging the central market claim

The claim under test: *"the workflow from raw machine export to a qualification-ready dataset is underserved."* The steps are numbered:

1. Raw export
2. Cleaning
3. ASTM/ISO data reduction
4. Specimen metadata
5. Validity checks
6. Failure-mode recording
7. Statistics
8. Report

| Product (company) | Target | Relevant capabilities | Steps covered | Outside the product | Evidence on limits | Price |
|---|---|---|---|---|---|---|
| **Bluehill Universal + Composites Application Module (Instron)** | Every lab with an Instron frame | Pre-configured ASTM D3039 method [V: Instron D3039 page]; chord modulus, transition strain and Poisson's ratio are standard D3039 outputs [V]; calculation suite regression-tested for every release [V: Bluehill SQA letter] | 1, 3, 4 (in-method), 5–6 (likely; field details not found), 7 (sample mean/SD/CV, likely), 8 | Cross-programme pooling and basis values [I]; non-Instron machines [V: runs Instron systems] | No source describes the failure-code UI or the exclusion workflow, so **unknown, not missing** | Quote only. Training costs $1,300/day [V] |
| **Bluehill Central (Instron)** | Multi-frame Instron labs | Central database of users, templates and data across systems [V: FAQ]; explicitly **not a LIMS** [V: Spanish FAQ]; API/export for LIMS/MES [V: custom-services PDF] | Data centralisation for 1–8 | Non-Instron frames; basis statistics [I] | Vendor states "not a LIMS" [V] | Quote only |
| **testXpert III (ZwickRoell)** | ZwickRoell labs | D3039 programs "pre-configured with all settings" [V]; standards mapped so "mainly selection parameters need to be entered" [V]; 21 CFR Part 11 option with tamper-proof audit trail [V]; Excel curve export [V]; DQ/IQ/OQ validation services [V] | 1, 3, 4, 8, audit trail; 5–7 likely | Cross-programme basis statistics [I]; other vendors' machines [I] | Series statistics and LIMS interface not documented, so **unknown** | Quote only; options sold separately [V] |
| **MTS TestSuite TW** | MTS labs | D3039 "Advanced" template with strain-gauge or extensometer support, modulus, strength, Poisson's ratio [V] | 1, 3, 4, 8 | Basis statistics [I] | D3039 is a paid add-on template, not in the base package [V] | Quote; templates sold separately [V] |
| **ADMET MTESTQuattro; Shimadzu Trapezium; Tinius Olsen Horizon** | Their own frames | ADMET documents a D3039 procedure [V]; software details not found | Probably 1, 3, 8 [I] | Unknown | Not researched in depth | Unknown |
| **QBench LIMS** | Configurable LIMS for testing labs | Specimen tracking, worksheets [V]; **ready-made Instron Bluehill integration** [V: qbench.net] | 2, 4, workflow and report | Composite-specific data reduction and statistics need configuration [I] | — | About $249–425 per user per month, 5-user minimum [V, from third-party listings] |
| **Wavefront LIMS** | Advanced-materials labs | Traceability from result to coupon, lot, instrument and calibration [V]; **Bluehill Universal integration** [V] | 2, 4, traceability, report | Composite statistics [I] | — | Quote only [V] |
| **LabWare, LabVantage, SampleManager** | Enterprise | General LIMS [V] | 2, 4, 8 | Composite content [I] | — | Enterprise |
| **Granta MI (Ansys)** | Primes and enterprise | Composite test data, qualification and equivalency, CMH-17/NCAMP/AGATE reference data [V] | 4, 7, 8 and more | Price and scale for small labs [V: "significant investment", third-party] | — | Quote only |
| **CMH17-STATS (CMH-17/NIAR)** | Qualification engineers | Approved Excel tool for A/B-basis values [V] | 7 | Data assembly from tests [I] | Single-user Excel licence [V] | Paid; price not found |
| **STAT-17 / ASAP** | Same | VBA macros named in the NCAMP SOP [V] | 7 | Password-protected code that users cannot audit [V]; 5 environments × 200 points limit [V] | [V] | Free/legacy |
| **cmstatr (open-source R)** | Engineers who use R | CMH-17-1G methods, validated against STAT-17 and ASAP [V] | 5 (outliers), 7 | Needs R; no data assembly [V/I] | — | Free (AGPL) |
| **CMTDS schema** | Data exchange | A composite test-data schema listed by CMH-17, **with no official recognition** [V] | 4 | Not a product | [V] | Free |
| **Excel / MATLAB / Python** | Everyone | Anything | All | No audit trail or version control [V: biased vendor source] | — | Free/already owned |

**Finding.** The claim **mostly fails**.
- For any lab that owns a current Instron, ZwickRoell or MTS frame, steps 1–8 *for a single test series* are covered by machine software that the vendors themselves present as standards-compliant, regression-tested, and (for ZwickRoell) Part 11 capable [V].
- Traceability and LIMS links are sold off the shelf, with ready-made Bluehill connectors in QBench and Wavefront [V].
- Basis statistics are covered by three tools, one of them free and validated [V].
- **What is left over is narrow:**
  - (a) assembling a pooled qualification dataset across many test series, batches and environments, then handing it to CMH17-STATS or cmstatr [I];
  - (b) labs whose frames come from several vendors [I];
  - (c) old frames or open-source DAQ setups, typical of universities [I].

## Part 2: One workflow in detail (small/independent lab, ASTM D3039)

| Step | Software | Manual work | Files | Error sources | Time | Evidence |
|---|---|---|---|---|---|---|
| 1. Register specimen | LIMS or Excel; the machine method's specimen fields | Enter IDs, panel/batch, and w/t (micrometer data can go directly into the software) | Test request, traveller | ID mix-ups, lost genealogy | Minutes per coupon [A] | Genealogy need [V: Lab Manager]; direct transfer of cross-section measurements [V: ZwickRoell, plastics page] |
| 2. Execute test | Bluehill / testXpert / TestSuite | Fit gauge, mount, run | — | Misalignment, grip failures | 5–15 min per coupon [A] | Pre-configured methods [V] |
| 3. Export | Machine software; raw curves to CSV/Excel | Choose the export | Raw CSV, binary result files | Wrong units, file naming | Low [A] | Excel export [V: ZwickRoell webinar] |
| 4. Data reduction | **Machine software** (chord modulus, strength) | Little | — | Wrong strain window or method setup | Low | [V: Instron, MTS, ZwickRoell] |
| 5. Validity | Operator judgement in the machine software or on paper | Inspect each break; flag breaks at the tab or near the grips as invalid | Photos | Inconsistent judgement | 1–3 min per coupon [A] | Invalid-break rules [V: ZwickRoell/standard] |
| 6. Failure documentation | Machine software notes, a photo, a 3-letter code | Visual coding | Photos | Code inconsistency between operators [A] | 1–3 min per coupon [A] | 3-letter code [V] |
| 7. Statistics | Machine report (mean/SD/CV) **for one series**; CMH17-STATS/cmstatr for basis values | **Copy results from many series and environments into the statistics tool, normalise, and set batch/environment grouping** | Exported results to Excel to STATS | **Transcription, mis-grouping, normalisation errors** [A, supported by I] | Hours to days per qualification [A] | Tools exist [V]; manual handling is not documented by users, so **inference** |
| 8. Report | Machine report template plus Word | Combine method, conditioning, results and failure photos | PDF/Word | Version drift | Hours per report [A] | Report content needs [V: D3039 guides] |

**The bottleneck.** If one exists, it sits at **step 7 across series**: moving many machine-generated result tables into a correctly grouped, normalised, pooled dataset for basis-value statistics. Steps 1–6 and 8 are largely served by machine software and LIMS [V]. The size of the step-7 burden is **unverified [A]**.

## Part 3: Three candidate wedges

| | **W1: Basis-statistics data assembler** | **W2: Multi-vendor result consolidator** | **W3: Academic data-reduction tool** |
|---|---|---|---|
| One sentence | "Turns many machine result exports into a correctly grouped, normalised, outlier-checked pooled dataset and B-basis report." | "Merges result exports from Instron, ZwickRoell and MTS frames into one consistent coupon database." | "Reduces raw load–strain CSVs from any frame to D3039 results for teaching or research labs." |
| User | Qualification or allowables engineer | Lab manager with a mixed-vendor fleet | University lab and students |
| Trigger | A qualification, equivalency or process-change programme | Data review across machines | Thesis or coursework testing |
| Input | Machine result exports plus a batch/environment map | Exports from several vendors | Raw CSV |
| Output | Pooled dataset, CMH-17 diagnostics, basis values, report | Unified table and traceability | Chord modulus, strength, report |
| Alternative | Excel copy-paste plus CMH17-STATS or cmstatr [V] | LIMS with connectors, e.g. QBench/Wavefront for Bluehill [V] | MATLAB/Python scripts, vendor software [I] |
| Reason to switch | Removes the assembly step and errors [A] | One view across vendors [A] | Free and easy [A] |
| Verdict | **Weakly viable.** Small user base and episodic need | **Reject.** LIMS connectors exist [V] and the problem is rare [A] | **Reject commercially.** Low willingness to pay and trivially scriptable [I] |

## Part 4: Willingness to pay

- **Who buys:** the lab manager or quality manager holds the budget, and IT/quality must validate the software for ISO 17025 [I]. For W1 the buyer is a materials/certification lead at an OEM or supplier [I].
- **Purchasing constraints:**
  - accredited labs must validate software, which is why vendors sell DQ/IQ/OQ services [V];
  - defence and ITAR work restricts cloud use [I];
  - procurement favours established vendors [A].
- **Do small labs buy specialist software?** Yes, from their machine vendor, as option bundles [V: options and templates are sold separately]. Buying from a third-party start-up is **unproven [A]**.
- **Price signals:**
  - QBench costs about $3–5k per user per year with a 5-user minimum [V, third party];
  - CMH17-STATS is a paid single-user licence, price not found [V];
  - cmstatr is free [V];
  - machine software is priced by quote [V].
  - W1 would compete against a **free validated tool plus Excel**, so its price ceiling is low [I].
- **Likely preference:**
  - Excel and the vendor software they already own [I];
  - engineers comfortable with code will use cmstatr [V exists; I preference];
  - LIMS for genealogy [V].
- **Missing evidence (must come from interviews):**
  1. hours spent per qualification on assembling statistics data;
  2. error incidents found in audits;
  3. whether in-house scripts already exist (a sign of real pain);
  4. budget owner and amount;
  5. how often programmes run each year;
  6. whether CMH17-STATS combined with an export template already makes this a non-problem.

## Part 5: Technical red team (if the software produces a wrong result)

- **Liability:** a wrong basis value flows into design allowables, so the safety consequence is real. Standard EULA disclaimers help, but reputational damage would be fatal for a small vendor [I].
- **Validation:**
  - every release must reproduce the CMH-17 handbook examples, as the established tools do [V: ASAP checked against handbook examples; cmstatr validated against STAT-17/ASAP];
  - Instron regression-tests its calculations on every release [V], which sets the bar a newcomer has to meet;
  - customers will also want IQ/OQ documentation [V].
- **Version control:** the method version, software version and parameters must be stamped on every result, and old results must be reproducible exactly [I].
- **Traceability:** an append-only audit trail; the standard for comparison is Part 11-grade tamper-proof records [V: ZwickRoell].
- **Calculation edge cases:**
  - choosing between pooling and single-point methods, with failed normality tests or Anderson–Darling k-sample tests;
  - fewer than 3 batches (ANOVA not recommended [V]);
  - an unusually low CV that inflates basis values [V];
  - the maximum normed residual outlier test applied within and across batches;
  - normalisation to cured ply thickness;
  - strain-window interpolation on sparse data.
- **Export-format risks:** formats are proprietary or binary [V: testXpert stores data in binary form]; units, column names and locale decimal separators vary; vendor updates silently change exports [I].
- **Implementation risk:** CMH-17 Rev H can change procedures, so the tool must track revisions [V: Rev H exists]. A divergence from CMH17-STATS output is an immediate credibility failure [I].
- **Can it be positioned as productivity, not certification, software?** Only partly. Basis values are used for certification by definition [V: NCAMP/FAA acceptance], so the tool sits next to certification whatever it calls itself. A "preparation only, verify with CMH17-STATS" positioning reduces liability, but it also limits the value: the user still runs the approved tool [I].

## Part 6: Decision

**KILL: CouponTrail as defined.**
- The central gap claim is largely refuted. Machine software covers single-series reduction, validity, reporting and audit trails; LIMS vendors sell ready-made connectors to that software; and statistics tools exist, including a free validated one [V].
- My earlier analysis underestimated the machine vendors. That was the error.

**The one remaining hypothesis is not a GO.** W1, the basis-statistics data assembler, survives only as an **unproven hypothesis**:
- its pain is inferred, not documented;
- it competes against Excel plus a free validated tool;
- its users are a small, episodic population;
- it carries certification-adjacent liability.

It does not meet a PIVOT bar on current evidence. Treat it as an interview question, not a product.

**What would re-open it.** At least 3 of 10 qualification engineers would need to independently report all of the following:
- more than 1 day of manual data assembly per programme;
- a real grouping or normalisation error they have experienced;
- willingness to pay at least €2k per year.

If those thresholds aren't met, W1 stays dead.

## Sources
Instron: https://www.instron.com/en/testing-solutions/astm-standards/astm-d3039/ · https://www.instron.com/wp-content/uploads/2024/06/Bluehill-SQA-Letter.pdf · https://www.instron.com/en/products/materials-testing-software/bluehill-central/faq/ · https://www.instron.com/es/products/materials-testing-software/bluehill-central/faq/ · https://instron.jp/ja-jp/-/media/literature-library/products/2024/11/bluehill-univeral-custom-services.pdf?sc_lang=en · https://www.instron.com/ko/일정/2026-08-28/
ZwickRoell: https://www.zwickroell.com/industries/composites/astm-d3039-tensile-test-on-composites/ · https://www.zwickroell.com:443/en/testing-software/testxpert-iii/traceability · https://www.zwickroell.com/fileadmin/content/Files/SharePoint/user_upload/PI_DE/05_584_Produktinformation_testXpert_III_Option_Nachvollziehbare_und_sichere_Pruefergebnisse_gemaess_FDA_21_CFR_Part_11_DE.pdf · https://www.zwickroell.com/en/news/en_us/testxpert-iii-export-editor-webinar · https://www.zwickroell.com/fileadmin/content/Files/SharePoint/user_upload/PI_EN/05_590_testXpert_III_PI_EN.pdf · https://www.zwickroell.com/industries/plastics/thermoplastics-and-thermosetting-molding-materials/tensile-properties-astm-d638/
MTS: https://www.mts.com/-/media/materials/pdfs/test-standards/100-342-854b_Composite_ASTMD3039.pdf?as=1 · https://www.mts.com/-/media/materials/pdfs/brochures/mts-testsuite-tw-brochure.pdf?as=1
ADMET: https://www.admet.com/?p=3959
LIMS: https://qbench.net/integration/instron-bluehill-univeral · https://www.wavefrontsoftware.com/integrate-instron-bluehill-universal-with-wavefront-lims/ · https://www.scispot.com/blog/qbench-pricing-explained-is-it-worth-it · https://www.capterra.com/p/188736/Wavefront-LIMS/ · https://www.labmanager.com/materials-testing-lims-structuring-multi-method-data-and-approval-workflows-35515
Statistics: https://cmh17.org/RESOURCES/Statistics-Software · https://www.cmh17.org/RESOURCES/Related-Documents · https://github.com/cmstatr/cmstatr · https://joss.theoj.org/papers/10.21105/joss.02265.pdf · https://www.amtas.washington.edu/wordpress/wp-content/uploads/2022/05/pap9-Raju_Statistics.pdf · https://www.wichita.edu/industry_and_defense/NIAR/Research/nsp100-sop.php
Granta: https://www.compositesworld.com/products/materials-data-management-software · https://us.fitgap.com/products/ansys-granta-mi-pro
