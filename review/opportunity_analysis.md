# Composites Software Opportunity Analysis

Date: 2026-11-02. Method: about 20 web searches across the composites product lifecycle. Every claim is tagged as follows:
- **[V] Verified:** a cited source states it.
- **[I] Inference:** reasoned from the cited conditions.
- **[H] Hypothesis:** must be validated through customer interviews.

Most sources are vendor pages, standards bodies, job postings or papers. No user interviews have been run yet, which is the main limitation of this whole analysis.

---

## Phase 1–3: Problem landscape, evidence and existing solutions

| # | Problem area | Evidence | Existing solutions | Verdict |
|---|---|---|---|---|
| 1 | **Prepreg out-time and shelf-life tracking** | Out-time is cumulative, and ERP systems lack prepreg life-cycle tracking [V: JETCAM, Cratus] | Plataine TPO (Airbus JV and HITCO customers), JETCAM CrossTrack, DeltaTRAK wireless loggers, TotalControlPro, DynamxMFG [V] | **Reject.** The pain is real but the market is well served. |
| 2 | **Allowables and equivalency statistics (CMH-17)** | STAT-17 and ASAP are Excel/VBA macros with password-protected code that users cannot audit [V: cmstatr JOSS]. ASAP is limited to 5 environments and 200 data points per environment [V: AMTAS]. Job postings ask engineers to "calculate basis properties" [V: Joby] | CMH17-STATS (paid, single-user Excel) [V]; cmstatr (open-source R, validated against STAT-17 and ASAP) [V]; Granta MI equivalency module [V] | **Moderate.** The statistics are already solved; the workflow around them is not. |
| 3 | **Test data from coupon to qualified dataset (traceability and data reduction)** | Postings ask staff to "maintain a test database", produce test matrices, Excel and test reports [V: Vectorply, Rock West, Joby, CPI]. Type certification takes "thousands of inspections and tests" [V: Joby]. Coupons must stay linked to panel, batch and records [V: Lab Manager]. Broken specimen-to-batch traceability and transcription are named as the main causes of invalid data [V, but from a vendor blog, so biased] | Machine software (Instron, ZwickRoell) handles single-test calculations [I]; generic LIMS (QBench, LabWare, LabVantage) [V]; Granta MI composites at enterprise pricing, quote only [V]; Excel [V] | **Strong.** The gap is the composite-specific hierarchy combined with the qualification output. |
| 4 | **Cure record review (autoclave and oven thermocouples)** | Leading and lagging thermocouples can differ by 20–30 °C, so one may finish its dwell while the other is still heating [V: academia case study]. Thermocouple drift and wiring faults produce misleading data [V: TE Wire, PharmOut] | Autoclave controllers log and plot data and identify the leading and lagging thermocouples [V: CompositesWorld]; review against the cure specification is mostly done by eye [H] | **Moderate–strong.** Niche, but concrete. |
| 5 | **Wind blade inspection data** | Fleet-scale demand is real [V] | SkySpecs (Horizon), Aerones Visual Inspection Studio, and others [V] | **Reject.** Saturated and venture-funded. |
| 6 | **NDT C-scan indication disposition and MRB** | Dispositions must cite the SRM, ADL or an engineering disposition, and screening cannot support structural decisions [V: MoviTherm] | Inspection vendor software, in-house MRB systems [I] | **Reject.** Liability is high, the data formats are proprietary, and a qualified human decision is required. |
| 7 | **Scarf repair design for repair stations** | Methods are academic and need validation [V]; repairs must follow approved data [I] | CATIA, in-house tools, SRM [V] | **Reject.** The regulatory approval barrier is too high. |
| 8 | **Marine scantlings (ISO 12215-5)** | — | HullScant, CompoSIDE/YACHTScant, free ICOMIA tool [V] | **Reject.** Served and small. |
| 9 | **FRP strengthening of concrete (ACI 440.2R)** | — | Sika CarboDur (free), frppy (open source), academic tools [V] | **Reject.** Free tools from vendors with a strong interest in giving them away. |
| 10 | **Coordinating test programmes between OEMs and external labs** | NCAMP runs about 1,200 coupons a week, has to be selective, and uses outside labs [V, older article] | Email, spreadsheets, lab portals [H] | **Weak as a standalone product.** Demand is unproven and it is a two-sided network. Better as a later module of #3. |

## Phase 4: Scores (1–10; deliberately skeptical)

| # | Severity | Frequency | Willingness to pay | Gap | Feasibility | Data availability | Ease of entry | Academic value | **Sum /80** |
|---|---|---|---|---|---|---|---|---|---|
| 3 Test data to qualified dataset | 7 | 8 | 6 | 6 | 7 | 9 | 5 | 8 | **56** |
| 4 Cure record review | 6 | 8 | 5 | 6 | 8 | 8 | 6 | 4 | **51** |
| 2 Allowables/equivalency statistics | 6 | 4 | 5 | 5 | 8 | 8 | 5 | 6 | **47** |
| 10 Test programme coordination | 5 | 5 | 4 | 5 | 6 | 7 | 3 | 4 | 39 |
| 1 Out-time tracking | 6 | 9 | 6 | 2 | 8 | 9 | 2 | 2 | 44 (saturated) |
| 5 Blade inspection data | 7 | 7 | 7 | 2 | 4 | 4 | 1 | 2 | 34 |
| 6 NDT disposition | 8 | 7 | 6 | 4 | 3 | 3 | 2 | 3 | 36 |
| 7 Repair design | 7 | 5 | 4 | 5 | 4 | 4 | 1 | 6 | 36 |
| 8 Marine scantlings | 4 | 4 | 3 | 2 | 8 | 8 | 3 | 3 | 35 |
| 9 Concrete strengthening | 4 | 5 | 2 | 1 | 8 | 9 | 1 | 4 | 34 |

Ideas 1 and 5 are rejected even with good severity scores, because the gap is closed and established companies own the market.

## Phase 5: Top 3 briefs

### A. CouponTrail: from coupon to qualification-ready dataset (#3)

**Problem.** An in-house or independent composites test lab runs coupon programmes of hundreds to thousands of tests. The data has to roll up in a fixed hierarchy:

> material batch → panel (cure record, fibre volume fraction, voids) → coupon (dimensions, tabs, conditioning, environment) → test (standard, machine export) → validity (failure mode code, grip failure) → result → statistics by batch and environment → report

Each machine's software reduces one test at a time [I]. The hierarchy, the validity screening, the conditioning history and the pooling into statistics live in Excel that is maintained by hand [V for Excel and "test database" in postings; I for the details]. Errors come from transcription and lost genealogy [V, but a biased source].

- **Who has the problem:** test engineers and technicians at tier-2/3 suppliers, eVTOL and space start-ups, independent labs and university labs.
- **When:** every qualification, equivalency, process-change or batch-acceptance programme.
- **Cost:** hours of manual data handling per programme and audit risk [H, to be quantified in interviews].

**Why the alternatives fail.**
- Machine software stops at one test and does not know panel/batch genealogy, conditioning, or CMH-17 pooling structure [I].
- Generic LIMS track samples but provide no composite data reduction, ASTM failure-mode codes or statistics, so a lot of configuration is needed [V that QBench is "configurable"; I that composite content is missing].
- Granta MI does cover this, but it is an enterprise system priced by quote and sized for primes [V for the positioning; I for its fit to small labs].
- cmstatr and STAT-17 handle the statistics only, and expect clean, already-structured input [V].
- **The missing piece is the middle layer:** turning raw machine exports into a validated, traceable, analysis-ready dataset.

**Product.**
- **Inputs:** machine CSV exports (Instron, ZwickRoell, MTS, generic), panel and batch records, and the test plan.
- **Processing:**
  - recompute standard-specific results (D3039, D6641, D7264, D2344, D3518 and so on) from the raw curves;
  - check validity (strain window, failure-mode code, grip failure);
  - detect outliers with the CMH-17 maximum normed residual (MNR) test;
  - normalise to cured ply thickness;
  - calculate basis values using cmstatr-equivalent methods.
- **Outputs:** an audit-trailed dataset, a test report in NCAMP style, and exports to cmstatr, STAT-17 and Granta.

**MVP (8–10 weeks).**
- *Essential:* hierarchy data model; import of 2–3 machine export formats; D3039 and D2344 data reduction; failure-mode capture; normalisation; MNR outlier test; B-basis for a single batch and pooled environments; PDF/CSV report; audit log.
- *Later:* more standards, cure-record attachment, test request portal, Granta and ERP connectors, multi-lab collaboration.
- *Not in v1:* direct machine control, AI of any kind, FEA, A-basis certification claims, 21 CFR Part 11 or Nadcap certification of the software itself.

**Architecture.**
- **Backend:** Python with FastAPI; NumPy, SciPy and pandas for data reduction; statistics ported from cmstatr and validated against the CMH-17 handbook examples.
- **Database:** PostgreSQL with an append-only audit table.
- **Frontend:** React with AG Grid and Plotly.
- **Files:** S3-compatible object storage for raw files.
- **Deployment:** Docker, with an on-premise option because labs may refuse cloud for ITAR or proprietary data.
- **AI:** none in v1. At most later, for mapping unfamiliar machine export columns.

**Business model.**
- Per-lab subscription (indicative €3–12k a year, to be validated).
- Free academic tier, which brings in university labs and teaching use.
- Paid on-premise licence for defence work.

### B. CureCheck: automated cure record review (#4)

- **Problem:** after every autoclave or oven run, quality staff check the thermocouple and pressure logs against the cure specification (ramp rates, dwell windows, leading/lagging spread, vacuum) and sign it off, mostly by eye [H]. The gradient and drift problems are documented [V].
- **Product:**
  - upload the controller CSV;
  - encode the specification as rules: ramp limits, dwell start when the lagging thermocouple reaches temperature, maximum spread, pressure tolerance;
  - get pass/fail per clause, a flag for suspect thermocouples (flat-lining, readings inconsistent with the setpoint), and a signed PDF record.
- **MVP:** 4–6 weeks.
- **Risks:**
  - Controller vendors (e.g. ASC) may already offer this, which needs checking [unverified].
  - The market is small and is a single feature.
- **Best treated as a module of A.**

### C. Web-based, auditable allowables and equivalency tool (#2)

- **Problem:** the VBA tools cannot be audited and have hard limits [V]; R is a barrier for most engineers [I].
- **Product:** a web front end over cmstatr-equivalent methods, with traceable inputs and reports.
- **Risks:**
  - The statistics are free and validated, so differentiation is thin.
  - Regulators prefer the established tools [I].
- **Also best treated as a module of A.**

## Phase 6: Stress test of A, looking for reasons to kill it

| Attack | Assessment |
|---|---|
| "Is it painful enough?" | Partly unproven. The evidence for Excel and manual databases is real [V], but its cost has not been quantified. **This is a must-validate:** 10 interviews, and look for anyone who has built an in-house tool, which is the strongest sign of pain. |
| "Engineers will keep using Excel." | This is the main threat. Excel is free and flexible. CouponTrail only wins if it removes a whole step, such as producing the qualification report and basis values directly from raw exports. Data entry alone is not enough. |
| "Granta MI or a LIMS already does this." | Granta does for primes. The target is labs that cannot justify Granta. Generic LIMS need composite-specific build-out, which is our content. The risk is that a LIMS vendor ships a composites template. |
| "Customer acquisition." | It is hard: labs are conservative and sales cycles are slow. The free academic tier, plus NCAMP-format reports that small suppliers need, are the wedges. Expect 6–12-month industrial cycles. |
| "Needs proprietary data?" | No. Customers use their own data, which is a strength. |
| "Regulatory and liability." | Software used for certification data may need validation by the customer; ISO 17025 labs validate their software. **Mitigation:** publish a validation pack (handbook examples reproduced) and present the tool as data reduction, not approval. |
| "Harder than it looks?" | Yes, in parsing heterogeneous machine exports, and the pooling and outlier logic has edge cases. Start with 2 machine formats and 2 standards. |

**Verdict:** A survives, but narrowed. "Composite LIMS" is a bad framing because it collides with generic LIMS. The right framing is **raw machine exports in, qualification-ready dataset and report out**. B and C become modules, not separate products.

---

## Phase 7: Recommendation (pending your approval)

1. **One-sentence definition:** CouponTrail turns raw composite coupon-test exports into a traceable, validity-screened, statistically analysed dataset and test report, without spreadsheets.
2. **Customer and user:** the test lab manager or materials engineer (buyer) and the test technician (user), at composite tier-2/3 suppliers, eVTOL and space start-ups, and independent test labs. Secondary users are university composite labs.
3. **The problem:** coupon programmes generate large volumes of data whose genealogy, validity screening and statistics are managed by hand in Excel and test databases [V]. Error and labour costs are [H] until interviewed.
4. **Why alternatives fall short:**
   - machine software stops at one test;
   - LIMS are generic;
   - Granta MI is enterprise-scale;
   - statistics tools expect clean input.
   Nobody owns the middle layer from raw export to qualified dataset.
5. **MVP features:** listed in brief A above.
6. **Roadmap:**
   - **Weeks 0–3:** 10–15 interviews, plus collecting real anonymised machine exports. This is the go/no-go gate.
   - **Weeks 3–10:** MVP.
   - **Weeks 10–16:** pilot with 2 labs and 1 university.
   - **Months 4–9:** more standards, the cure-check module and the allowables module, plus a validation pack.
   - **Month 9 onward:** on-premise edition and connectors.
7. **Biggest technical risks:**
   - the variety of export formats;
   - correct implementation of CMH-17 pooling and outlier logic;
   - keeping the audit trail truly immutable.
8. **Biggest commercial risks:**
   - Excel inertia;
   - slow lab sales cycles;
   - a LIMS vendor or Ansys moving down-market;
   - certification users requiring software validation evidence.
9. **Why pursue it:** it's a narrow, recurring workflow that every qualification programme repeats. It needs no proprietary data or AI. Evidence of manual handling is documented. It sits in a gap between tools rather than competing with them. It also serves industry and universities with the same product.

**Next step:** interviews before any code. The pain is still partly hypothetical, and Excel inertia could kill the product.

## Key sources
Prepreg tracking: https://pages.jetcam.net/blog/problems-of-manufacturing-with-pre-preg-composite-materials · https://www.cratustech.com/prepreg-out-time-makes-or-breaks-a-composite-part/ · https://files.jetcam.net/ctmtl/ · https://www.compositesworld.com/products/automated-wireless-real-time-prepreg-out-time-monitor · https://www.plataine.com/press/harbin-hafei-airbus-partners-plataine-argosy-improved-traceability-efficiency-yield/ · https://www.compositesworld.com/news/hitco-selects-plataine-software
Allowables: https://www.theoj.org/joss-papers/joss.02265/10.21105.joss.02265.pdf · https://www.amtas.washington.edu/wordpress/wp-content/uploads/2022/05/pap9-Raju_Statistics.pdf · https://wichita.edu/industry_and_defense/NIAR/cmh-17/software.php · https://www.wichita.edu/industry_and_defense/NIAR/Research/nsp100-sop.php · https://www.eng-tips.com/threads/airbus-composite-design-allowables.68066/post-260622
Test data: https://jobs.8vc.com/companies/joby-aviation/jobs/65376540-senior-composites-engineer-methods-and-allowables · https://vectorply.com/composite-test-engineer-job-opening/ · https://www.tealhq.com/job/test-technician_7ea1a42f4f3c65eff2e8ba3122664033e7339 · https://careers.cpijobs.com/jb/Advanced-Materials-Process-Engineer-Jobs-in-Marion-Virginia/12934461 · https://www.jobyaviation.com/news/joby-begins-first-conformity-testing-enters-next-phase-of-certification-process · https://www.labmanager.com/materials-testing-lims-structuring-multi-method-data-and-approval-workflows-35515 · https://qbench.com/blog/the-best-lims-for-materials-testing-labs · https://www.bassetti-group.com/en/material-testing-lab-data-reliability/ · https://www.compositesworld.com/products/materials-data-management-software · https://us.fitgap.com/products/ansys-granta-mi-pro · https://www.compositesworld.com/articles/plant-tour-national-institute-for-aviation-research-wichita-kan-us
Cure: https://www.academia.edu/6825152/root_cause_analysis_of_autoclave_curing_deviations · https://www.compositesworld.com/articles/automating-and-optimizing-autoclave-cure · https://blog.tewire.com/blog/dr-thermocouples-cure-for-erratic-temperature-readings-in-autoclave-composites-manufacturing
Rejected sectors: https://skyspecs.com/wind/inspections/ · https://aerones.com/visual-inspection-studio-officially-launched/ · https://movitherm.com/feeds/blog/aerospace-composite-inspection · https://wolfsonunit.co.uk/softwares/hull-and-scantlings-design/ · https://compositesuk.co.uk/?p=6945 · https://mus.sika.com/en/documents-resources/sika-carbodur-frp-design-software.html · https://pypi.org/project/frppy/ · https://www.sciencedirect.com/science/article/abs/pii/S0263822322012697
