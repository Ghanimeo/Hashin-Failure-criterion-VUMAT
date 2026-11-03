# AcademicWrite — Technical Specification v0.3

Status: pre-implementation specification. Supersedes v0.2 (`AcademicWrite_Spec_v0.2.md`, preserved unchanged, SHA-256 `8f0ef0629c1317874d9a0a7f067aeadbcea8143078b229fe32cecfa0ae411315`).
No application code exists. Nothing in this document is a performance result.

---

## 0. Provenance, conventions, evidence levels

### 0.1 Source of v0.2
v0.2 was not present in this repository (`ghanimeo/hashin-failure-criterion-vumat`, which otherwise contains only an Abaqus VUMAT and README). The audited text is the v0.2 file produced in the originating session (604 lines, hash above), now committed alongside this document. No other AcademicWrite documents, test plans or code exist in the repository or its branches. **Recommendation:** move both specifications into a dedicated `academicwrite` repository before implementation; this repository is unrelated to the project.

### 0.2 Normative language
**MUST / MUST NOT** = mandatory for v1. **SHOULD** = mandatory unless a documented reason is recorded in `docs/decisions/`. **MAY / OPTIONAL (future)** = not in v1 scope.

### 0.3 Evidence levels (applied to every important feature)

| Level | Meaning | What counts as evidence |
|---|---|---|
| **0 — Guaranteed by design** | The code path cannot behave otherwise *under the stated assumptions*, and a test exists that fails the build if the property is violated. | Design + named automated test + passing CI run. Until the test passes, the feature is at **target level 0, current level 2**. |
| **1 — Tested and demonstrated** | Measured on a named, versioned corpus or fixture set with recorded results. Valid only for that corpus/fixture/model digest/hardware. | Stored result file under `bench/results/` or `tests/reports/`. |
| **2 — Expected, not demonstrated** | Design intent with rationale; no measurement yet. | Prose only. |
| **3 — Experimental / unresolved** | Behind a feature flag or advisory; no correctness claim. | — |

**v0.2 defect corrected here:** v0.2 labelled designed-but-unbuilt items "[T] Tested". No AcademicWrite feature is currently above level 2. Every feature in this document is listed as *target level → current level*. Current level is 2 or 3 for all items.

---

## 1. Hostile audit of v0.2

Severity: **C** Critical, **Mj** Major, **Mo** Moderate, **Mi** Minor. "Pre-code" = must be resolved in this specification before any implementation.

### 1.1 Critical findings

| ID | v0.2 section | Problem | Why it matters | Correction (v0.3 section) | Pre-code |
|---|---|---|---|---|---|
| C-01 | §K, §E.3, §F.5, §G | Features labelled "[T] Tested" with no implementation or measurement. | Misrepresents evidence; a reviewer or the author could treat unbuilt checks as validated. | Evidence levels redefined (§0.3); all features "target → current" (§K of v0.3). | Yes |
| C-02 | §E.3 worked example vs. §E.3 extraction rule 5 | Example rewrite has property `?` (unbound), yet R1 fires. Rule 5 says unbound slots → `partial` → R8 WARN only. The two statements contradict: as specified, the canonical swap would yield WARN, not BLOCK. | The flagship integrity test would fail or be "fixed" by ad-hoc code. | Binding model with explicit inheritance and a value-anchored comparison that does not require every slot (§E.4, rule R1). | Yes |
| C-03 | §E.1, §E.3 R9 | Comparison is per aligned sentence; cross-sentence value moves only WARN unless R1 also fires within a sentence. Failure cases J and M are not covered. | Misattribution via neighbouring sentence is a realistic small-model error. | Paragraph-level claim graph; comparison over the paragraph plus frozen context window (§E.3–E.5). | Yes |
| C-04 | §E.3 | Schema lacks: uncertainty (±, SD, CI, n), baseline semantics of percentages, limitation/qualification clauses, property-identity checks, conditional/scope qualifiers ("at RH > 85 %"). Failure cases F, H, K are not detectable. | These are exactly the meaning changes that survive token checks. | Extended schema (`Claim`, `Qualifier`, `Limitation`, `Uncertainty`, `Baseline`) and rules R10–R18 (§E.4). | Yes |
| C-05 | §I.3 | "Numerical preservation 100 % [G] after gating". Only holds for numbers the detector found; detector false negatives pass silently. | Overclaim on the core guarantee. | Restated: guarantee covers *detected* quantities only; an independent "digit-run" catch-all check is added so any changed digit sequence is BLOCK regardless of detector (§E.2 L1-Q0). | Yes |
| C-06 | §F.3 class E | "OPAQUE atoms re-emitted unchanged in new order". Re-ordering complex-field begin/separate/end, bookmarks or comment ranges can produce invalid or semantically broken XML; v0.2 also allowed citations to move within a clause. | DOCX corruption; Zotero/EndNote field breakage. | v1: OPAQUE atom **order is invariant** within a paragraph; any reorder → BLOCK. Text may change only between consecutive atoms (§G.4). | Yes |
| C-07 | §F.2 | Complex fields can span paragraphs (`fldChar begin` in one `w:p`, `end` in a later one: TOC, Zotero bibliography, some EndNote fields). Per-paragraph atomisation would split them. | Field corruption on export. | Field-span scan across the body before classification; every paragraph touched by a multi-paragraph field is class R (§G.3). | Yes |
| C-08 | §I.1–I.2 | Corpus written and annotated solely by the developer/author; perturbations generated from the same gold used for rule development; no held-out split. | Measured recall would be inflated by construction (leakage); results not defensible. | Dev/test split, independent authors, sealed test set, rules frozen before test evaluation, Wilson-CI-based acceptance (§J.1–J.3). | Yes |
| C-09 | §D.4 `analytical` | Mode outputs a rewrite *and* notes, and may add "explicit contrast/cause connectives where already implied". Adding "because/therefore" is a causal upgrade by definition. | Directly violates the "do not invent causal explanations" requirement. | Analytical mode produces **no rewrite**; feedback only (§F.3). Connective insertion of causal class is BLOCK in all modes (R7). | Yes |
| C-10 | §C, §6 | Hunk-level partial acceptance re-verifies the resulting paragraph, but the claim graph of a partially accepted paragraph was never generated by the model or reviewed; v0.2 does not define what is compared. | A combination of hunks can create a swap that no single hunk contains. | Partial acceptance → full L1/L2 against the **original paragraph revision** (not the candidate); BLOCK on any finding (§D.5, §E.6). | Yes |

### 1.2 Major findings

| ID | v0.2 section | Problem | Correction | Pre-code |
|---|---|---|---|---|
| Mj-01 | §H.1 | Candidate list incomplete/inaccurate: `qwen3.5` was listed without tags; it is thinking-capable and multimodal (vision), so its weights and memory are larger than a text-only model of the same size; no official non-thinking tag found. `granite4:tiny-h` is a 7B-total/≈1B-active hybrid MoE, not a "4B-class" comparison. A dense small Granite (`granite4:micro`) was omitted. | Revised candidate table with confirmed/unverified status (§I.1). | Yes |
| Mj-02 | §H.2 | `think:false` assumed to work for hybrid models. | Benchmark pre-check P-think: any output containing reasoning traces or `<think>` fragments in > 0 of 30 probe calls disqualifies the tag for production use without a stripping proof (§I.3). | Yes |
| Mj-03 | §H.3–H.4 | Gate P-rel "≥ 97 % vs gold" measured by L2 itself. A verifier cannot certify a model against gold it also extracts. | Gold relations human-annotated; model-output relation correctness judged by human adjudication on a stratified subset; L2 used only to pre-screen (§I.4). | Yes |
| Mj-04 | §H.3 | ≈700 human judgements stated; no plan for rater availability; κ threshold only. | Reduced, fixed design: 48 items × ≤4 finalists × 2 raters = 384 judgements; preliminary automatic gates eliminate models first (§I.5). | Yes |
| Mj-05 | §D.4 | Modes mixed "level" and "scope" (`sentence` is a scope). Required levels (proofread / light / moderate / advanced / analytical feedback) not represented. | Mode = level; scope = paragraph / sentence(s) / expression; `concise` becomes an option (§F.2). | Yes |
| Mj-06 | §C undo/redo | Server-side linear undo stack across paragraphs coexists with TipTap's own undo; restore-to-revision semantics with undo unspecified. | Two-tier model: TipTap undo only inside an uncommitted manual-edit buffer; document operations log with explicit undo/redo semantics (§D.6). | Yes |
| Mj-07 | §F.1 | python-docx dropped, but section classification needs style resolution (`basedOn` chains, outline levels). | Specified lxml style resolver over `styles.xml` (§G.2). | Yes |
| Mj-08 | §F.5 T-RT13 | ECMA-376 XSD validation of Word output generally fails due to Markup Compatibility namespaces (w14/w15/w16*, `mc:Ignorable`). | Replace with structural validator: rels integrity, id uniqueness, content types, well-formedness, required-child checks; XSD optional after MCE preprocessing (§G.6). | Yes |
| Mj-09 | §F.5 T-RT14 | Only manual test for "Word opens without repair". | Keep manual M-tests but add automated proxy suite and a mandatory manual regression checklist per release (§G.6). | Yes |
| Mj-10 | §G token | Token delivered via URL query, then sessionStorage, plus HttpOnly cookie — two inconsistent mechanisms; token lands in browser history and shell command line. | Single mechanism: same-origin bootstrap `GET /api/v1/session` guarded by Host + `Sec-Fetch-Site`; token held in memory only (§H.2). | Yes |
| Mj-11 | §G | No temp-file policy, no shutdown behaviour, no project isolation statement. | §H.6–H.8. | Yes |
| Mj-12 | §A, §C | Jobs in memory; restart behaviour undefined; SSE reconnect semantics undefined. | Job table persisted in SQLite; interrupted jobs marked `interrupted`; SSE `Last-Event-ID` replay (§B.4). | Yes |
| Mj-13 | §D.6.1 standard mode | Numbers visible to model — reasonable — but no unit-normalisation contract for comparison; `23 °C`/`23°C`/`23 ºC` (ordinal indicator) mismatches. | Canonicalisation table (§E.2). | Yes |
| Mj-14 | §D.6.5 | Composite citation placeholder `⟦CITE:3-5⟧` changes the token set the verifier compares; ungrouping rules undefined. | Composite placeholders map 1:1 to an ordered list of original atoms; restored as a block; internal order invariant (§F.6). | Yes |
| Mj-15 | §I.3 | Latency/RAM criteria tied to "target hardware" never defined. | Minimum and reference hardware profiles (§I.6). | Yes |
| Mj-16 | §F.3 class P | Hyperlink display text "editable in advanced mode" contradicts "default protected"; bookmark-spanned text frozen but how frozen spans appear to the model is unspecified. | Frozen spans rendered as `⟦FIX:n⟧` placeholders with verbatim restoration; hyperlink text never editable in v1 (§G.3). | Yes |
| Mj-17 | §E.4 L3 | "Contrastive QA" with string compare; false alarm threshold 20 % with no sample size. | Kept as level 3, off by default; enablement requires measured FP rate with CI on ≥ 200 items (§E.7). | No |
| Mj-18 | §G secure delete | "Overwrite then unlink" implies secure erasure; pointless on SSD/VSS and misleading. | Ordinary deletion + `VACUUM`; documented limitation; advise BitLocker (§H.5). | Yes |

### 1.3 Moderate findings

| ID | v0.2 section | Problem | Correction | Pre-code |
|---|---|---|---|---|
| Mo-01 | §B | `uv.lock` *or* `requirements.lock` undecided. | `requirements.lock` with `--require-hashes`, generated by `pip-compile`; uv optional for developer (§C). | Yes |
| Mo-02 | §A deps | `defusedxml` redundant with hardened lxml parser + DOCTYPE rejection. | Removed (§B.3). | No |
| Mo-03 | §C | `docs_url=None, openapi_url=None` in prod but TS types generated from OpenAPI. | Types generated at build time from `app.openapi()` via script; schema not served (§D.1). | No |
| Mo-04 | §D.1 | Section classification heuristic; "Results and discussion" mixed sections need both rule sets. | `results_discussion` uses the stricter union of Results and Discussion constraints (§F.4). | Yes |
| Mo-05 | §H.3 grammar | LanguageTool offline requires Java; dependency boundary unclear. | Benchmark-only optional tool, never shipped in app; results labelled proxy (§I.4). | No |
| Mo-06 | §G | Port 8765 conflict not handled. | Start script probes; fixed fallback list 8765–8769; Host allow-list built from the bound port (§H.2). | No |
| Mo-07 | §B | Windows path length, OneDrive-synced `%LOCALAPPDATA%` not addressed. | Data dir check: refuse paths under OneDrive/Dropbox sync roots by default (manuscript would leave the machine); long-path-safe naming (§H.6). | Yes |
| Mo-08 | §D.2 | Diagnostic thresholds (45 words, 3 clauses) unsourced. | Thresholds configurable; defaults recorded as level 2; calibrated on dev set only (§F.5). | No |
| Mo-09 | §F.4.3 | Formatting inheritance heuristic list incomplete (character styles `w:rStyle`, `w:lang`, `w:rFonts` for symbol fonts). | Extended rule; any `w:rStyle` change or symbol font → protected (§G.5). | Yes |

### 1.4 Minor findings

| ID | Problem | Correction |
|---|---|---|
| Mi-01 | `pysbd` optional — undecided. | Mandatory, pinned; custom abbreviation list for "Fig.", "Eq.", "et al.", "i.e.", "approx.", "vs.". |
| Mi-02 | Placeholder delimiter fallback only mentioned. | Delimiter is a per-model profile value chosen by benchmark P-tok. |
| Mi-03 | Style profile feature retained. | Moved to future; not v1. |
| Mi-04 | Fixture list includes "Korean/Greek characters" without purpose. | Unicode fixture defined: Greek symbols, sub/superscript digits, U+2212, NBSP/thin spaces, CJK. |

### 1.5 Audit of v0.2 unresolved risks (§L)

| v0.2 risk | Assessment | v0.3 handling |
|---|---|---|
| L1 L2 coverage ceiling | Correct and under-stated; also affects false negatives silently if R8 is not surfaced per claim. | UNVERIFIED is a first-class status, per sentence; restricted modes when coverage is low (§E.6, §F.2). |
| L2 gold-relation bias | Critical (C-08). | §J.1. |
| L3 run-formatting heuristic | Correct. | Formatting-change report mandatory, per run (§G.5). |
| L4 Ollama nondeterminism | Correct. | Digest + version + hardware pinned; 3 seeds; report variance (§I.3). |
| L5 thinking-model leakage | Under-stated; now a hard gate (Mj-02). | §I.3 P-think. |
| L6 CPU-only latency | Correct. | Hardware profiles + per-length benchmark (§I.6). |
| L7 placeholder tokenisation | Correct. | P-tok gate. |
| L8 Word-only validation | Correct. | Manual regression checklist mandatory (§G.6). |
| L9 human-rating capacity | Correct (Mj-04). | §I.5. |
| L10 tag drift | Correct. | Digest pinning; benchmark invalidated on digest change. |
| *Missing in v0.2* | Model may emit text in another language, truncated output at `num_predict`, or refuse. | Postprocess checks: language id (stopword ratio), truncation (`done_reason == "length"` → failure), refusal pattern (§F.7). |
| *Missing in v0.2* | User manual edits can delete protected atoms in TipTap. | ProtectedSpan atoms non-deletable via keyboard; explicit "unprotect" action logged (§D.6). |

---

## A. Product scope and non-goals

### A.1 Scope (v1, mandatory)
1. Local, single-user, Windows 10/11 web application for refining the language of the user's own academic manuscripts (English).
2. Import `.docx`; edit at paragraph, sentence, or expression scope; review every change; export a new `.docx` (optionally with Word tracked changes).
3. Local inference via Ollama on `127.0.0.1` only.
4. Deterministic verification of textual and structured-relationship preservation between original and proposed text, with explicit UNVERIFIED reporting.
5. Revision history, restore, undo/redo, backup/restore, deletion.

### A.2 Verification levels — what the application does and does not do

| Level | Definition | v1 support |
|---|---|---|
| V-1 Textual preservation | Protected spans, numbers, units, citations, terms identical | **Yes**, deterministic (L1) |
| V-2 Structured relationship preservation | Same claims: subject–property–condition–value–direction–comparator–statistics–modality–causality–qualifiers | **Partial**, deterministic within extraction coverage (L2); otherwise UNVERIFIED |
| V-3 Scientific plausibility | Whether claims are physically/statistically sensible | **No.** Out of scope. The application never asserts plausibility. |
| V-4 External factual verification | Whether claims/citations match the literature | **No.** Requires network/literature access; out of scope for v1. |

A local LLM is used only for generation and, optionally, level-3 advisory comparison. **It is never used to certify correctness.**

### A.3 Non-goals (v1)
- Detecting AI-generated text; claiming outputs are undetectable; any optimisation against AI detectors.
- Reference/citation verification against databases; bibliography formatting.
- Writing new content (introductions, abstracts) from notes.
- Languages other than English; `.doc`, `.odt`, LaTeX, PDF input.
- Multi-user, sync, cloud, telemetry, plugins, Electron packaging.
- Editing headers/footers, footnote/endnote bodies, text boxes, captions, tables' structure (cell text editing is in scope with restrictions).
- Style-profile imitation (future, optional).

---

## B. Architecture and component responsibilities

### B.1 Topology
```
Windows host (single user)
 Browser tab ── http://127.0.0.1:<port>/  (SPA static, CSP 'self')
    │  fetch /api/v1/* with X-AW-Token (in-memory)      ▲ SSE /api/v1/jobs/{id}/events
    ▼                                                   │
 Python process: uvicorn (1 worker, asyncio) + FastAPI ─┘
   security  │ Host allow-list · Sec-Fetch/Origin checks · token · CSP · egress guard
   intake    │ ooxml_guard (zip limits, name checks, XML parser hardening)
   docx      │ package (zipfile) · reader (lxml atoms) · classify · styles · writer · xmlcheck
   segment   │ sections · sentences (pysbd) · scopes
   protect   │ detectors · plan · placeholders · realign
   refine    │ prompts · ollama_client · postprocess · candidates
   verify    │ L1 tokens · L2 claim graph · L3 advisory (flag) · report
   changes   │ changesets · hunks · operations log (undo/redo) · revisions
   store     │ project dirs · SQLite (WAL) · atomic writes · backup/restore · deletion
   jobs      │ single generation queue · persisted job table · cancellation
   ollama_client ──► http://127.0.0.1:11434  (only allowed egress)
```

### B.2 Component contracts
| Component | Inputs | Outputs | MUST |
|---|---|---|---|
| `ooxml_guard` | uploaded bytes | validated in-memory `ZipFile` or `IntakeRejected(reason)` | Run before any XML parse; enforce §H.3 limits |
| `docx.reader` | package | `Document{paragraphs[], atoms[], fields_span_map, styles}` | Never mutate package; record per-paragraph source hash |
| `docx.classify` | Document | edit class per paragraph (E/P/R) or refuse (X) | Allow-list semantics (§G.3) |
| `protect.plan` | paragraph, mode, protection level | model text, placeholder map, anchors, visible-checked spans | Deterministic; same input → same plan |
| `refine.pipeline` | scope, mode, section | `ChangeSet` (status pending/failed) | Never write to document |
| `verify` | original revision text+plan, candidate text | `Report` | L1, L2 always run; never PASS on L3 alone |
| `changes` | user actions | new revisions, operation log entries | Every applied change traceable to an operation |
| `docx.writer` | original package copy, accepted revisions | new `.docx` + `ExportReport` | Write to temp file in same dir, validate (§G.6), then atomic rename; never touch original |
| `jobs` | requests | SSE events, job rows | One generation at a time; cancellable |

### B.3 Dependencies (exhaustive for v1 runtime)
Backend (Python 3.12.x): `fastapi`, `uvicorn` (no `[standard]` extras needed; `h11` only), `httpx`, `lxml`, `pydantic`, `pydantic-settings`, `regex`, `pysbd`, `psutil` (health/memory display). Standard library: `zipfile`, `sqlite3`, `hashlib`, `secrets`.
Frontend (build-time only Node 20 LTS): `react`, `react-dom`, `typescript`, `vite`, `tailwindcss`, `@tiptap/react`, `@tiptap/starter-kit`, `@tiptap/pm`, `zustand`, `diff-match-patch`.
Benchmark-only (not shipped): `languagetool` server JAR (optional), `scipy` (CIs), `pandas`.
Test-only: `pytest`, `hypothesis` (fuzzing), `python-docx` (oracle), `playwright` (Python), LibreOffice (optional).
Excluded: Docker, Redis, Celery, Postgres, LangChain/LlamaIndex, spaCy, defusedxml, Electron, any analytics SDK.

### B.4 Jobs, streaming, cancellation
- Queue: `asyncio.Queue`, concurrency 1 for generation; verification and DOCX tasks run in a `ThreadPoolExecutor(max_workers=2)` (CPU-bound lxml), never concurrently on the same project (per-project `asyncio.Lock`).
- Job row in SQLite: `{id, project_id, kind, state: queued|running|done|failed|cancelled|interrupted, created, started, ended, error_code, changeset_id}`.
- On startup, any `running`/`queued` job → `interrupted`; UI offers re-run.
- SSE: events carry monotonically increasing `id`; server keeps the last 500 events per job in memory; `Last-Event-ID` reconnect replays; after job end, `GET /jobs/{id}` is authoritative.
- Cancel: sets job flag, closes the `httpx` streaming response (Ollama stops generation when the client disconnects — verified in benchmark pre-checks, P-cancel), state `cancelled`, partial output discarded.
- Timeouts: connect 2 s; inter-chunk 90 s (CPU loads); total = `max(120 s, 4 × expected_time)` from model profile.

### B.5 Windows compatibility, install, uninstall, offline startup
- `install.ps1` (online, once): checks Python 3.12, Ollama, creates `.venv`, `pip install --require-hashes -r requirements.lock` (or from bundled `wheels/`), copies prebuilt `frontend/dist` (built in repo CI; Node not needed on the user machine), `ollama pull` of selected model tag, records digest to `config.toml`.
- `start.ps1`: verifies Ollama reachable on loopback, warns if `OLLAMA_HOST` not loopback, chooses port, launches uvicorn, opens default browser at `http://127.0.0.1:<port>/`.
- `uninstall.ps1`: removes app dir and `.venv`; asks separately whether to delete `%LOCALAPPDATA%\AcademicWrite` (manuscript data) and whether to `ollama rm` models. Default: keep data.
- Offline startup requirement: with all network adapters disabled, `start.ps1` + full E2E pass (test OFF-1).

---

## C. Project folder structure

```
academicwrite/
├─ docs/
│  ├─ spec/AcademicWrite_Spec_v0.2.md  AcademicWrite_Spec_v0.3.md
│  ├─ decisions/                      # ADRs for any SHOULD deviation
│  └─ manual_tests/M-checklist.md
├─ backend/
│  ├─ pyproject.toml  requirements.in  requirements.lock (hashed)
│  └─ app/
│     ├─ main.py  config.py  errors.py  logging.py
│     ├─ security/   middleware.py  session.py  egress_guard.py  csp.py
│     ├─ api/        session.py health.py models.py projects.py paragraphs.py refine.py
│     │              changesets.py operations.py revisions.py verify.py export.py
│     │              glossary.py lexicon.py settings.py backup.py jobs.py
│     ├─ domain/     document.py atom.py protection.py claim.py changeset.py
│     │              revision.py operation.py report.py job.py
│     ├─ intake/     ooxml_guard.py
│     ├─ docx/       package.py reader.py styles.py fields.py classify.py writer.py
│     │              runmap.py xmlcheck.py c14n.py trackchanges.py
│     ├─ segment/    sections.py sentences.py scopes.py
│     ├─ protect/    detectors/{citation,quantity,unit,chem,math,xref,acronym,term,digitrun}.py
│     │              canonical.py plan.py placeholders.py realign.py
│     ├─ refine/     pipeline.py prompts.py diagnostics.py postprocess.py candidates.py
│     ├─ verify/     l1_tokens.py alignment.py
│     │              l2/{lexicon,clauses,patterns,binder,graph,compare,rules}.py
│     │              l3_advisory.py report.py
│     ├─ changes/    hunks.py changesets.py operations.py revisions.py
│     ├─ store/      paths.py projects.py db.py migrations/ atomic.py backup.py delete.py
│     ├─ jobs/       queue.py events.py
│     ├─ llm/        ollama_client.py model_profiles.toml
│     └─ prompts/<profile>/<mode>/<section>.txt  (hash recorded per changeset)
├─ frontend/
│  ├─ package.json  package-lock.json  vite.config.ts  tailwind.config.ts  index.html
│  └─ src/
│     ├─ api/        client.ts  sse.ts  types.gen.ts
│     ├─ state/      session.ts project.ts changesets.ts operations.ts jobs.ts health.ts
│     ├─ editor/     Editor.tsx  extensions/{ProtectedSpan,ParagraphMeta,HunkMark,ScopeSelection,ReadOnlyBlock}.ts
│     ├─ views/      DocumentView.tsx ReviewView.tsx CompareView.tsx HistoryView.tsx
│     ├─ components/ HunkCard.tsx IntegrityPanel.tsx ClaimTable.tsx ModelStatus.tsx JobBar.tsx
│     │              ImportDialog.tsx ExportDialog.tsx GlossaryEditor.tsx LexiconEditor.tsx
│     │              SettingsDialog.tsx BackupDialog.tsx ErrorBanner.tsx
│     └─ lib/        diff.ts  format.ts
├─ bench/
│  ├─ corpus/        dev/ test_sealed/ (encrypted-at-rest zip, see §J.1) README.md
│  ├─ annotations/   schema.json guidelines.md dev/ test/
│  ├─ perturb/       operators.py  (operator definitions frozen before test generation)
│  ├─ paraphrase/    dev/ test/
│  ├─ run_model_bench.py  run_verifier_eval.py  score.py  stats.py
│  ├─ rating/        static HTML rating tool (served from 127.0.0.1)
│  └─ results/<date>_<profile>_<digest12>/
├─ tests/
│  ├─ unit/  verify/  docx/{fixtures,malformed,regression}/  security/  api/  e2e/  offline/
│  └─ reports/
└─ scripts/  install.ps1 start.ps1 uninstall.ps1 build_frontend.ps1 gen_types.py verify_offline.ps1
```

---

## D. API and data model

### D.1 Conventions
- Base `/api/v1`; JSON UTF-8; all non-static requests require `X-AW-Token`.
- Errors: `{"error":{"code":str,"message":str,"detail":obj|null,"retryable":bool,"trace_id":str}}`.
- Concurrency control: every mutating request on a paragraph carries `base_rev`; mismatch → 409 `REVISION_CONFLICT`.
- Idempotency: mutating POSTs accept `Idempotency-Key`; repeated key returns the first result.
- OpenAPI generated at build (`scripts/gen_types.py`), not served at runtime.

### D.2 Core data model (persisted in `project.sqlite`)

```
Project       {id, title, created, updated, source_sha256, source_filename, schema_version,
               discipline, spelling: en-GB|en-US, protection_default}
Paragraph     {id, project_id, order, part: document|table_cell, xml_path, style_id,
               section_type, edit_class: E|P|R, refuse_reason?, source_hash, current_rev}
Revision      {paragraph_id, rev, text, atoms_json, origin: import|model|manual|restore|undo|redo,
               operation_id, created}
Atom          (json) {kind: TEXT|OPAQUE|FROZEN, id, text?, xml_ref?, rpr_ref?, protected_type?}
ProtectionPlan{paragraph_id, rev, level, placeholders[{token, atom_ids[], type, hint, anchor}],
               checked_spans[{type, canonical, start, end}], density}
ChangeSet     {id, project_id, paragraph_id, base_rev, scope{type, sent_ids?, char_range?},
               mode, options, model{name, digest}, prompt_hash, candidate_text,
               status: pending|failed|partially_applied|applied|rejected|superseded,
               report_id, created}
Hunk          {id, changeset_id, order, orig_range, new_range, orig_text, new_text,
               findings[], state: pending|accepted|rejected}
Report        {id, overall: BLOCK|WARN|UNVERIFIED|NO_ISSUES_DETECTED,
               findings[{check_id, layer, severity, orig_spans, new_spans, claim_ids, message}],
               coverage{sentences_total, sentences_fully_bound, quantities_unbound}}
Claim / Graph (json, §E.3)
Operation     {id, project_id, seq, kind: apply_hunks|manual_edit|restore|unprotect,
               paragraph_ids[], before_revs[], after_revs[], override?{reason, check_ids},
               undone: bool, created}
Job           (§B.4)
ExportRecord  {id, project_id, path, sha256, track_changes, created, report_json}
```

### D.3 Endpoints

**Session & health**
| Method | Path | Behaviour |
|---|---|---|
| GET | `/session` | Returns `{token}` only if Host valid and `Sec-Fetch-Site ∈ {same-origin, none}`; token rotates per process start |
| GET | `/health` | `{backend, ollama:{reachable, version, loopback_only, lan_exposed}, model:{name, digest, digest_matches_profile, state: ready|missing|cold|loading}, egress_guard, data_dir:{path, synced_folder: bool}, queue_depth}` |
| GET | `/models` | Installed models with `/api/show` details; flags `approved` (passed §I gates) |
| PUT | `/models/active` | `{name}`; non-approved requires `{acknowledge_unapproved: true}` and restricts modes to proofread |
| POST | `/models/warmup` | Loads model; returns load time |

**Projects & paragraphs**
| Method | Path | Behaviour |
|---|---|---|
| GET | `/projects` | List |
| POST | `/projects` | multipart `.docx`; returns `{project, paragraphs[], import_report}`; import_report lists every R/X paragraph and refused element with reason |
| GET | `/projects/{id}` | Project + paragraphs (current revision) |
| PATCH | `/projects/{id}` | `{title?, spelling?, section_overrides?{pid: type}, protection_default?}` |
| DELETE | `/projects/{id}` | Deletes project dir + rows (§H.5); `{confirm_title}` required |
| PUT | `/projects/{id}/paragraphs/{pid}` | Manual edit `{base_rev, text_with_atoms}` → verification run → Operation `manual_edit` (BLOCK on protected-atom loss) |
| GET | `/projects/{id}/paragraphs/{pid}/revisions` | Revision list |
| GET | `/projects/{id}/paragraphs/{pid}/revisions/{rev}` | Revision text |
| POST | `/projects/{id}/paragraphs/{pid}/restore` | `{rev, base_rev}` → new revision (verified against the restored-from text; no rewrite of history) |

**Refinement**
| Method | Path | Behaviour |
|---|---|---|
| POST | `/projects/{id}/refine` | `{paragraph_id, base_rev, scope:{type: paragraph|sentences|expression, sent_ids?, char_range?}, mode: proofread|light|moderate|advanced, options:{concise: bool, candidates: 1|2}, protection: conservative|standard}` → 202 `{job_id}` |
| POST | `/projects/{id}/feedback` | Analytical feedback `{paragraph_id, base_rev}` → 202 `{job_id}`; result is `Feedback{items[]}`, never a ChangeSet |
| GET | `/jobs/{id}` | Snapshot |
| GET | `/jobs/{id}/events` | SSE: `queued, started, model_loading, token, candidate_done, verify_done, changeset, feedback, error, end` |
| POST | `/jobs/{id}/cancel` | 202 |

**Change review**
| Method | Path | Behaviour |
|---|---|---|
| GET | `/projects/{id}/changesets?status=&paragraph_id=` | List |
| GET | `/changesets/{id}` | ChangeSet + hunks + report + claim graphs |
| POST | `/changesets/{id}/apply` | `{hunk_ids[], base_rev, override?{reason ≥ 15 chars, check_ids[]}}` → re-verifies combined result against original revision (§E.6); 422 `INTEGRITY_BLOCK` with report if BLOCK and no matching override |
| POST | `/changesets/{id}/reject` | — |
| POST | `/changesets/{id}/edit` | `{text}` user-modified candidate → new verification, new hunks |

**Operations (undo/redo)**
| Method | Path | Behaviour |
|---|---|---|
| GET | `/projects/{id}/operations` | Ordered log |
| POST | `/projects/{id}/undo` | Reverts the latest non-undone operation by writing new revisions equal to `before_revs` (if `current_rev == after_rev` for every paragraph; else 409) |
| POST | `/projects/{id}/redo` | Re-applies the latest undone operation under the same condition; any new operation clears the redo stack |

**Verification, export, configuration, backup**
| Method | Path | Behaviour |
|---|---|---|
| POST | `/projects/{id}/verify` | `{paragraph_id, rev_a, rev_b}` ad-hoc comparison |
| GET | `/projects/{id}/export/preview` | Dry run: which paragraphs would be written/skipped, formatting changes |
| POST | `/projects/{id}/export` | `{track_changes: bool (default true), filename?}` → job → `ExportRecord`; file saved under project `exports/` and downloadable |
| GET | `/exports/{id}/file` · `/exports/{id}/report` | |
| GET/PUT | `/glossary` · `/projects/{id}/lexicon` · `/settings` | Lexicon = entity/property lexicon for L2 |
| POST | `/backup` | `{project_ids[] | all}` → zip download |
| POST | `/restore` | multipart; restores as new project ids |
| DELETE | `/projects/{id}/history` | `{keep_current: true}` purges revisions/changesets/operations except current |

---

## E. Scientific integrity and relationship verification

### E.1 Layers and statuses
- **L1 Textual invariants** (deterministic): BLOCK/WARN.
- **L2 Structured relationship preservation** (deterministic, coverage-limited): BLOCK/WARN/UNVERIFIED.
- **L3 Advisory** (local model, level 3, off by default): WARN only.
- Report `overall` precedence: BLOCK > WARN > UNVERIFIED > NO_ISSUES_DETECTED. The UI never displays "verified", "correct" or "PASS".

### E.2 L1 checks
| ID | Check | Severity |
|---|---|---|
| L1-Q0 | **Digit-run invariance (catch-all):** multiset of maximal digit sequences (incl. decimal separators, sub/superscript digits normalised) identical, independent of any detector | BLOCK |
| L1-Q1 | Canonical quantity multiset `(value, unit, operator, uncertainty)` identical | BLOCK |
| L1-Q2 | Number words ↔ digits: "three specimens" vs "3 specimens" treated equal; any other change | BLOCK |
| L1-P | Placeholder multiset; no invented, duplicated, missing; order of OPAQUE atoms invariant | BLOCK |
| L1-C | Citation atoms identical; each in same aligned sentence and same clause anchor | BLOCK |
| L1-T | Glossary terms, acronyms, cross-refs, chemical formulas, specimen codes verbatim (count per type) | BLOCK |
| L1-N | Negation markers count per aligned sentence | WARN (BLOCK if L2 polarity rule also fires) |
| L1-L | Length ratio outside mode band | WARN |
| L1-X | Output language not English / truncated (`done_reason=length`) / refusal | BLOCK (changeset `failed`) |

Canonicalisation (`canonical.py`): `°`/`º`/`˚` → `°`; `−`/`–` (as minus) → `-`; NBSP/thin space removed for comparison; `×10^-3`, `×10⁻³`, `e-3` equivalent; `wt%`/`wt.%`/`wt. %` equivalent; `%` vs "percent" equivalent; decimal comma per project setting; trailing zeros significant (`2.50` ≠ `2.5`, reported precision is meaningful).

### E.3 L2 representation

#### Paragraph claim graph
```
Entity      {id, surface, canonical, kind: configuration|material|specimen|group|treatment|model}
Property    {id, surface, canonical, family}          # family groups confusable properties
Condition   {id, kind: temperature|humidity|time|medium|cycles|load|rate|other, qty?, text}
Quantity    {id, value, unit, op, uncertainty?{type: ±|SD|SE|CI|range, value, level?}, n?}
Baseline    {kind: relative_to_entity|relative_to_initial|relative_to_condition|absolute, ref_id?}
Claim       {id, sent_id, clause_id,
             subject: Entity?, property: Property?, conditions: [Condition],
             value: Quantity?, change: {direction: + | - | 0 | ~ | null,
                                        form: percent|ratio|absolute|qualitative, baseline: Baseline?},
             comparator: Entity?,
             stats: {significance: sig|nonsig|unstated, p?: Quantity, test?: str, ci?: Quantity},
             modality: asserted|hedged(level 1-3)|negated|hypothesis|conditional,
             relation: observed|correlated|caused_by|attributed_to|consistent_with|contrasts_with,
             qualifiers: [QualifierRef], binding: full|partial|none, provenance: {rule_id, spans}}
Qualifier   {id, kind: scope|limitation|exception|condition, text_span, attached_to: claim_id|sentence}
Edge        {from_claim, to_claim, kind: contrast|support|elaboration|same_subject_elided}
Graph       {entities, properties, conditions, quantities, claims, qualifiers, edges,
             unbound_quantities: [Quantity], coverage}
```

#### Lexicons
- **Entity lexicon (per project):** built at import from table header/first-column cells, capitalised designators (`configuration|sample|specimen|laminate|group|batch|series` + id), coded ids (`[A-Z]{1,3}\d{0,3}[a-z]?`), fibre/matrix strings (`\w+/\w+(?:/\w+)?`), treatment phrases (`(alkali|silane|NaOH|untreated|treated|aged|unaged|dry|wet|control)`), editable by the user. Ambiguous designators (single letters also used as variables) require user confirmation in the lexicon UI before L2 treats them as entities.
- **Property lexicon:** seed list with families, e.g. family `interlaminar` = {ILSS, interlaminar shear strength, short-beam strength}; family `interface` = {IFSS, interfacial shear strength}; `tensile` = {tensile strength, UTS}; `tensile_stiffness` = {tensile modulus, Young's modulus, E}; `flexural`, `impact`, `moisture` = {water uptake, moisture content, Mₘ}, `diffusion` = {D, diffusivity, diffusion coefficient}, `thermal` = {Tg, glass transition}, `dynamic` = {storage modulus E′, tan δ}, `porosity`, `fibre_volume`. Synonyms within a family are equal; across families never equal.
- **Hedge lexicon:** level 1 weak (may, might, could, possibly, appears, suggests), level 2 moderate (likely, indicates, is consistent with), level 3 strong (demonstrates, shows, confirms, proves, establishes, clearly). Modal of possibility + verb = hedged.
- **Causal lexicon:** caused_by/attributed_to markers (because, due to, owing to, caused, led to, resulted in, attributed to, responsible for, therefore, thus, hence, consequently, as a result, drives, governs, induces) vs correlated (associated with, correlated with, coincided with, accompanied by, along with, concurrently).
- **Limitation lexicon:** however, although, but, only, limited to, within, under the conditions, at least, in this study, not tested, remains unclear, further work, cannot be excluded, preliminary, caution.

#### Extraction pipeline (deterministic)
1. Sentence split (pysbd + abbreviation list); clause split on `;`, `whereas`, `while`, `but`, `although`, `compared with/to`, `relative to`, `than`, coordinating `and` between finite clauses.
2. Tag spans: quantities, entities, properties, conditions, hedges, causal/limitation markers, negation, significance markers.
3. Pattern binder: ordered rule list (`l2/patterns.py`), each rule has id, regex over tagged sequence, slot assignments, and unit tests. Minimum v1 rule families: subject-verb-change-property; property-of-subject-changed-by-qty; qty-higher/lower-than-comparator; property-value-at-condition; comparative ellipsis; significance clause; parenthetical stats `(p < 0.05)`, `(mean ± SD, n = 5)`; "from X to Y" (absolute pair → derive change form); "X-fold"; "by X% relative to".
4. Inheritance (explicit, limited): within a sentence, an elided property/condition is inherited from the nearest preceding clause in the same sentence **only** when the elided clause has a subject and a quantity but no property; inheritance recorded in provenance. Cross-sentence inheritance only via explicit anaphora list ("the latter", "the former", "this configuration", "it") resolved to the immediately preceding sentence's subjects when exactly one candidate of matching kind exists; otherwise binding stays partial.
5. Anything not bound → `unbound_quantities` and claim `binding: partial|none`. **No guessing.**

### E.4 L2 comparison rules
Comparison runs on graphs G_o (original revision of the paragraph + frozen context) and G_n (candidate). Claims are matched by `(subject, property family, condition set)` where bound, and additionally by **value anchoring**: each quantity in G_o is located in G_n by canonical identity (L1 guarantees the multiset is identical), and its bound slots are compared.

| Rule | Detects (failure case) | Trigger | Severity |
|---|---|---|---|
| R1 | Value re-associated with another subject (A) | Same quantity, different bound subject | BLOCK |
| R2 | Direction flip (B) | Same quantity & subject, direction changed (+↔−, ±↔0) | BLOCK |
| R3 | Comparator changed/omitted (G) | Comparator entity differs or removed | BLOCK (removed: BLOCK; added where original had none: WARN) |
| R4 | Condition moved (I) | Same quantity, condition set differs | BLOCK |
| R5 | Significance change (D) | `nonsig`/`unstated` → `sig`, or `sig` → other, or p/CI changed or dropped | BLOCK (except `unstated`→`unstated`) |
| R6 | Modality strengthening (E) | hedged→asserted, hedge level decreases in certainty (1→3), hypothesis/conditional→asserted, negated→asserted | BLOCK; weakening → WARN |
| R7 | Correlation→causation (C) | relation observed/correlated/consistent_with → caused_by/attributed_to; or causal connective inserted between two claims without a causal marker in original | BLOCK |
| R8 | Coverage gap (L, M) | Any sentence with ≥ 1 unbound quantity or any claim with binding≠full | UNVERIFIED (per sentence) |
| R9 | Cross-sentence move (J) | Quantity or claim appears in a different aligned sentence | BLOCK if any slot changed; else WARN |
| R10 | Qualifier/limitation loss (F) | Any original Qualifier with no matching qualifier (same kind, attached to the matched claim or sentence) in G_n | BLOCK for `limitation`/`exception`/`condition`; WARN for `scope` |
| R11 | Property confusion (H) | Same quantity & subject, property family differs | BLOCK |
| R12 | Baseline/percentage semantics (K) | Change form or baseline differs: e.g. "A 23 % higher than B" → "B 23 % lower than A"; percent ↔ percentage points; "reduced by 72 %" ↔ "reduced to 72 %"; "X-fold increase" ↔ "X % increase"; retention ↔ loss | BLOCK |
| R13 | Uncertainty loss | ±/SD/CI/n dropped or changed | BLOCK |
| R14 | Claim added | Claim in G_n with no source in G_o (incl. new mechanism sentences) | BLOCK if it contains a quantity, causal relation, or property; else WARN |
| R15 | Claim dropped | Claim in G_o with no counterpart in G_n | BLOCK (concise option: WARN if the claim is duplicated elsewhere in the paragraph) |
| R16 | Contrast edge changed | `contrasts_with` edge removed or turned into `support` | WARN |
| R17 | Generalisation | Quantifier scope widened (some→most/all; "in this study"→ removed; specific material→class noun, e.g. "flax/epoxy" → "natural fibre composites") | BLOCK |
| R18 | Neighbour contamination (J) | A G_n claim uses an entity, property, or quantity that occurs only in the frozen context, not in the editable scope | BLOCK |

#### Required failure-case treatment

| Case | Deterministic detection realistic? | Representation | BLOCK / WARN / UNVERIFIED | When extraction is ambiguous | Never auto-accepted |
|---|---|---|---|---|---|
| A wrong group | Yes, when subject binding is full in both | Claim.subject + value anchoring | R1 BLOCK | UNVERIFIED for that sentence; hunk shows "relationship not verified" | Any change of subject attached to a quantity |
| B direction flip | Yes, lexicon-based direction words, comparatives, "from X to Y" | change.direction | R2 BLOCK | UNVERIFIED if direction word not bound to a quantity | Any polarity word change in a quantity-bearing clause |
| C correlation→causation | Partly: marker-based; implicit causation via syntax ("X, reducing Y") is missed | Claim.relation, Edge | R7 BLOCK | WARN `CAUSAL_AMBIGUOUS` when a participial clause appears/changes | Insertion of any causal-lexicon item |
| D nonsig→sig | Yes for explicit markers and p-values | stats | R5 BLOCK | UNVERIFIED if "significant" appears without stats context (statistical vs colloquial meaning) — BLOCK if "significant(ly)" is added at all (L1-T on that word) | Adding or removing "significant(ly)", p, CI |
| E may improve→improves | Yes | modality + hedge level | R6 BLOCK | WARN if hedge lexicon miss | Any hedge removal or certainty increase |
| F limitation lost | Partly: marker-based | Qualifier | R10 BLOCK | WARN `QUALIFIER_UNMATCHED` when qualifier text changed but marker retained | Deletion of limitation/exception/condition clause |
| G comparator changed/omitted | Yes when comparator bound | Claim.comparator | R3 BLOCK | UNVERIFIED | Removing "compared with/relative to/than" phrases |
| H property confusion | Yes within lexicon families; unlisted properties missed | Property.family | R11 BLOCK | UNVERIFIED if property not in lexicon (prompt user to add) | Property term substitution across families |
| I condition moved | Yes for quantified conditions; qualitative ("wet", "aged") via lexicon | Condition set | R4 BLOCK | UNVERIFIED | Changing the condition attached to a quantity |
| J neighbour contamination | Yes via frozen-context provenance | provenance + R18 | R18 / R9 BLOCK | BLOCK (conservative: any token present only in context) | Any context-only entity/quantity in output |
| K baseline/percentage | Yes for listed forms; arithmetic re-expressions (e.g. converting 23 % increase to 1.23×) are BLOCK, not evaluated for equivalence | change.form + baseline | R12 BLOCK | UNVERIFIED | Any change in percentage form, baseline, "by/to", "points" |
| L multiple configurations / nested comparisons | Partially; nested comparatives ("D's increase was twice that of B") beyond patterns | Graph edges + partial bindings | R8 UNVERIFIED; any matched R1–R18 still BLOCK | Paragraph-level refinement of such sentences restricted to `proofread`/`light`; sentence shown with "complex relations — review manually" | Moderate/advanced rewriting of sentences with ≥ 3 entities and ≥ 2 comparisons |
| M relation spread across paragraph/table/figure | No for tables/figures (values not in text); partial across sentences | unbound_quantities, xref atoms | R8 UNVERIFIED | Always UNVERIFIED; cross-refs preserved by L1-T | Any change to a sentence referencing a table/figure value whose quantity is unbound |

### E.5 Alignment
Monotone DP alignment over sentences (1:1, 1:2, 2:1) using content-lemma Jaccard + shared quantities/citations/entities (weights fixed in config, calibrated on dev only). Unaligned original sentences → R15; unaligned new sentences → R14. Alignment confidence < threshold → paragraph UNVERIFIED for R9/R18 and changeset restricted to per-sentence hunks.

### E.6 Partial hunk acceptance
Applying a subset of hunks produces text T′. T′ is verified against the **original revision** with L1+L2. Any BLOCK → apply refused (422) unless overridden. The UI pre-computes verification for the selected hunk set before the user confirms (debounced).

### E.7 L3 advisory (level 3, default OFF)
Constrained-JSON claim extraction by the active model on both texts, compared using the same rules; differences shown as "advisory". May only add WARN. Enabling requires a measured false-alarm rate ≤ 15 % (upper 95 % Wilson bound ≤ 20 %) on ≥ 200 dev paraphrase pairs **and** no increase in user-visible noise in the HIL study. Never affects BLOCK/UNVERIFIED decisions.

### E.8 What is never automatically accepted
No change reaches the document without user action. Additionally, overrides are **not permitted** (BLOCK is final; user must edit text manually) for: L1-Q0/Q1 numeric changes, L1-C citation changes, L1-P placeholder violations, R1, R2, R5, R12, R13. Other BLOCKs permit override with a reason, logged in the Operation.

---

## F. Academic writing and refinement engine

### F.1 Principles (MUST)
Passive voice, nominal style, long sentences and formal vocabulary are not defects. The engine MUST NOT: replace technical terms with general synonyms; add mechanisms, causes, references, or quantities; strengthen evidence or remove hedges; inflate conclusions or generalise scope; homogenise all paragraphs to one rhythm (no global targets for sentence length or voice). These are enforced by prompts **and** verified by L1/L2 (R6, R7, R14, R17, L1-T).

### F.2 Modes (level) × scope

| Mode | Purpose | Allowed operations | Forbidden | Length band | Protection default | Allowed when L2 coverage < 70 % or entity/comparison-dense |
|---|---|---|---|---|---|---|
| `proofread` | Correctness | Spelling, grammar, punctuation, agreement, articles, obvious word errors | Reordering, lexical substitution beyond correction, voice change | 0.95–1.05 | standard | Yes |
| `light` | Light refinement | proofread + local word choice, connective variety (non-causal), removal of empty phrases, de-stacking ≥ 3-nominal chains | Clause reordering across sentence boundary, sentence merge/split | 0.9–1.1 | standard | Yes |
| `moderate` | Natural academic refinement | light + sentence split/merge within paragraph, clause reordering, voice change where agent is unclear in interpretive claims | Moving claims between sentences that change subject binding; adding connectives of causal class | 0.8–1.15 (concise: 0.65–1.0) | standard | Sentence scope only |
| `advanced` | Substantial restructuring | moderate + paragraph-level reorganisation for topic-sentence/flow | Any content addition/removal; available only for Introduction/Literature review/Discussion/Conclusions; disabled for Methods/Results | 0.75–1.2 (concise: 0.6–1.0) | conservative | No |
| `feedback` (analytical) | Critique only | Returns list of items: `{type: logic_gap|unsupported_claim|missing_hedge|overclaim|ambiguous_reference|missing_comparator|undefined_term|structure, span, question}`; each item is a **question or observation**, never a replacement text containing scientific content | Rewriting; suggesting mechanisms, data, citations | n/a | n/a | Yes |

Scope: `paragraph` | `sentences` (1–3 contiguous sentence ids) | `expression` (≤ 25 words, returns ≤ 3 alternatives, rest of sentence frozen). Expression scope is limited to `proofread`/`light`/`moderate` operations.

Options: `concise` (applies concision band; R15 relaxed only for duplicates), `candidates` (1|2).

### F.3 Feedback mode output contract
JSON schema-constrained (`format` param). Postprocess rejects items whose `question` contains a quantity, a citation pattern, or a causal-lexicon assertion not phrased as a question. Example acceptable: "The 72 % IFSS loss is attributed to hydrolysis without a supporting reference or measurement — is this inferred or measured?" Example rejected: "Add that hydrolysis of the phenolic matrix causes the loss."

### F.4 Section instruction blocks
Section type determined by heading classification (§G.2), overridable per paragraph. Each block is a fixed text file; the content is normative:

- **Introduction:** keep funnel (context → gap → objective); preserve gap statement strength; keep each citation attached to the clause it supports; keep objective explicit; no new claims about prior work.
- **Literature review:** preserve attribution (who found what); never merge findings of different citations into one claim; keep contrasts between sources; no evaluative adjectives added about cited work; citation-dense rules (§F.6).
- **Methods:** passive and procedural order are conventional and must be retained unless the user selects `moderate` and the step order is unchanged; preserve all parameters, equipment, standards (ASTM/ISO/EN codes verbatim), specimen counts, conditioning protocol; `advanced` disabled.
- **Results:** report only; no interpretation added; preserve each number–property–condition–group association and statistics; keep figure/table references; tense of reporting preserved; `advanced` disabled.
- **Discussion:** preserve hedge levels and causal direction; mechanisms remain as tentative as the original; preserve limitations; comparisons with literature keep their citation anchors.
- **Conclusions:** no new claims, numbers, or generalisation beyond the body; limitations and future work preserved.
- **Results and discussion:** union of Results and Discussion constraints; `advanced` disabled.
- **Abstract / other:** proofread, light only by default.

### F.5 Diagnostics (descriptive)
Computed per paragraph and shown to the user; only flagged items (rules below) become ≤ 4 instructions in `light`/`moderate`/`advanced`. Thresholds configurable, defaults level 2, calibrated on dev set only.
- Nominal stack: ≥ 3 nominalisations linked by "of"/prepositions within 8 tokens, none in glossary.
- Empty phrase list hit (configurable list).
- Ambiguous agent: ≥ 3 consecutive agentless passives in Discussion/Introduction **where** the claim is interpretive (hedge or causal marker present).
- Sentence > 50 words with ≥ 2 quantity-bearing clauses and ≥ 2 entities → suggest split (moderate only).
- Repeated sentence openers (≥ 3 of the same first lemma in a paragraph).
Never flagged: passive in Methods; technical nominal compounds; long enumerations of conditions.

### F.6 Protection system
#### Span handling
| Class | Conservative | Standard |
|---|---|---|
| Citation (text pattern or field) | Placeholder | Placeholder |
| OPAQUE XML atom (field, OMML, note ref, drawing, sym, hyperlink, comment/bookmark-spanned text) | Placeholder/FIXED | Placeholder/FIXED |
| Inline math (LaTeX, Unicode math, OMML) | Placeholder | Placeholder |
| Quantity with unit, statistics | Placeholder with hint | Visible, L1-checked |
| Chemical formula, specimen code, standard code | Placeholder | Visible, L1-checked |
| Glossary term, acronym, cross-ref | Visible, L1-checked | Visible, L1-checked |
| URL/DOI | Placeholder | Placeholder |
| Sub/superscripted characters in TEXT runs | Visible as Unicode if a mapping exists and run otherwise unchanged; else placeholder | Same |

#### Placeholder format & grammar
`⟦TYPE:n|hint⟧` where hint ∈ fixed vocabulary {`a citation`, `citations`, `a symbol`, `an equation`, `a quantity`, `a temperature`, `a percentage`, `a duration`, `a material code`, `a reference to a figure/table`, `a URL`} with grammatical number. Delimiter per model profile (`⟦⟧` or `[[ ]]`) chosen by P-tok. Composite citation placeholders allowed only for contiguous citation atoms, mapped to an ordered list; internal order invariant.

#### Failure handling
| Event | Action |
|---|---|
| Missing placeholder | 1 retry with explicit missing list; then `failed` |
| Duplicated / invented | `failed` (no retry for invented; one retry for duplicated) |
| Mangled but unambiguous (`[CITE:2]`) | Normalise, WARN `PH_NORMALISED` |
| Moved to another clause/sentence (citation) | BLOCK L1-C |
| Reordered OPAQUE atoms | BLOCK L1-P |

#### Density limits
`ρ = protected chars / total chars` (placeholders + checked spans). ρ > 0.35 (standard) or > 0.25 (conservative) → paragraph scope limited to `proofread`/`light`; sentence/expression scopes still allowed. ≥ 6 citations in a paragraph → `advanced` disabled.

#### Acronyms
First occurrence of each defined acronym in the document keeps the definition form; acronym/expansion swaps → BLOCK L1-T (terminology). Plural forms normalised.

### F.7 Generation and postprocessing
- Request: `/api/chat`, `stream: true`, `think: false` (only for profiles with `supports_think_param = true`), options from model profile, `keep_alive: "30m"`.
- Output contract: text between `<out>` and `</out>`; anything outside discarded; missing tags → one retry, then `failed`.
- Reject: residual `<think>`/reasoning markers; `done_reason == "length"`; English stopword ratio below threshold; refusal patterns; identical-to-input for non-proofread modes (reported as "no change proposed", not failure).
- Candidates = 2: second candidate at temperature + 0.1; pick fewer BLOCK, then fewer WARN, then smaller edit distance; both stored.

---

## G. DOCX import, editing and export

### G.1 Package handling
- Reading via `zipfile` + `lxml` only. python-docx is a test oracle, not a runtime dependency.
- The uploaded file is stored as `original.docx`, set read-only (file attribute), SHA-256 recorded; never opened for writing.
- Export: copy original bytes to `exports/.tmp-<uuid>.docx` → rebuild ZIP writing unmodified members by copying their raw compressed data where possible (`ZipFile` member copy preserving compress_type, date_time, external_attr) and modified parts re-serialised → validate (§G.6) → `os.replace` to final name. On any failure, temp file deleted; original untouched (test DX-ATOM).
- Modified parts in v1: `word/document.xml` only. (Footnotes/endnotes/headers are read-only.) `word/settings.xml` is not modified, including `w:trackRevisions`.

### G.2 Reader
- Parse with hardened parser (§H.3). Reject DOCTYPE.
- Styles: parse `styles.xml`; resolve `basedOn` chains (cycle-safe), `w:outlineLvl`, built-in heading/caption/TOC style ids (locale-independent via `w:styleId` and `w:name` both).
- Field-span pre-pass over the body: track `fldChar` begin/separate/end nesting across paragraphs; record for each paragraph the set of fields that intersect it and whether any begins/ends outside it.
- Atomisation per `w:p` (document order, including table cells, recursively for nested tables): TEXT atoms (from `w:t` respecting `xml:space`, `w:tab`, `w:br`, `w:cr`, `w:noBreakHyphen`, `w:softHyphen`), OPAQUE atoms (everything else inline, each with an XML path reference), FIXED atoms (TEXT inside bookmark/comment/hyperlink ranges).

### G.3 Element classification

| Structure | Class | Treatment |
|---|---|---|
| Body paragraph, plain runs | E | Editable |
| Mixed formatting (b/i/u, colour, highlight) | E | Editable; formatting mapped per §G.5; changes reported |
| Sub/superscript runs (`w:vertAlign`) | E with protected run | Run content protected (placeholder or verbatim Unicode check) |
| Character styles (`w:rStyle`), symbol fonts, `w:sym` | E with protected run | Protected |
| `w:lang` runs (e.g. Latin species names) | E with protected run | Protected |
| Inline OMML (`m:oMath` inside paragraph) | E | OPAQUE atom |
| Display equation paragraph (`m:oMathPara` only) | R | Read-only |
| Hyperlinks (`w:hyperlink`) | E (P region) | Atom; display text FIXED |
| Bookmarks (`w:bookmarkStart/End`) | E (P region) | Positions invariant; text between them FIXED if the bookmark is a cross-ref target (`_Ref*`) |
| Cross-reference fields (REF, PAGEREF, NOTEREF) | E | OPAQUE atom |
| Simple fields (`w:fldSimple`) | E | OPAQUE atom |
| Zotero (`ADDIN ZOTERO_ITEM`), Mendeley (`ADDIN CSL_CITATION`), EndNote (`ADDIN EN.CITE`) in-text | E | OPAQUE atom (begin..end incl. result runs and `w:fldData`) |
| Bibliography fields (`ZOTERO_BIBL`, `EN.REFLIST`), TOC, INDEX | R | Read-only, including all paragraphs spanned |
| Any multi-paragraph field | R | All spanned paragraphs read-only |
| Footnote/endnote references | E | OPAQUE atom |
| Footnote/endnote bodies | R | Not shown for editing in v1 (listed in import report) |
| Comments (ranges, references) | E (P region) | Range text FIXED; `comments.xml` untouched |
| Tracked changes (`w:ins`, `w:del`, `w:moveFrom/To`, `w:rPrChange`, `w:pPrChange`) | R | Paragraph read-only; import report recommends accepting/rejecting in Word |
| Tables (incl. merged, nested) | E for cell paragraphs meeting E rules | `w:tbl`, `w:tr`, `w:tc`, `w:tblPr`, `w:tcPr` untouched; text in cells with only numbers → R |
| Captions (Caption style or SEQ field) | R | Read-only |
| Headings | R by default | User may unlock to `proofread` only |
| Numbered/bulleted lists (`w:numPr`) | E | `w:pPr` byte-preserved |
| Section breaks (`w:sectPr` in `w:pPr` or body) | E/R unaffected | `w:pPr`/`w:sectPr` untouched |
| Images (`w:drawing`), embedded objects (`w:object`, OLE), `w:pict`, charts | E paragraph, OPAQUE atom | Atom; binary parts untouched |
| Text boxes (`w:txbxContent`), shapes with text | R | Read-only |
| Content controls (`w:sdt`) | R | Read-only |
| `mc:AlternateContent` | R | Read-only |
| Headers/footers | R | Parts untouched |
| `w:customXml` inline, smart tags, `w:permStart`, `w:altChunk` | R (altChunk: X) | — |
| Any element not on the tested allow-list | R | Automatic; listed in import report |
| Encrypted (OLE CFB container), `.docm`/`vbaProject.bin`, Strict OOXML namespace, malformed XML/ZIP, missing main part | X | Import refused with reason |

### G.4 Edit application rules
1. Edits change only TEXT atoms between consecutive OPAQUE/FIXED atoms; atom sequence invariant (BLOCK otherwise).
2. Paragraph `w:pPr` byte-identical; `w:rsidR*` attributes on `w:p` retained; run-level rsids may be dropped only on rewritten runs.
3. `w:proofErr` and `w:lastRenderedPageBreak` removed only inside rewritten spans.
4. Export verifies `source_hash` of the paragraph in the copy equals import hash; mismatch → skip, report.

### G.5 Formatting mapping and honest reporting
- Unchanged characters keep their original `rPr` exactly.
- Inserted characters inherit the `rPr` of the preceding unchanged character, except where that `rPr` contains local emphasis (`w:b`, `w:i`, `w:u`, `w:strike`, `w:caps`, `w:smallCaps`, `w:highlight`, `w:color`, `w:shd`); then inherit the paragraph's dominant run `rPr`.
- Every deleted or replaced span that carried formatting different from the paragraph's dominant `rPr` produces a `FormattingChange{paragraph, original_text, original_rpr_summary, new_text, applied_rpr_summary}` in the export report and as a WARN on the hunk **before** acceptance.
- Track-changes export (default ON): `w:ins`/`w:del` with `w:author="AcademicWrite"`, ISO date, ids allocated above the maximum `w:id` across all parts' revision, bookmark, comment and annotation ids; deletions use `w:delText`; OPAQUE atoms never wrapped in `w:del`.

### G.6 DOCX test suite
**Fixtures** (authored in Word 365 for Windows, plus LibreOffice-authored variants where noted), each with a README describing its structures. Minimum 30:
plain; Zotero numeric; Zotero author–year; Mendeley; EndNote; inline OMML; display OMML; footnotes; endnotes; hyperlinks; bookmarks + REF/PAGEREF cross-refs; SEQ captions; comments; tracked changes (ins/del/move/format); merged tables; nested tables; header/footer with fields; text boxes; section breaks (portrait/landscape); images inline/floating; embedded Excel object; numbered lists multi-level; mixed formatting; sub/superscripts + Greek + U+2212 + NBSP; species names in `w:lang`; content controls; multi-paragraph Zotero bibliography; TOC; LibreOffice-saved document; Google-Docs-exported document; document > 100 pages.

**Malformed/adversarial set (≥ 25):** truncated ZIP; CRC error; duplicate member names; overlapping-entry ZIP bomb; nested ZIP; high-ratio member; > 2000 members; path traversal names; absolute names; `.docm`; encrypted CFB; Strict OOXML; DOCTYPE/entity expansion; external entity; missing `document.xml`; missing rels target; invalid UTF-8; mismatched content types; unclosed field; `fldChar end` without begin; 10⁵ runs in one paragraph; deeply nested tables (depth > 20); 50 MB media; zero-byte file; renamed PDF.

**Automated assertions:**
| ID | Assertion |
|---|---|
| DX-IMM | `original.docx` SHA-256 unchanged after import, refine, export, failed export, restore |
| DX-ID | Zero-edit export: every ZIP member's uncompressed bytes identical; member set identical |
| DX-PARTS | One-paragraph edit: all members except `word/document.xml` identical bytes |
| DX-PARA | All non-edited body children C14N-identical (rsid/proofErr-normalised) |
| DX-ATOMS | Edited paragraphs: ordered list of C14N(OPAQUE) identical |
| DX-FIELD | Every field: begin/separate/end balanced; `instrText` and `w:fldData` identical; Zotero/EndNote JSON identical |
| DX-RELS | Every `r:id`/`r:embed`/`r:link` in modified parts resolves; no orphaned relationships created |
| DX-IDS | `w:id` uniqueness per id space after track-changes export |
| DX-CT | `[Content_Types].xml` covers every member |
| DX-WF | All XML parts well-formed; namespaces declared; `mc:Ignorable` prefixes declared |
| DX-ATOM | Export failure injected at each step → no file at final path; original intact |
| DX-ROUNDTRIP-TC | Track-changes export: programmatic "accept all" (our own XML transform, verified against LibreOffice when installed) yields candidate text |
| DX-ORACLE | python-docx opens every export; paragraph texts equal expected |
| DX-MAL | Malformed set: each rejected with specific code within 20 s, no crash, no temp residue |
| DX-FUZZ | Hypothesis-driven mutation of fixtures (≥ 10⁴ cases in nightly): no unhandled exception |
| DX-REG | Every bug found becomes a fixture in `tests/docx/regression/` with expected outcome |

**Manual checklist (per release, Word 365 Windows):** M1 open without repair prompt; M2 Zotero "Refresh" with no errors and unchanged citations; M3 EndNote "Update citations" unchanged; M4 tracked changes visible and accept-all reproduces candidate; M5 cross-refs update (F9) to same targets; M6 page count unchanged for proofread-only edits; M7 equation editing still works.

Preservation promise: only for structures in §G.3 with a passing DX test and M-checklist on the release. All else read-only or refused and reported.

---

## H. Security, privacy and offline requirements

### H.1 Threat model
In scope: malicious websites in the same browser (CSRF, DNS rebinding), malicious DOCX files, accidental exposure of Ollama or the app to the LAN, manuscript leakage via logs/backups/sync folders, outbound connections from the backend. Out of scope: malware running as the same Windows user (can read files directly), physical access, compromised Ollama binary, browser extensions with broad permissions (documented).

### H.2 Network surface
| Control | Requirement | Level target→current | Verification |
|---|---|---|---|
| Binding | uvicorn binds `127.0.0.1` only; startup asserts socket address; config cannot set other hosts | 0→2 | SEC-BIND |
| Host validation | Reject Host ∉ {`127.0.0.1:<port>`, `localhost:<port>`} with 421 (defeats DNS rebinding) | 0→2 | SEC-HOST |
| Session token | 256-bit random per process; obtained via `GET /api/v1/session` (requires valid Host and `Sec-Fetch-Site` same-origin/none); kept in JS memory; required as `X-AW-Token` on all API calls; compared constant-time | 0→2 | SEC-TOKEN |
| Origin check | For non-GET: `Origin` must equal own origin (absent Origin → reject) | 0→2 | SEC-ORIGIN |
| CORS | No CORS headers emitted, ever | 0→2 | SEC-CORS |
| GET safety | No state change on GET | 0→2 | API tests |
| CSP | `default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data: blob:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'` + `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store` on API | 0→2 | SEC-HDR |
| Rendering | TipTap schema-only rendering; no `dangerouslySetInnerHTML`; lint rule enforces | 0→2 | lint + SEC-XSS fixtures |
| Port | Probe 8765–8769; allow-list built from bound port | 0→2 | — |

### H.3 Upload and parser hardening
| Control | Requirement |
|---|---|
| Size | ≤ 50 MB upload (streamed to memory with cap) |
| Type | `PK\x03\x04` magic; `[Content_Types].xml` and main document part present with WordprocessingML main content type; `.docm` / macro content types rejected |
| ZIP limits | ≤ 2000 members; each uncompressed ≤ 100 MB (XML parts ≤ 50 MB); total ≤ 300 MB; ratio ≤ 100 for XML parts; overlapping local headers detected (offset/size consistency); duplicate names rejected; decompression streamed with running cap (headers not trusted) |
| Names | Reject `..`, leading `/` or `\`, drive letters, NUL, > 255 chars; members never extracted to disk |
| XML | `lxml.etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False, dtd_validation=False, huge_tree=False, remove_blank_text=False)`; reject any part containing `<!DOCTYPE`; depth limit 256 |
| Time | Import aborted after 20 s CPU time (worker thread with cancel check between parts) |
| Embedded binaries | Never parsed or executed; copied byte-for-byte |

All level target 0 → current 2, verified by DX-MAL and SEC-ZIP tests. Robustness against unknown parser bugs in lxml/libxml2 is **not** guaranteed by design; it requires fuzzing (DX-FUZZ) and dependency updates.

### H.4 Egress and offline
- Backend egress guard: custom `httpx` transport that only allows `127.0.0.1:11434`, plus a process-wide `socket` audit hook (`sys.addaudithook` on `socket.connect`) that raises on any other destination. Level 0→2 (SEC-EGRESS). Covers the Python process only.
- Frontend: no external URLs in `dist/` (build check), CSP `connect-src 'self'`.
- Ollama: `start.ps1` and `/health` check `OLLAMA_HOST` env var and probe `<LAN-IP>:11434`; if reachable, red banner. Ollama's own update checks and model registry access are outside the application's control; the install guide documents disabling auto-update and that `ollama pull` is the only intended online action. Level 2.
- Offline acceptance: OFF-1 (all adapters disabled, full E2E), OFF-2 (Windows Firewall outbound block rule on venv `python.exe` produces zero blocked-connection events during E2E — evidence that no attempts are made).

### H.5 Data at rest, deletion, backup
- Data dir: `%LOCALAPPDATA%\AcademicWrite\projects\<uuid>\{original.docx, project.sqlite, exports\}`. Each project isolated in its own directory and database; no cross-project queries.
- Synced folders: refuse data dir under OneDrive/Dropbox/Google Drive roots unless the user explicitly overrides (manuscript would leave the machine).
- Deletion: project = remove directory after closing DB handles (retry on Windows file-lock, max 5 s), then confirmation. History purge = `DELETE` + `VACUUM` + `PRAGMA wal_checkpoint(TRUNCATE)`. **Physical erasure is not claimed**: SSD wear-levelling, Volume Shadow Copies, Windows Search index and backups may retain data. Recommendation: BitLocker. Level: logical deletion 0→2.
- Backup: zip of selected project dirs (SQLite via online backup API to a consistent copy), `manifest.json` with schema version and SHA-256 per file. Backup files are as sensitive as manuscripts; the UI says so. No encryption in v1 (stated limitation).
- Restore: backup passes the same ZIP limits; manifest hashes verified; schema migrations applied forward only; restored as new project ids.

### H.6 Temporary files
- All temp files under `<data_dir>\tmp\` (not `%TEMP%`), created with `tempfile.mkstemp(dir=...)`; deleted in `finally`; startup sweep deletes all `tmp\*` older than process start. No manuscript text in temp files except export staging.

### H.7 Logs
- Rotating file log in `<data_dir>\logs\` (5 × 5 MB). Records contain: event, ids, hashes, durations, error codes, model name/digest, sizes. **Never** paragraph text, prompts, outputs, filenames of manuscripts (hashed).
- Redaction filter: drops any string field > 120 chars or with ≥ 8 whitespace-separated tokens; unit-tested with manuscript-like strings (SEC-LOG).
- Debug prompt logging: off; enabling requires settings toggle with warning; writes to `logs\debug-<session>.log`; disabled and file deleted at shutdown.

### H.8 Shutdown
- Ctrl+C / window close of `start.ps1` console: stop accepting requests, cancel running job (closing Ollama stream), checkpoint SQLite WAL, delete temp files, delete debug log. Abrupt termination: next startup performs sweep and marks jobs interrupted. SQLite in WAL mode with `synchronous=FULL` for operation commits.

### H.9 Guaranteed vs pen-test-required
- By design + automated tests (target 0): loopback bind, Host allow-list, token, Origin, no CORS, CSP headers, ZIP/XML limits, egress guard for the Python process, log redaction, original immutability.
- Requires penetration/fuzz testing (target 1): parser robustness against crafted files, DNS-rebinding via real browsers (Chrome, Edge, Firefox), CSRF via real browsers, behaviour with browser extensions, Ollama exposure detection on real networks.

---

## I. Model benchmarking and hardware requirements

### I.1 Candidates (tag status as of 2026-11-03)
Status meanings: **Confirmed (listing)** = tag page found on ollama.com via search results; not fetched live from this environment (network policy blocked direct access). **Must be re-confirmed** at install by `ollama pull` + `ollama show --modelfile` and digest recording. No candidate is assumed to be non-thinking or instruction-tuned from its name; P-think and template inspection decide.

| ID | Tag | Status | Notes (from listings; to be confirmed by `ollama show`) |
|---|---|---|---|
| M1 | `qwen3:4b-instruct-2507-q4_K_M` | Confirmed (listing) | ~2.5 GB, Q4_K_M; listed context 256K; marketed non-thinking |
| M2 | `qwen3:4b-instruct-2507-q8_0` | Confirmed (listing) | ~4.3 GB, Q8_0; quantization control for M1 |
| M3 | `qwen3:8b` | Confirmed (listing) | ~5.2 GB; hybrid thinking; requires `think:false` and P-think |
| M4 | `qwen3.5:4b-q4_K_M` | Confirmed (listing) | ~3.3 GB; thinking-capable; vision-capable (multimodal weights); no official instruct/non-thinking tag found |
| M5 | `qwen3.5:9b-q4_K_M` | Confirmed (listing) | ~6.6 GB; thinking-capable; vision; third-party non-thinking repacks (e.g. `frob/qwen3.5-instruct`) **excluded** (unofficial provenance) |
| M6 | `gemma3:12b-it-qat` | Confirmed (listing) | ~8.9 GB; instruction-tuned; vision-capable |
| M7 | `granite4:micro` (≡ `granite4:3b`) | Confirmed (listing) | ~2.1 GB dense 3B; listed context 128K |
| M8 | `granite4:tiny-h` | Confirmed (listing) | ~4.2 GB; hybrid Mamba-2, 7B total / ~1B active; listed 1M context |
| — | `qwen3:8b-instruct-2507` | **Not found** | Does not exist as far as listings show; v0.1 assumption withdrawn |
| Ref (optional) | `qwen3.5:27b`, `gemma3:27b` | Unverified quant tags | Ceiling reference only if ≥ 24 GB VRAM; never selected for v1 |

### I.2 Recorded identity per run
`ollama --version`; tag; full digest from `ollama show`; modelfile (template, parameters, system); quantization; parameter count; context length used (`num_ctx`) and model max; whether template supports `think`; OS build; CPU model, cores, AVX2/AVX-512; RAM; GPU model, VRAM, driver; power plan; other running apps (Word closed/open noted).

### I.3 Pre-checks (automatic disqualification for production use)
| ID | Check | Pass |
|---|---|---|
| P-think | 30 probe calls with `think:false` (if supported) | 0 outputs with reasoning text, `<think>` fragments or meta-commentary after postprocess |
| P-tok | 30 masked passages | ≥ 95 % first-attempt placeholder validity; chosen delimiter recorded |
| P-fmt | `<out>` contract | ≥ 98 % compliance |
| P-cancel | Client disconnect stops generation | `ollama ps` shows generation stopped within 5 s |
| P-ctx | 500-word passage + context + prompt fits `num_ctx` without truncation | no truncation |

### I.4 Benchmark design
- Inputs: §J.1 corpus, **dev split for prompt development, test split for selection**. Length strata: 150 ± 20, 300 ± 30, 500 ± 50 words (≥ 12 passages per stratum in test).
- Modes: `proofread`, `light`, `moderate` on all; `advanced` on eligible sections; `feedback` on 20 Discussion/Introduction passages; expression scope on 30 expressions.
- Identical system/mode/section prompts for all models; Ollama applies the model template. A per-model "tuned" variant is allowed only on dev, reported separately, and may be adopted only if it improves gates on test.
- Options per mode fixed: proofread T = 0.1, others T = 0.3, `top_p` 0.9, `seed` ∈ {11, 23, 37} (3 runs), `num_ctx` 8192, `num_predict` = 2 × input tokens + 64, `keep_alive` 0 between models, one excluded warm-up.
- Protection: standard and conservative.
- Metrics — deterministic: P-num (zero L1-Q violations), P-cite, P-term, P-rel (human-adjudicated: §J.3), placeholder failure rate, retry rate, failed rate, length-band compliance, UNVERIFIED rate, latency (TTFT, total, decode tokens/s, prompt eval tokens/s from Ollama response fields), peak RAM (`psutil` on `ollama*.exe` processes, 4 Hz), VRAM (`nvidia-smi` 4 Hz; "not measured" on non-NVIDIA), `ollama ps` CPU/GPU split.
- Metrics — subjective: §I.5.
- Variance: report median and IQR across seeds; a model's gate is evaluated on the worst seed.

### I.5 Human rating
- Finalists: at most 4 models passing automatic gates.
- 48 items (stratified: 16 per length; ≥ 8 per section type), same items for all finalists; original shown; model identity hidden; order randomised per rater.
- 2 raters minimum (author + ≥ 1 independent domain researcher). 48 × 4 × 2 = 384 judgements (~6–8 h per rater).
- Dimensions (1–5 anchored scales defined in `bench/rating/guidelines.md`): Meaning preservation, Technical precision, Grammar, Naturalness (competent disciplinary prose, not "less AI-like"), plus binary Accept-as-is and binary "introduced a scientific change".
- Agreement: quadratic-weighted κ per dimension; κ < 0.4 → dimension reported, not used for selection.

### I.6 Hardware profiles
| Profile | Spec | Purpose |
|---|---|---|
| H-min | Windows 11, 4-core AVX2 CPU, 16 GB RAM, no GPU, SSD | Minimum supported; expected to run ≤ 4B models only (level 2) |
| H-ref | 8-core CPU, 32 GB RAM, NVIDIA GPU 8 GB VRAM | Reference for selection |
| H-user | The researcher's actual machine | Final acceptance |
The benchmark MUST be run on H-user; H-min results determine whether the app documents a model as supported on minimum hardware.

### I.7 Selection rule
1. Eliminate on pre-checks (§I.3).
2. Hard integrity gates on test split, standard protection, worst seed: P-num ≥ 99.5 %, P-cite ≥ 99.5 %, P-term ≥ 99 %, human-adjudicated relationship preservation ≥ 97 % with lower 95 % Wilson bound ≥ 94 %, "introduced a scientific change" rate ≤ 3 %, failed rate ≤ 3 %.
3. Models failing (2) may be approved for `proofread` and `light` only if those modes alone pass (2).
4. Among models passing for unrestricted (`moderate`/`advanced`) use: rank by Meaning preservation, then Naturalness, then Accept-as-is. Fluency never outranks meaning preservation.
5. Latency constraint on H-user (300-word, moderate): median total ≤ 90 s, p95 ≤ 180 s. Failing models remain selectable as "slow quality mode" with explicit UI estimate.
6. Memory constraint: with Word open, ≥ 3 GB system RAM free during generation.
7. Re-benchmark mandatory when Ollama version, model digest, or prompts change (prompt hash), at least for pre-checks and deterministic gates.

---

## J. Evaluation corpus, testing, acceptance criteria, roadmap

### J.1 Corpus
| Split | Size | Authors | Use |
|---|---|---|---|
| Dev | 60 passages | ≤ 50 % developer/author; rest from open-licensed (CC-BY) papers with attribution | Rule development, prompt development, threshold calibration |
| Test (sealed) | 60 passages | ≥ 70 % not written by the developer: independent researchers (with permission) and CC-BY papers from journals/authors **not** used in dev | Final evaluation only |
| Held-out style | 15 passages | Non-native English authors, older papers, different disciplines (civil, biomedical materials, polymer chemistry) | Generalisation report; not gating |

Stratification per split (minimums): sections (Intro 8, Lit review 8, Methods 10, Results 12, Discussion 12, Conclusions 6, other 4); domains (natural-fibre composites 15, textile/3D woven 10, polymer/bio-matrix 10, mechanical testing 12, experimental methods 8, modelling 5); features: citation-dense (≥ 5 citations) 12; table/figure references with values 10; sentences > 40 words in ≥ 15 passages; numerical comparisons between ≥ 2 groups 20; statistical reporting (p, CI, SD, n) 12; negative or inconclusive results 8; hedged mechanism claims 10; OMML/inline math 6; defined acronyms 10; deliberately flawed language 8.

**Leakage prevention**
- Test split stored in an encrypted zip (password held by the second rater) until rules/prompts are frozen (git tag `freeze-vX`); decryption logged in `bench/results/`.
- No passage, paraphrase, or perturbation from the test split may be viewed by the rule developer before freeze; rule/prompt changes after a test run require a new test split for the next claim (or reporting as "post-hoc").
- Passages from the same paper never cross splits (split by source document).
- Near-duplicate check (shingled Jaccard > 0.3) between splits.

**Annotations**
- Gold per passage: protected spans, claim graph (§E.3 schema), qualifiers, hedge levels, citation anchors, section type.
- Two independent annotators on 100 % of test and ≥ 30 % of dev; adjudication; agreement reported (span F1, slot-level κ).

**Perturbations (verifier recall)**
- Operators frozen before test generation, one per failure case A–M plus number/unit/citation/acronym edits; each operator produces a minimal, fluent corruption (hand-checked). Target: ≥ 25 instances per operator per split (≥ 400 per split).
- Negative controls (verifier false-alarm): meaning-preserving paraphrases written by humans (≥ 150 per split, ≥ 50 % by people other than the rule developer) plus model outputs adjudicated as meaning-preserving.

### J.2 Test strategy (deterministic, CI)
Unit (detectors, canonicalisation, masking, L1, L2 patterns), DOCX (§G.6), security (§H), API contract with mock Ollama (timeouts, 404, OOM text, malformed NDJSON, think leakage, truncation, disconnect), E2E (Playwright: import → sentence refine → accept 1 of 3 hunks → undo → redo → restore rev → export with track changes → reopen), offline (OFF-1, OFF-2), migration tests (schema vN→vN+1), Windows CI runner (paths, file locks).

### J.3 Acceptance criteria (targets; none achieved)

| Area | Metric | Type | Target |
|---|---|---|---|
| Critical relationship preservation (model, applied text) | Applied changes (after user acceptance flow, simulated as accept-all-non-BLOCK) with adjudicated scientific change | Human-adjudicated, deterministic count | 0 BLOCK-class errors reach applied text in test E2E; adjudicated scientific-change rate ≤ 1 % with upper 95 % bound ≤ 3 % |
| Verifier recall (false negatives) | Detected perturbations / total, per operator, test split | Deterministic | A, B, D, E, G, I, K: recall ≥ 0.95 (lower Wilson bound ≥ 0.90); C, F, H, J: ≥ 0.85 (≥ 0.78); L, M: UNVERIFIED or BLOCK ≥ 0.95 (never NO_ISSUES_DETECTED on > 5 %) |
| Verifier false positives | BLOCK on human meaning-preserving paraphrases | Deterministic | ≤ 10 % BLOCK, ≤ 25 % WARN+BLOCK; UNVERIFIED reported separately |
| Numbers & units | L1-Q violations in raw output (model) / undetected numeric changes reaching applied text (system) | Deterministic | ≥ 99.5 % clean raw; 0 applied |
| Citations | Citation atom/anchor violations | Deterministic | ≥ 99.5 % clean raw; 0 applied |
| Terminology | L1-T violations | Deterministic | ≥ 99 % clean raw |
| L2 coverage | Quantity-bearing sentences fully bound | Deterministic | Reported; ≥ 70 % for unrestricted modes in Results/Discussion, else those modes restricted |
| Meaning preservation (human) | Mean, 1–5 | Subjective | ≥ 4.3; no item ≤ 2 without a BLOCK/UNVERIFIED flag |
| Grammar | LanguageTool offline errors/100 words (proxy) + human grammar score | Proxy + subjective | Output ≤ original errors on ≥ 90 % passages; human ≥ 4.3 |
| Natural academic writing | Human naturalness, 1–5 | Subjective | ≥ 3.8 and ≥ original on flawed subset |
| Stylistic homogenisation | Std. dev. of sentence length across a 10-paragraph document, output/original ratio | Deterministic descriptive | ≥ 0.8 (not collapsing variety) |
| Processing time (H-user) | 150/300/500-word moderate: median total | Measured | ≤ 45 / 90 / 150 s; p95 ≤ 2× median |
| DOCX safety | DX suite + M-checklist | Deterministic + manual | 100 % |
| Security | SEC suite + browser pen-test checklist | Deterministic + manual | 100 % |

All proportions reported with Wilson 95 % CIs and sample sizes.

### J.4 Roadmap
| Phase | Deliverables | Exit (evidence) |
|---|---|---|
| P0 Spec & data | Annotation guidelines, dev corpus + gold, test corpus sealed, perturbation operators, DOCX fixtures + malformed set | Annotator agreement report; fixture README; freeze of operators |
| P1 Skeleton & security | FastAPI app, session/Host/Origin/token, egress guard, CSP, intake guard, logging, store, migrations | SEC suite green on Windows CI |
| P2 DOCX core | Reader, styles, field-span pass, classifier, writer, xmlcheck; identity & one-paragraph edits (programmatic, no model) | DX suite green (except TC) |
| P3 Detection & L1 | Detectors, canonicalisation, masking/realign, L1 | Unit suites green; dev perturbation recall for L1 cases |
| P4 L2 | Lexicons, clause split, patterns, binder, graph, rules R1–R18, alignment | Dev recall/FP measured; rules frozen; then sealed test evaluation |
| P5 Model bench | Ollama client, prompts, refine pipeline (headless), benchmark harness, pre-checks, human rating | Selection report per §I.7 |
| P6 Change workflow | ChangeSets, hunks, partial-apply verification, operations/undo/redo, revisions/restore | API + unit green |
| P7 Frontend | Document/Review/Compare/History views, integrity panel, job bar, model status | E2E green |
| P8 Export & data ops | Track-changes export, export preview, backup/restore, deletion, uninstall | DX-ROUNDTRIP-TC, M-checklist, backup tests |
| P9 Optional | L3 advisory, feedback-mode tuning, footnote-body editing | Level-3 features behind flags |

Critical path: P0 → P2 → P4. **If P4 sealed-test targets are not met, `moderate`/`advanced` are disabled for Methods/Results/Discussion in v1** (proofread/light/feedback only).

---

## K. Unresolved risks and explicit limitations

### K.1 Risks
| # | Risk | Severity | Mitigation / status |
|---|---|---|---|
| K1 | Rule-based L2 cannot represent all scientific language; nested comparisons, implicit causality (participial clauses), cross-sentence anaphora, table-only values | Critical (inherent) | UNVERIFIED status; mode restrictions; human review is mandatory |
| K2 | Corpus may still reflect a narrow writing population | Major | ≥ 70 % independent test authors; held-out style report |
| K3 | Annotation subjectivity in claim graphs | Major | Double annotation, adjudication, agreement reported |
| K4 | Formatting of rewritten words can be lost (italic species names, local emphasis) | Major | Protected `w:lang`/`rStyle` runs; per-change formatting report before acceptance |
| K5 | Word behaviour not automatable; LibreOffice differs | Major | Mandatory M-checklist per release |
| K6 | Ollama versions change determinism, `think` handling, cancellation | Major | Version pinning, pre-checks, re-benchmark rule |
| K7 | CPU-only hardware may make every model that passes integrity gates too slow | Major | Slow-mode labelling; restricted modes; documented hardware profiles |
| K8 | lxml/libxml2 parser vulnerabilities | Moderate | Hardened config, fuzzing, dependency updates |
| K9 | Ollama itself may make outbound connections (update checks) | Moderate | Documented; firewall rule recommendation; outside app guarantees |
| K10 | Human rating burden | Moderate | Reduced design (384 judgements) |
| K11 | Tag/digest drift and model removal upstream | Moderate | Local digest pinning; keep model files; documented |
| K12 | Users may override WARNs habitually ("alarm fatigue") | Moderate | FP targets; WARN grouping; override logging; no override for core BLOCKs |

### K.2 Limitations (stated in the application's About/Help)
- The application does not verify scientific correctness, plausibility, or references (V-3, V-4).
- "No issues detected" means only that L1/L2 checks did not fire within their coverage.
- Preservation is promised only for DOCX structures listed in §G.3 with passing tests.
- Deletion is logical, not physical.
- Backups are unencrypted.
- English only.
- No AI-detection or detector-evasion functionality.

### K.3 Feature classification (target → current)

| Feature | Target | Current |
|---|---|---|
| Original DOCX immutable; failed export never affects original | 0 | 2 |
| Loopback binding, Host allow-list, token, Origin, no CORS, CSP | 0 | 2 |
| Python-process egress restricted to Ollama loopback | 0 | 2 |
| ZIP/XML intake limits | 0 | 2 |
| Log redaction | 0 | 2 |
| No change applied without user action; core BLOCKs non-overridable | 0 | 2 |
| Undo/redo/restore/revision history | 0 (functional) | 2 |
| L1 detection of changed digit sequences (catch-all) | 0 | 2 |
| L1 detection of detected quantities/citations/terms | 0 | 2 |
| L1 detector recall on unusual formats | 1 | 2 |
| L2 rules R1–R18 on in-pattern sentences | 1 | 2 |
| L2 coverage on real text | 1 | 3 |
| DOCX preservation for §G.3 E/P structures | 1 | 2 |
| Zotero/EndNote refresh after export | 1 (manual) | 2 |
| Track-changes export accepted by Word | 1 (manual) | 2 |
| Formatting retention of rewritten words | 2 | 3 |
| Language-quality improvement by selected model | 1 | 3 |
| Model selection meets integrity gates | 1 | 3 |
| Feedback (analytical) mode usefulness | 2 | 3 |
| Section auto-classification | 1 | 2 |
| L3 advisory | 3 | 3 |
| Ollama not LAN-exposed (detection) | 1 | 2 |
| Physical erasure | not claimed | — |

---

## L. Pre-implementation approval checklist

A gate passes only on evidence, not prose. "Specification-complete" (S) and "evidence-complete" (E) are tracked separately. Coding of the components that *produce* a gate's evidence is permitted before the gate passes; enabling the guarded functionality for real manuscripts is not.

### Gate 1 — Scientific integrity
- **Required evidence:** (S) §E schema, rules R1–R18, failure-case table, statuses — present in this document. (E) Annotation guidelines; dev corpus with double-annotated gold; frozen perturbation operators; sealed test split; L2 implementation evaluated on sealed test with recall/FP per operator and CIs.
- **Pass criteria:** §J.3 verifier recall and FP targets met on sealed test; coverage reported; no failure case A–K with recall below target.
- **Failure conditions:** any of A, B, D, E, G, I, K below target; FP BLOCK > 10 %; leakage detected.
- **Coding if failed:** Yes for infrastructure and L1/L2 development; **No** for enabling `moderate`/`advanced` on Methods/Results/Discussion.
- **Status:** S = complete; E = not started → **not passed**.

### Gate 2 — DOCX safety
- **Required evidence:** (S) §G classification, edit rules, test list — present. (E) ≥ 30 fixtures + ≥ 25 malformed files committed; DX suite green on Windows; M-checklist completed on Word 365.
- **Pass criteria:** 100 % DX automated; M1–M7 pass on all fixtures with E-class content.
- **Failure conditions:** any DX-IMM/DX-ID/DX-PARTS/DX-FIELD/DX-RELS failure; any M1 repair prompt.
- **Coding if failed:** Yes (reader/writer development); export of model-edited real manuscripts **not** enabled.
- **Status:** S = complete; E = not started → **not passed**.

### Gate 3 — Privacy and security
- **Required evidence:** (S) §H — present. (E) SEC suite green; OFF-1/OFF-2 pass; browser pen-test checklist (Chrome, Edge, Firefox: DNS rebinding, CSRF form/fetch, cross-origin SSE) executed and recorded.
- **Pass criteria:** 100 % SEC + OFF; pen-test checklist all pass.
- **Failure conditions:** any egress, any accepted foreign Host/Origin, any manuscript text in logs.
- **Coding if failed:** Yes; use with real manuscripts **not** permitted.
- **Status:** S = complete; E = not started → **not passed**.

### Gate 4 — Model feasibility
- **Required evidence:** (S) §I — present; hardware profiles defined. (E) H-user hardware record; pre-checks run; benchmark results on test split; human rating with κ; selection report.
- **Pass criteria:** ≥ 1 model passes §I.7 step 2 for at least `proofread`/`light`; latency and memory constraints met on H-user for that model.
- **Failure conditions:** no model passes integrity gates in any mode; or all passing models violate memory constraint on H-user.
- **Coding if failed:** Yes for non-model components; if no model passes for any mode, the product reduces to DOCX + verification tooling and the project must be re-scoped.
- **Status:** S = complete; E = not started; tag confirmation pending live `ollama show` → **not passed**.

### Gate 5 — User workflow
- **Required evidence:** (S) §D API, data model, operation semantics, §F modes/scopes, UI views (§M below) — present. (E) Clickable prototype or E2E-tested implementation; usability walkthrough by the researcher on 3 real manuscripts (copies) covering paragraph/sentence/expression refine, partial hunk accept, undo/redo, restore, cancel, model-missing error, export.
- **Pass criteria:** E2E green; walkthrough completes with no data loss and no change applied without explicit action.
- **Failure conditions:** any path that applies text without user confirmation; undo/redo inconsistency; lost revisions after crash test.
- **Coding if failed:** Yes (the workflow must be built to be tested).
- **Status:** S = complete; E = not started → **not passed**.

---

## M. User interface (normative summary)

- **DocumentView:** paragraphs rendered read-only by default with edit class badges (E/P/R); selection → scope (paragraph / sentence(s) / expression); action bar: mode, protection level, concise, candidates; "Feedback" button.
- **ReviewView / HunkCard:** side-by-side and inline diff; each hunk with accept/reject; findings attached to hunks with severity colour and plain-language message ("Value 23.3 % now attached to configuration A instead of D"); BLOCKed hunks cannot be accepted (core) or require reason (overridable); live re-verification of the selected hunk set; ClaimTable showing original vs candidate claims for the paragraph.
- **CompareView:** any two revisions of a paragraph or the whole document (original vs current).
- **HistoryView:** per-paragraph revisions with origin, model, prompt hash; restore; document operation log with undo/redo.
- **JobBar:** queue, progress, streaming preview (read-only, clearly labelled "unverified draft"), elapsed time, estimated time from model profile, Cancel.
- **ModelStatus:** Ollama reachability, model state, digest match, LAN exposure warning, approved modes.
- **ErrorBanner:** every API error code mapped to a message with a concrete action.
- **Editing:** manual edits in an edit buffer per paragraph; ProtectedSpan atoms cannot be deleted by keystroke (explicit "unprotect" action creates an Operation); commit → verification → Operation.
- **Never:** auto-apply, auto-export, overwrite the uploaded file, apply streaming preview text.

---

## Decision

**READY FOR LIMITED PROTOTYPE ONLY.**

Justification by gate:
- **Gate 1 (Scientific integrity):** specification complete; evidence absent (no corpus, no gold, no sealed test, no measured recall). Coding the L1/L2 verifier and corpus tooling is permitted and is the only way to generate evidence; rewriting modes beyond `proofread`/`light` must not be used on real manuscripts.
- **Gate 2 (DOCX safety):** specification complete; no fixtures or test results. Reader/writer may be built and tested on fixtures and copies; no exports from real manuscripts until DX + M-checklist pass.
- **Gate 3 (Privacy/security):** specification complete; tests not run. Prototype must run only on non-sensitive or copied documents until SEC/OFF/pen-test evidence exists.
- **Gate 4 (Model feasibility):** candidate tags confirmed only from listings, not live; no benchmark run; user hardware unrecorded. Unknown whether any local model passes integrity gates.
- **Gate 5 (User workflow):** specified; not demonstrated.

No gate has evidence; therefore the specification does not qualify as READY FOR IMPLEMENTATION. It is detailed enough to build the evidence-producing components (phases P0–P5) without major design guesses, so it is not NOT READY. The limited prototype is defined as: phases P0–P5 plus a headless CLI that runs refine + verify on corpus passages and DOCX copies, with no production use on real manuscripts.

---

## Change log v0.2 → v0.3

| Area | Change | Reason |
|---|---|---|
| Evidence | Levels redefined (0–3), "target → current"; all v0.2 "[T]" claims downgraded | v0.2 claimed testing that never occurred (C-01) |
| Scope | Explicit V-1…V-4 verification levels; non-goals incl. AI-detection | Distinguish textual, relational, plausibility, factual verification |
| L1 | Added digit-run catch-all, canonicalisation table, output language/truncation checks | Detector false negatives (C-05), Mj-13 |
| L2 | Paragraph claim graph; extended schema (uncertainty, baseline, qualifiers, edges); explicit inheritance; value-anchored comparison; rules R10–R18; failure-case matrix A–M; non-overridable BLOCK list | C-02, C-03, C-04, C-10 |
| Writing engine | Modes = proofread/light/moderate/advanced/feedback; scope separated; analytical mode no longer rewrites; section rules with mode restrictions; diagnostics descriptive only | C-09, Mj-05 |
| Protection | Hint vocabulary, composite-citation mapping, density limits tied to modes, OPAQUE order invariance | Mj-14, C-06 |
| DOCX | Multi-paragraph field detection; full element classification table incl. captions, text boxes, lists, sections, images, OLE, `w:lang`, `w:rStyle`; XSD replaced by structural validator; ≥ 30 fixtures + ≥ 25 malformed + fuzz + regression; manual checklist; formatting-change report before acceptance; atomic export | C-06, C-07, Mj-07–09, Mj-16, Mo-09 |
| Security | Single token mechanism via same-origin bootstrap; Sec-Fetch checks; audit-hook egress guard; synced-folder refusal; temp-file and shutdown policy; deletion stated as logical only; guaranteed vs pen-test split | Mj-10, Mj-11, Mj-18 |
| Models | Candidate list corrected (qwen3.5 tags, granite4 micro and tiny-h characterisation, no qwen3 8B instruct-2507); pre-checks incl. P-think, P-cancel; 150/300/500-word strata; hardware profiles; selection with Wilson bounds; restricted approval path | Mj-01–04, Mj-15 |
| Corpus | Dev/test/held-out splits; ≥ 70 % independent test authors; sealed test; split by source paper; perturbation operators per failure case; human paraphrase negatives | C-08 |
| API/data | Revision/Operation model, base_rev conflicts, idempotency, apply-with-reverification, feedback endpoint, export preview, persisted jobs, SSE replay | Mj-06, Mj-12, C-10 |
| Dependencies | Removed defusedxml, python-docx (runtime), spaCy; fixed lockfile choice; pysbd mandatory | Mo-01, Mo-02, Mi-01 |
| Gates | Five gates with evidence, pass/fail, coding-permission rules; final decision | Requested |
