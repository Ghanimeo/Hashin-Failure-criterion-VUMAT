# AcademicWrite — Technical Specification v0.2

Status: pre-implementation. Supersedes v0.1. No code until sign-off.

Claim levels used throughout:

- **[G] Guaranteed** — enforced by construction (code path cannot do otherwise) and covered by a test that fails the build.
- **[T] Tested** — behaviour verified on the fixture/benchmark corpus; may fail on inputs outside it.
- **[E] Expected** — design intent with partial evidence; measured, not enforced.
- **[X] Experimental** — off by default or advisory only; no correctness claim.

---

## 0. Self-critique of v0.1

| # | v0.1 defect | Consequence | v0.2 fix |
|---|---|---|---|
| D1 | Model chosen a priori (4B) | Selection biased toward speed | §H benchmark gates selection |
| D2 | Integrity = token multisets | Swapped associations pass (D↔A example) | §E relation layer (claim tuples) |
| D3 | Patch-in-place described, not specified | Rewritten runs could orphan `w:fldChar`, `w:bookmarkStart`, `w:commentRangeStart`, `w:proofErr`, `w:rsid*` | §F lxml run-tree editor with edit-safety classes and XML-diff tests |
| D4 | Opaque `⟦N1⟧` placeholders | Breaks agreement ("⟦N1⟧ were…"), article choice, model deletes/duplicates them, poor fluency in citation-dense text | §D typed, semantically-hinted placeholders + numbers kept visible in standard mode + positional constraints |
| D5 | Passive voice, nominalization, long sentences scored as defects | Damages Methods sections; pushes non-disciplinary style | §D section- and convention-aware diagnostics; no global "reduce" targets |
| D6 | "Humanization" framing | Optimises surface variation, not clarity | Renamed **refinement**; no detector-evasion objective |
| D7 | Security = "binds to 127.0.0.1" | DNS rebinding, CSRF from any open browser tab, Ollama on 0.0.0.0 | §G Host/Origin allow-list, per-launch token, Ollama exposure check |
| D8 | ZIP limits only on file size | ZIP bomb / XXE / path traversal | §G hardened OOXML intake |
| D9 | `.docx` export claimed to preserve "fields, equations, footnotes" | Untested promise | Every preservation claim tied to a named test (§I) |
| D10 | V9 semantic LLM check counted as verification | 4B judge unreliable | LLM checks strictly [X] advisory, never PASS-granting |
| D11 | Single edit per paragraph | No sentence/expression granularity, no per-hunk accept | §C/§6 change-set model with hunks |
| D12 | No backup/delete semantics | Data loss or residual sensitive data | §G secure delete, export/restore |
| D13 | `seed`+`temperature 0.3` assumed reproducible | Ollama output differs across versions/GPU/CPU | Benchmark pins Ollama version, model digest, records hardware |

---

## A. Revised architecture

```
┌────────────────────────── Windows host ───────────────────────────┐
│ Browser tab  http://127.0.0.1:8765/?t=<launch-token>               │
│  React/TipTap SPA (static, no external origins; strict CSP)        │
│        │ fetch + X-AW-Token header          ▲ SSE                   │
│        ▼                                    │                       │
│ FastAPI (uvicorn, 127.0.0.1:8765, 1 worker)                        │
│  ├ security middleware: Host allow-list, Origin check, token, CSP  │
│  ├ intake: ooxml_guard (zip/xml hardening)                          │
│  ├ docx: package model (lxml)  ── python-docx only for style lookup │
│  ├ segment: paragraph → sentences → editable spans                  │
│  ├ protect: detectors → protection plan (mode-dependent)            │
│  ├ refine: prompt builder → ollama_client → postprocess → realign   │
│  ├ verify: L1 token, L2 relation (claim tuples), L3 LLM advisory    │
│  ├ changes: change-sets, hunks, history (SQLite WAL)                │
│  ├ store: project dir, atomic writes, backup/restore, secure delete │
│  └ ollama_client ── loopback only ──► Ollama 127.0.0.1:11434        │
└────────────────────────────────────────────────────────────────────┘
```

Invariants:
- [G] Backend opens no socket except listening on 127.0.0.1:8765 and connecting to 127.0.0.1:11434 (enforced in `net_guard`, test `test_no_egress`).
- [G] Original DOCX bytes never modified; exports are new files.
- [G] No model output reaches the document without explicit user acceptance of each hunk.
- [G] An edit with any L1/L2 BLOCK cannot be accepted without a typed override reason stored in history.

Single worker, single generation queue (concurrency 1). Optional benchmark harness is a separate CLI sharing `services/`.

Runtime dependencies (backend): `fastapi`, `uvicorn`, `httpx`, `lxml`, `python-docx` (style resolution, optional), `pydantic`, `pydantic-settings`, `defusedxml` (pre-parse guard), `regex`. Optional: `pysbd` (sentence boundary; pure Python, offline). Dropped from v0.1: spaCy (download + size + negligible gain over rules for this task). Frontend: `react`, `typescript`, `vite`, `tailwindcss`, `@tiptap/react` + starter-kit, `zustand`, `diff-match-patch`. Nothing else.

---

## B. Revised folder structure

```
academicwrite/
├─ backend/
│  ├─ pyproject.toml  uv.lock (or requirements.lock with hashes)
│  └─ app/
│     ├─ main.py                      # app factory; docs_url=None, openapi_url=None in prod
│     ├─ config.py                    # Settings, paths under %LOCALAPPDATA%\AcademicWrite
│     ├─ security/
│     │  ├─ middleware.py             # Host, Origin, token, CSP, no-cache
│     │  ├─ net_guard.py              # socket.create_connection / httpx transport allow-list
│     │  └─ launch_token.py
│     ├─ api/  health.py models.py projects.py paragraphs.py refine.py
│     │        changes.py verify.py history.py export.py glossary.py
│     │        settings.py backup.py jobs.py
│     ├─ domain/  document.py span.py protection.py claim.py change.py report.py
│     ├─ services/
│     │  ├─ ollama_client.py
│     │  ├─ intake/ooxml_guard.py
│     │  ├─ docx/ package.py reader.py classify.py writer.py runmap.py xmlnorm.py
│     │  ├─ segment/ sentences.py sections.py
│     │  ├─ protect/ detectors/{citation,number,unit,chem,math,xref,acronym,term}.py
│     │  │           plan.py placeholders.py realign.py
│     │  ├─ refine/  pipeline.py prompts.py diagnostics.py postprocess.py
│     │  ├─ verify/  l1_tokens.py l2_relations/{extract,schema,compare}.py l3_llm.py report.py
│     │  ├─ changes/ hunks.py history.py
│     │  ├─ store/   projects.py sqlite.py backup.py secure_delete.py
│     │  └─ jobs.py
│     └─ prompts/<model_family>/<mode>.<section>.txt   # versioned, hashed into history
├─ bench/
│  ├─ corpus/passages.jsonl           # 40 passages + gold annotations (§H/§I)
│  ├─ corpus/gold_relations.jsonl
│  ├─ perturbations/                  # synthetic error injections for verifier recall
│  ├─ run_bench.py  score.py  rate_ui/ (blind human rating, static HTML served locally)
│  └─ results/<date>_<model_digest>/
├─ frontend/src/
│  ├─ api/ client.ts sse.ts types.gen.ts
│  ├─ store/ project.ts changes.ts history.ts jobs.ts health.ts
│  ├─ editor/ Editor.tsx extensions/{ProtectedSpan,ParagraphId,HunkMark,SelectionScope}.ts
│  ├─ components/ ChangeReview.tsx HunkCard.tsx IntegrityPanel.tsx HistoryDrawer.tsx
│  │              CompareView.tsx ModelStatus.tsx ImportDialog.tsx GlossaryEditor.tsx
│  │              SettingsDialog.tsx BackupDialog.tsx
│  └─ lib/ diff.ts tokens.ts
├─ tests/  (backend) unit/ docx_roundtrip/ fixtures/*.docx security/ verify/ e2e/(Playwright)
└─ scripts/ install.ps1 start.ps1 bench.ps1 gen_types.ps1 verify_offline.ps1
```

---

## C. Revised API specification

Base `/api/v1`. All requests require header `X-AW-Token: <launch-token>`; GET of `/` and static assets require `?t=` once, which sets an `HttpOnly; SameSite=Strict` cookie. Error envelope unchanged from v0.1 plus `trace_id`.

### Health and models
| Method | Path | Notes |
|---|---|---|
| GET | `/health` | `{backend, ollama:{reachable, version, bound_loopback:bool}, model:{name, digest, state:"ready|missing|cold"}, egress_guard:"active"}` |
| GET | `/models` | From Ollama `/api/tags` + `/api/show`: name, digest, params, quant, ctx, family |
| PUT | `/models/active` | `{name}`; rejects if absent or not in `models.allowed` benchmark-approved list (override flag) |
| POST | `/models/warmup` | |

### Projects and documents
| Method | Path | Notes |
|---|---|---|
| GET/POST | `/projects` | POST multipart `.docx` → intake guard → read → `{id, sections[], paragraphs[], warnings[]}` |
| GET | `/projects/{id}` | Paragraphs with `edit_class`, `section_type`, spans, protection plan |
| PATCH | `/projects/{id}/meta` | `{title, section_overrides:{pid: section_type}, discipline, spelling:"en-GB|en-US"}` |
| DELETE | `/projects/{id}` | Secure delete (§G); `?keep_backup=false` |
| PATCH | `/projects/{id}/paragraphs/{pid}` | Manual text edit → new change-set with origin `manual` |

### Refinement (scoped)
| Method | Path | Body |
|---|---|---|
| POST | `/projects/{id}/refine` | `{scope:{type:"paragraph"|"sentences"|"expression", pid, sent_ids?, char_range?}, mode, section_type?, protection:"conservative"|"standard", options:{candidates:1|2}}` → `{job_id}` 202 |
| GET | `/jobs/{id}/events` | SSE: `queued, started, token(preview), candidate, verify, changeset, error, end` |
| GET | `/jobs/{id}` · POST `/jobs/{id}/cancel` | |

`mode` ∈ `proofread | natural | concise | analytical | sentence`. `expression` scope = user-selected span ≤ 25 words; returns up to 3 alternatives, no surrounding rewrite.

### Change-sets and hunks
| Method | Path | Notes |
|---|---|---|
| GET | `/projects/{id}/changesets?status=` | `ChangeSet{id, pid, scope, mode, model_digest, prompt_hash, base_rev, hunks[], report}` |
| GET | `/changesets/{id}` | |
| POST | `/changesets/{id}/hunks/{hid}/accept` · `/reject` | Accepting a hunk re-runs L1/L2 on the **resulting** paragraph (partial acceptance can itself create inconsistency) |
| POST | `/changesets/{id}/accept_all` · `/reject_all` | |
| POST | `/changesets/{id}/override` | `{reason (≥15 chars), check_ids[]}` |
| POST | `/changesets/{id}/edit` | User tweaks proposed text before accept → re-verify |

### History
| Method | Path | Notes |
|---|---|---|
| GET | `/projects/{id}/history?pid=` | Ordered revisions per paragraph `{rev, text_hash, origin, changeset_id, ts}` |
| GET | `/projects/{id}/paragraphs/{pid}/revisions/{rev}` | Text at revision |
| POST | `/projects/{id}/undo` · `/redo` | Server-side, document-level linear stack of accepted operations |
| POST | `/projects/{id}/paragraphs/{pid}/restore` | `{rev}` → new revision (history never rewritten) |
| DELETE | `/projects/{id}/history` | `{before?:ts}` secure purge; current text kept |

### Verification, export, misc
| Method | Path | Notes |
|---|---|---|
| POST | `/projects/{id}/verify` | Run L1/L2(/L3) on arbitrary original vs current pair |
| GET | `/projects/{id}/claims?pid=` | Extracted claim tuples (debug/inspection view) |
| GET | `/projects/{id}/export?track_changes=true` | DOCX; response includes `X-AW-Export-Report` id |
| GET | `/exports/{id}/report` | Per-paragraph written/skipped/reason |
| GET/PUT | `/glossary`, `/settings` | |
| POST | `/backup` → zip download · POST `/restore` multipart | §G |

---

## D. Revised academic writing pipeline

### D.1 Section classification
`sections.py` assigns `section_type ∈ {abstract, introduction, literature_review, methods, results, discussion, conclusions, other}` by heading regex (incl. numbered, "Materials and methods", "Experimental", "Results and discussion" → `results_discussion`), propagated to subsequent paragraphs. [T] on fixtures; user override in UI always wins. Unknown → `other` → only `proofread` and `sentence` modes enabled by default.

### D.2 Diagnostics are descriptive, not targets
v0.1's "reduce passive / nominalization / length" is withdrawn. Diagnostics are computed and **compared to a section-specific band**, and only out-of-band *and* defect-patterned items become instructions.

| Feature | Treated as defect only when |
|---|---|
| Passive | Agent is relevant and hidden in interpretive claims (Discussion: "it was concluded"), or ≥3 consecutive agentless passives create ambiguity about who did what. **Never** in Methods procedure descriptions. |
| Nominalization | Stacked (≥2 nominalizations linked by "of" within 6 tokens) *and* a verb form exists. Technical nominal terms (e.g., "moisture absorption", "fibre degradation") in glossary are exempt. |
| Sentence length | >45 words **and** ≥3 clauses **and** results/claims interleaved. Long sentences listing conditions in Methods are exempt. |
| Formal vocabulary | Only items on a configurable "empty phrase" list (e.g., "it is worth noting that", "plays a crucial role in") — not register-appropriate formal words. |
| Hedging | Never reduced automatically. Missing hedge on a speculative causal claim → flagged to the user, not inserted. |

### D.3 Section instruction blocks (inserted into the system prompt)
- **Introduction**: maintain funnel (field → gap → objective); do not soften or strengthen the stated gap; keep citation placement attached to the claim it supports; objective sentence must remain explicit.
- **Literature review**: preserve attribution (who found what); do not merge findings from distinct citations into one claim; keep contrasts ("whereas", "in contrast") between sources; no new evaluative adjectives about cited work.
- **Methods**: passive and procedural sequence are conventional — preserve order of steps, all parameters, equipment, standards (ASTM/ISO codes), specimen counts; improve only grammar, ambiguity, and redundancy.
- **Results**: no interpretation added; preserve every number–property–condition association; keep reporting tense; keep reference to figures/tables.
- **Discussion**: preserve hedge strength and causal direction; mechanism claims stay tentative if tentative; preserve stated limitations; may improve logical connectives.
- **Conclusions**: no new claims; no stronger generalisation than the body; preserve limitations and future work.

### D.4 Editing modes
| Mode | Allowed operations | Word-ratio band | Default protection |
|---|---|---|---|
| `proofread` | Grammar, spelling, punctuation, agreement, article use. No reordering, no lexical substitution beyond correction. | 0.95–1.05 | standard |
| `natural` | Above + rhythm, connectives, de-stacking nominalizations, replacing empty phrases | 0.8–1.15 | standard |
| `concise` | Above + redundancy removal; no claim removal | 0.6–1.0 | conservative |
| `analytical` | Strengthen logical structure: explicit contrast/cause connectives **only where already implied**, topic sentences; must not add claims. Outputs a rewrite **plus** a list of "argument notes" (questions to author) shown separately, never inserted. | 0.85–1.2 | conservative |
| `sentence` | Single sentence, any of the above ops; 3 alternatives | 0.7–1.3 | standard |

### D.5 Pipeline stages
1. **Scope resolution**: paragraph / sentence ids / char range → editable text + frozen left/right context (context is shown to the model, marked "DO NOT EDIT", and not returned).
2. **Eligibility**: skip non-editable (§F), bibliography, captions unless explicitly selected, paragraphs whose protected fraction exceeds limit (§D.6).
3. **Diagnostics** (§D.2) → ≤4 targeted instructions.
4. **Protection plan** (§D.6) → model-facing text.
5. **Prompt**: system (role + section block + mode ops + hard rules) / user (context, target, instructions). Output contract: plain text only between `<out>` and `</out>`.
6. **Generation**: `think:false` (hybrid models), temperature per mode (proofread 0.1, others 0.3), `num_ctx` from model profile.
7. **Postprocess**: extract `<out>`; strip think blocks/preambles; reject if output ≈ input for non-proofread modes (no-op) or contains placeholders outside the plan.
8. **Realign** (§D.6.4) → candidate text.
9. **Verify** L1/L2/L3 (§E).
10. **Hunking**: word-level diff → hunks grouped at sentence boundaries; each hunk carries the verification findings touching its spans.
11. Candidates=2: choose the one with fewer BLOCK/WARN, tie-break by smaller edit distance (conservative).

### D.6 Protection system v2

#### D.6.1 Span classes and handling

| Class | Examples | Conservative | Standard |
|---|---|---|---|
| Citation | `[12]`, `[3–5]`, `(Baley et al., 2021)`, Zotero field result | Placeholder `⟦CITE:1⟧` | Same |
| Field / OMML / footnote ref / bookmark-bearing run | — | Placeholder (always; XML-bound) | Same |
| Inline math | `$\sigma_{11}$`, OMML inline, `D₆₀/D₂₃` | Placeholder `⟦MATH:1⟧` | Same |
| Number + unit / quantity | `23.3%`, `60 °C`, `3.8 × 10⁻¹² m²/s`, `n = 11`, `p < 0.05` | Placeholder `⟦QTY:1 \| a percentage⟧` | **Visible verbatim**, verified by L1/L2 |
| Chemical formula / specimen code | `NaOH`, `C₂H₅OH`, `[0/90]₃s`, `F-60`, `T700S` | Placeholder `⟦ID:1⟧` | Visible, verbatim-checked |
| Glossary term / acronym | `ILSS`, `fibre–matrix interface`, `Fickian` | Visible, verbatim-checked | Visible, verbatim-checked |
| Cross-ref | `Fig. 3b`, `Table 2`, `Eq. (4)` | Visible, verbatim-checked | Visible, verbatim-checked |
| URL / DOI | | Placeholder | Placeholder |

Rationale: v0.1 masked everything, which damaged fluency and grammar; visible-but-checked spans give the model linguistic context and L1/L2 still catch alteration. Only spans whose surface the model **cannot** reproduce safely (XML-bound, citations, math) are always masked.

#### D.6.2 Placeholder format
`⟦TYPE:n | hint⟧`, e.g. `⟦CITE:2⟧`, `⟦QTY:3 | a temperature⟧`, `⟦MATH:1 | a symbol, singular noun⟧`. Hints carry grammatical number/category so the model can choose articles and agreement. Tokenisation stability of `⟦⟧` is verified per model in the benchmark (§H, metric P-tok); fallback delimiter `[[TYPE_n]]` if a model mangles `⟦`.

#### D.6.3 Positional constraints
Each placeholder records its **anchor**: index of the sentence and the nearest content-word lemma to its left (citation anchored to the clause it supports). After generation:
- Citation must remain in the same sentence (sentence alignment, §E.1) and within the clause containing its anchor lemma (or its synonym list) → else BLOCK `CITE_MOVED`.
- Sentence-final citations before the full stop must remain before it (style preservation) → WARN.

#### D.6.4 Realignment and repair
- Exact multiset match → accept.
- Duplicated placeholder → BLOCK (never auto-dedupe: which instance is right is ambiguous).
- Deleted placeholder → one retry with explicit list "You omitted ⟦CITE:2⟧; return the text with every listed token exactly once". Second failure → changeset `failed_protection`, raw output visible.
- Mangled placeholder (`⟦CITE 2⟧`, `[CITE:2]`) → normalise by regex if unambiguous, record WARN `PH_NORMALISED`.
- Invented placeholder → BLOCK.

#### D.6.5 Citation-heavy paragraphs
Density `ρ = protected_chars / total_chars`. ρ > 0.35 (standard) / 0.25 (conservative): only `proofread` and `sentence` modes allowed; paragraph-level `natural/concise/analytical` disabled with explanation. Literature-review paragraphs with ≥6 citations: citations are grouped per sentence into one composite placeholder `⟦CITE:3-5⟧` only when contiguous in the source (reduces placeholder count without allowing reordering inside the group).

#### D.6.6 Detectors — specifics
- **Numbers**: Unicode-aware (`−` U+2212, thin spaces, `×10⁻³`, superscripts), decimal comma option, ranges (`20–60 °C`), `±`, inequalities, percentages, ratios, scientific notation. Canonical form `(value, unit_canonical, operator, tolerance)` for L2 comparison; number words ("three") ↔ digits equivalence.
- **Units**: curated SI + composites list (`MPa, GPa, kN, N/mm², J/m², mm/min, wt%, vol%, °C, K, h, RH %, g/m², tex, dtex, picks/cm, ends/cm`), with spacing normalisation (`23 °C` ≡ `23°C` for comparison, surface preserved).
- **Chemical**: element-symbol grammar `([A-Z][a-z]?\d*)+` validated against periodic table, with ≥2 element tokens or digit; ions/charges; common names list (NaOH, KMnO₄, APTES, MAPP, PLA, PP, PA11).
- **Math**: LaTeX delimiters, OMML (structural), Unicode math runs (Greek + sub/superscript), variable-with-subscript pattern (`D₆₀`, `E_11`, `σ_t`).
- **Acronyms**: detect definitions `long form (ACR)`; record pair. Rule: first occurrence in document must keep the definition; elsewhere acronym verbatim; expansion/contraction by the model → WARN `ACRONYM_CHANGED`. Plural `ILSSs` vs `ILSS` → normalised compare.
- **Subscript/superscript in runs**: any run with `w:vertAlign` is protected at XML level (§F) and appears to the model as its Unicode equivalent if one exists, else placeholder.

---

## E. Revised scientific integrity verification

Three layers. Only L1 and L2 can BLOCK. Nothing claims semantic equivalence.

### E.1 Sentence alignment (prerequisite)
Monotonic alignment of original→output sentences by DP over Jaccard of content lemmas + shared protected spans; supports 1:1, 1:2, 2:1. Unaligned original sentence → WARN `SENT_DROPPED`; unaligned new sentence with a claim tuple → BLOCK `CLAIM_ADDED`. [T]

### E.2 L1 — token invariants (v0.1 V1–V8, retained, tightened)
Placeholder multiset; quantity multiset (canonical); citation multiset; glossary/acronym/xref verbatim; negation; direction-word flips; hedge level; quantifiers incl. "significant(ly)"; length band per mode. [G] that the checks run; [T] for detector recall.

### E.3 L2 — relation layer (claim tuples)

#### Schema
```
Claim {
  id, sent_ref,
  subject:   Entity   # material/configuration/specimen/group, e.g. "configuration D", "alkali-treated flax/PLA"
  property:  Term     # ILSS, tensile modulus, water uptake, D
  condition: [Cond]   # 60 °C, 3 years immersion, 85 % RH, after 1000 cycles
  value:     Qty?     # 23.3 %, 72 MPa
  direction: +|-|=|~|null   # increase/reduction/no change/comparable
  comparator: Entity? # "relative to untreated", "versus configuration A", "control"
  stat:      {sig: true|false|null, p: Qty?, test: str?}
  modality:  assert|hedged|negated|hypothesis
  relation:  measured|caused_by|attributed_to|consistent_with|contrasts_with
}
```

#### Extraction — deterministic first
1. **Entity lexicon per document**: built at import from (a) glossary, (b) capitalised/coded designations (`configuration [A-Z]`, `[A-Z]\d?` in tables, `Sample \w+`, material strings `fibre/matrix` pattern `\w+/\w+`), (c) table header cells. Users can edit the lexicon.
2. **Property lexicon**: seed (ILSS, IFSS, tensile/flexural strength/modulus, strain to failure, water uptake, diffusion coefficient, Tg, storage modulus, impact energy, porosity, fibre volume fraction, …) + glossary + acronym pairs.
3. **Clause segmentation** on `; , whereas, while, but, compared with, relative to, and` and coordination.
4. **Pattern grammar** (ordered, ~25 rules) binding within a clause, e.g.:
   - `ENTITY (showed|exhibited|had|yielded) (a|an)? QTY (increase|reduction|decrease|improvement|loss) in PROPERTY`
   - `PROPERTY (of|for) ENTITY (increased|decreased|dropped|rose) by QTY (compared with|relative to|versus) ENTITY`
   - `QTY (higher|lower) PROPERTY than ENTITY`
   - `ENTITY … PROPERTY of QTY (at|after|under) COND`
   - Elided-subject coordination ("…, whereas A showed a 42.7 % reduction" inherits PROPERTY from previous clause).
   - Significance: `(statistically )?significant(ly)?`, `p\s*[<=>]\s*QTY`, `not significant`, `n.s.`
5. Unbindable quantities → `Claim` with null slots marked `partial`. Never guessed.

#### Comparison
For each aligned sentence pair, compute claim sets C_o, C_n. Key = (subject, property, condition-set). Checks:

| Check | Rule | Severity |
|---|---|---|
| R1 association swap | Same multiset of values but a value moved to a different key | BLOCK `ASSOC_SWAP` |
| R2 direction flip | Same key/value, direction differs | BLOCK |
| R3 comparator change | Comparator entity changed/removed | BLOCK |
| R4 condition change | Condition added/removed/altered for a key | BLOCK |
| R5 significance change | sig/p changed or "significant" added to a non-stat claim | BLOCK |
| R6 modality strengthening | hedged→assert, hypothesis→assert, negated→assert | BLOCK; weakening → WARN |
| R7 relation change | measured→caused_by, consistent_with→caused_by | BLOCK (causal overclaim) |
| R8 partial-claim coverage | Original sentence had ≥1 quantity not bound by extraction | WARN `L2_INCOMPLETE` — "relation not verified for this sentence" |
| R9 cross-sentence moves | Quantity moved to another sentence | WARN; BLOCK if R1 also triggered |

Worked example (required unit test `test_assoc_swap_ilss`):
- Original → `{D, ILSS, +, 23.3%}`, `{A, ILSS(inherited), −, 42.7%}`
- Rewrite → `{D, ?, +, 42.7%}`, `{A, ?, −, 23.3%}`; property inherited from context in both; keys (D,ILSS), (A,ILSS) map to different values → R1 BLOCK. L1 alone passes (identical multisets) — this test asserts L1=PASS and L2=BLOCK.

#### Claim levels
- [G] L2 runs on every candidate; R8 is always reported when extraction is partial (no silent pass).
- [T] Recall/precision of R1–R7 on perturbation suite (§I.3): targets recall ≥ 0.95 for R1/R2/R5 on in-pattern sentences.
- [E] Coverage (share of quantity-bearing sentences fully bound) ≥ 70 % on the 40-passage corpus; the remainder is R8 WARN, i.e., flagged unverified.
- Explicit limitation: sentences with nested comparatives, anaphora across >1 sentence ("the latter"), or values only in tables are not reliably extracted.

### E.4 L3 — local-model advisory [X]
Two prompts, JSON-schema constrained (`format` parameter), temperature 0:
1. **Claim-list extraction** from original and output separately → compared with the same R-rules; disagreement with L2 shown as "advisory difference".
2. **Contrastive QA**: for each original claim tuple, ask "In TEXT B, what is the [property] of [subject] under [condition]?" → string-compare with gold value. Mismatch → WARN `L3_MISMATCH`.
L3 never upgrades a WARN/BLOCK to PASS. L3 timeouts are non-fatal. Benchmark measures L3 false-alarm rate; disabled by default if > 20 %.

### E.5 Report
Per changeset: per check {id, layer, severity, spans_orig, spans_new, message, claim_ids}. UI groups by hunk. Overall status: BLOCK > WARN > UNVERIFIED (any R8) > PASS. "PASS" text is shown as "No issues detected by checks L1–L2" — never "verified correct".

---

## F. Revised DOCX preservation strategy

### F.1 Approach
python-docx is insufficient for edits (its `paragraph.text` setter destroys runs, fields, hyperlinks, bookmarks). Use **lxml directly on the package parts**; python-docx is used only to open the package and resolve styles (or drop it entirely and read `[Content_Types].xml` + rels via `zipfile` + lxml — preferred, removes a dependency with hidden behaviour). Decision: **lxml + zipfile only**; python-docx kept as a test-only oracle.

Package handling: copy every ZIP member byte-for-byte except parts actually modified (`word/document.xml`, and only if needed `word/footnotes.xml`, `word/endnotes.xml`). Preserve member order, compression type, and timestamps. `[Content_Types].xml`, rels, styles, numbering, theme, settings, customXml (Zotero/Mendeley prefs), media: untouched.

### F.2 Text model
Each `w:p` is linearised into a sequence of **atoms**:
- `TEXT(run_ref, offset, chars, rPr_ref)` from `w:t` (respect `xml:space`), `w:tab`→`\t`, `w:br`/`w:cr`→ line-break atom, `w:noBreakHyphen`, `w:softHyphen`, `w:sym` (symbol atom, protected).
- `OPAQUE(xml_subtree)` for anything else inline: field complex (`w:fldChar begin … end` incl. `instrText` and result runs — whole span is one atom), `w:fldSimple`, `w:hyperlink` (atom; its display text is editable only in conservative-off advanced mode — default protected), `m:oMath`/`m:oMathPara`, `w:footnoteReference`, `w:endnoteReference`, `w:commentRangeStart/End`, `w:commentReference`, `w:bookmarkStart/End`, `w:drawing`, `w:object`, `w:pict`, `mc:AlternateContent`, `w:sdt` (content controls), `w:smartTag`, `w:ins`, `w:del`, `w:moveFrom/To`, `w:permStart/End`.
- Ignorable for text but preserved positionally: `w:proofErr`, `w:lastRenderedPageBreak`, rsid attributes.

Model-visible text = TEXT atoms + placeholder per OPAQUE atom.

### F.3 Edit-safety classes per paragraph

| Class | Condition | Allowed |
|---|---|---|
| **E (editable)** | Body `w:p` in `document.xml` or table cell `w:p`; no `w:ins/w:del/w:moveFrom/To`; no `w:sdt` wrapping; not in TOC/bibliography field result; not heading/caption style (unless user unlocks) | Rewrite TEXT atoms; OPAQUE atoms re-emitted unchanged in new order constrained by D.6.3 |
| **P (protected-inline)** | Editable paragraph containing bookmarks spanning text, comments ranges, or hyperlinks with display text | Edit allowed only outside the ranges; range-internal TEXT frozen |
| **R (read-only)** | Tracked changes present; content controls; text boxes (`w:txbxContent`); headers/footers; footnote/endnote bodies (v1); TOC; bibliography (Zotero `ADDIN ZOTERO_BIBL`, EndNote `ADDIN EN.REFLIST`, or heading-detected); fields of type `TOC, INDEX, REF, PAGEREF, SEQ, NOTEREF`; equation-only paragraphs; `mc:AlternateContent` | Shown for context; not sent to model; export byte-identical |
| **X (refuse import)** | Encrypted (OLE CFB), `.docm` macros, `altChunk`, strict OOXML namespace (`purl.oclc.org/ooxml`), malformed XML | Import rejected with reason |

Footnote/endnote bodies: R in v1; E in roadmap phase 4 after their own round-trip suite.

### F.4 Writing an edited paragraph
1. Recompute atoms from the **current export copy** and assert paragraph text hash == import hash (else skip, report `EXPORT_MISMATCH`).
2. Diff old TEXT stream vs new text at character level (diff-match-patch, semantic cleanup off).
3. Map each output character to an `rPr`:
   - unchanged chars keep their original run's `rPr`;
   - inserted chars inherit `rPr` of the preceding unchanged char **unless** that `rPr` carries `w:vertAlign`, `w:i` on a single word, `w:b`, `w:caps`, `w:smallCaps`, `w:strike`, `w:highlight`, `w:color` (local emphasis) — then inherit the paragraph's dominant `rPr` (mode by char count);
   - a deleted span whose `rPr` was local emphasis whose replacement is a different word → WARN `FORMAT_DROPPED` listed in export report.
4. Coalesce adjacent same-`rPr` chars into runs; emit `<w:r><w:rPr/><w:t xml:space="preserve">`.
5. Re-insert OPAQUE atoms at their realigned positions with original XML (deep copy, identical attributes).
6. Preserve `w:pPr` byte-identical; preserve `w:bookmarkStart/End` positions relative to adjacent OPAQUE atoms; drop `w:proofErr` inside rewritten spans only (Word regenerates), keep elsewhere.
7. Track-changes export: wrap deletions as `<w:del w:id w:author="AcademicWrite" w:date><w:r><w:rPr/><w:delText>` and insertions as `<w:ins>`; `w:id` values allocated above the document's max existing id (scan all parts incl. comments/bookmarks).

### F.5 XML round-trip tests
Normalisation `xmlnorm.py`: canonical XML (C14N 2.0), strip rsid attributes and `w:proofErr` for comparison only.

| Test | Fixture | Assertion |
|---|---|---|
| T-RT0 identity | all fixtures | Export with zero accepted edits → every ZIP member byte-identical to original |
| T-RT1 untouched parts | all | Edit one paragraph → all members except `document.xml` byte-identical |
| T-RT2 untouched paragraphs | all | Edit paragraph k → C14N of every other body child identical |
| T-RT3 OPAQUE invariance | fields, OMML, notes, hyperlinks, bookmarks, comments, drawings | Multiset of C14N(OPAQUE subtrees) in edited paragraph identical before/after |
| T-RT4 Zotero | Zotero numeric + author-year docs | `instrText` JSON identical; Zotero "Refresh" in Word after export produces no prompt (manual test M1) |
| T-RT5 EndNote | `ADDIN EN.CITE` doc | `instrText` + `fldData` identical |
| T-RT6 OMML inline + display | | `m:oMath` C14N identical; Word opens without repair |
| T-RT7 footnotes/endnotes | | `footnotes.xml`/`endnotes.xml` byte-identical; reference ids preserved & unique |
| T-RT8 mixed formatting | bold/italic/sub/superscript words | Unchanged chars keep exact rPr; sub/superscript chars never re-emitted by model (protected) |
| T-RT9 tables | merged cells (`w:gridSpan`, `w:vMerge`) | `w:tblPr`, `w:tcPr` identical; cell paragraph edit only |
| T-RT10 headers/footers | | header*/footer* parts byte-identical (R class) |
| T-RT11 tracked changes | doc with ins/del | Affected paragraphs R; byte-identical |
| T-RT12 track-changes export | | Word accept-all reproduces proposed text (automated via LibreOffice headless *if installed* — optional; else manual M2); ids unique |
| T-RT13 schema validity | all exports | Validate `document.xml` against ECMA-376 transitional XSD (bundled offline) |
| T-RT14 Word open | all exports | Manual M3 checklist: opens without "unreadable content"; page count unchanged ±0 for proofread edits |
| T-RT15 fuzz | mutated fixtures | Reader never crashes; returns X with reason |

Fixture set (`tests/fixtures/`): ≥14 DOCX authored in Word 365 (Windows) and LibreOffice: plain; Zotero numeric; Zotero APA; EndNote; Mendeley; OMML inline/display; footnotes+endnotes; hyperlinks+bookmarks+cross-refs (REF/SEQ); comments; tables with merges; header/footer; tracked changes; content controls; text boxes; mixed formatting/sub-superscripts; Korean/Greek characters.

Promised preservation = exactly the rows above. Any element not listed (e.g., `w:customXml` inline, SmartArt, ink, embedded OLE inside editable paragraphs) → paragraph classified R automatically (allow-list, not deny-list): **a paragraph is E only if every child element type is on the tested allow-list**.

---

## G. Revised privacy and security strategy

| Threat | Control | Level |
|---|---|---|
| Remote access | uvicorn `--host 127.0.0.1`; startup asserts bound address is loopback; refuses `0.0.0.0` config | [G] |
| DNS rebinding | Middleware rejects any `Host` header not in `{127.0.0.1:8765, localhost:8765}` → 421 | [G] test |
| CSRF from other tabs/sites | (1) per-launch 256-bit token required in `X-AW-Token` on all `/api` calls (custom header forces CORS preflight; no CORS allowed → browser blocks); (2) `Origin` must equal own origin on state-changing requests; (3) cookie `SameSite=Strict`; (4) no `GET` mutates state | [G] test |
| CORS | No CORS middleware at all (same-origin SPA). Dev mode: Vite proxy, still same-origin. | [G] |
| Token leakage | Token passed in initial URL only, then moved to sessionStorage and URL cleaned via `history.replaceState`; regenerated each launch | [E] |
| XSS via document content | TipTap renders via schema (no raw HTML); strict CSP `default-src 'self'; script-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; frame-ancestors 'none'` | [G] header test |
| Upload validation | Extension `.docx`, magic `PK\x03\x04`, size ≤ 50 MB, must contain `[Content_Types].xml` + `word/document.xml` with expected content type | [G] |
| ZIP bomb | Before extraction: member count ≤ 2000; each member uncompressed ≤ 100 MB; total ≤ 300 MB; per-member ratio ≤ 100:1 (except media); stream-decompress with running byte cap (do not trust headers) | [G] tests with crafted bombs |
| Path traversal | Never extract to disk; read members in-memory by name; reject names with `..`, absolute, drive letters, backslashes | [G] |
| XXE / billion laughs | lxml `XMLParser(resolve_entities=False, no_network=True, load_dtd=False, huge_tree=False)`; reject any part containing `<!DOCTYPE` | [G] |
| Malformed DOCX | All parse errors caught → class X with reason; process time limit 20 s per import | [G] |
| Macros / OLE | Refuse `.docm`, `vbaProject.bin`; embedded OLE objects → OPAQUE/R, never opened | [G] |
| External requests (backend) | `net_guard` patches socket connect: allow only 127.0.0.1:11434; everything else raises and logs | [G] test |
| External requests (frontend) | No CDN/fonts; CSP `connect-src 'self'`; build check greps `dist/` for `http(s)://` outside license comments | [G] CI |
| Ollama exposure | `/health` checks `OLLAMA_HOST` env and probes the machine's LAN IP:11434; if reachable → red warning "Ollama exposed to network" with fix (`setx OLLAMA_HOST 127.0.0.1`) | [T] |
| Ollama telemetry/update checks | Ollama desktop app checks for updates online; document disabling auto-update or running `ollama serve` directly; this is outside AcademicWrite's control → stated limitation | [E] |
| Logs | Structured logs contain ids, hashes, durations, error codes only. Redaction filter rejects any log record field > 200 chars or containing ≥ 8 consecutive words. Debug mode that logs prompts is opt-in, time-limited (auto-off after 1 h), and writes to a separate file deleted on exit | [G] test |
| Prompt files / history at rest | Stored in `%LOCALAPPDATA%` (user ACL). Optional: Windows EFS/BitLocker advice. No app-level encryption in v1 (key management would be theatre) | [E] stated |
| Project deletion | Delete SQLite rows + `VACUUM`, overwrite then unlink project files; note: SSD wear-levelling and Volume Shadow Copies mean physical erasure is **not** guaranteed | [T] logical deletion; physical erasure not claimed |
| History deletion | Per-project purge with `DELETE` + `VACUUM` + WAL checkpoint(TRUNCATE) | [T] |
| Backup | `POST /backup` → zip of project dirs + SQLite (online backup API) + config + glossary + manifest with SHA-256 per file | [T] |
| Restore | Same intake guard as DOCX; manifest hashes verified; restore into new project ids (no overwrite unless confirmed); schema version check + migrations | [T] |
| Dependency supply chain | Hash-locked Python deps, `npm ci` with lockfile; offline wheelhouse | [E] |

---

## H. Model benchmarking protocol

### H.1 Candidates (tags verified against ollama.com library on 2026-11-03; **re-verify at install with `ollama show <tag>` and record digest**)

| ID | Tag | Notes |
|---|---|---|
| M1 | `qwen3:4b-instruct-2507-q4_K_M` (≡ `qwen3:4b-instruct`) | Non-thinking; ~2.5 GB |
| M2 | `qwen3:4b-instruct-2507-q8_0` | Same weights, higher precision; isolates quantization effect; ~4.3 GB |
| M3 | `qwen3:8b` | Hybrid thinking; run with `think:false`; ~5.2 GB. **No `8b-instruct-2507` tag was found** — v0.1's implied 8B instruct upgrade does not exist |
| M4 | `qwen3.5:9b` | Listed in library (sizes 0.8b–122b); thinking-capable → `think:false`; exact quant tags to be read from `ollama show` |
| M5 | `gemma3:12b-it-qat` | Strong English prose; ~8.9 GB; requires ≥12 GB VRAM for full offload, else CPU split |
| M6 (optional) | `granite4:tiny-h` | Hybrid Mamba; long context; ~4.2 GB; tests whether a non-Qwen small model is competitive |

Excluded unless hardware allows: ≥20B models (`qwen3.5:27b`, `gemma3:27b`) — included as **reference ceiling** run only if ≥24 GB VRAM present.

### H.2 Controlled conditions
- Same machine; record CPU, RAM, GPU, VRAM, driver, Windows build, Ollama version (pinned for the run), model digest.
- Identical system prompt + mode/section blocks; model-family-specific chat template handled by Ollama only (no per-model prompt tuning in the primary run). A secondary "tuned prompt" run is allowed but reported separately.
- Options: `temperature` per mode, `top_p 0.9`, `seed 42`, `num_ctx 8192`, `num_predict` = 2× input tokens, `keep_alive 0` between models, fresh model load before each model's run; 1 warm-up call excluded.
- Each passage × mode run **3 times** (seed 42, 43, 44) to measure variance.
- Modes benchmarked: `proofread`, `natural`, `concise` on all 40 passages; `analytical` on Discussion/Intro subset; `sentence` on 20 sentences.
- Protection: standard and conservative both run.

### H.3 Metrics
Deterministic (computed by `score.py`):
- **P-num** numerical fidelity: % outputs with zero L1 quantity violations.
- **P-cite** citation preservation: % with exact citation multiset and no CITE_MOVED.
- **P-term** terminology: % with zero glossary/acronym violations.
- **P-rel** relationship preservation: % with zero L2 BLOCK vs gold relations (gold-annotated, not just L2-vs-L2).
- **P-tok** placeholder protocol: % first-attempt valid placeholders; retry rate; failed_protection rate.
- **P-ratio** length-band compliance per mode.
- **Grammar (automatic proxy)**: LanguageTool **offline** server (Java, local JAR) error count per 100 words, original vs output — [E] proxy only; optional dependency for benchmark only, not in the app.
- **Readability proxy**: mean sentence length, SD, and nominal-stack count vs section band — descriptive, not a target.
- **Latency**: time-to-first-token, total time, tokens/s; median and p95 per passage.
- **Memory**: peak RSS of `ollama` process (psutil sampler at 4 Hz), VRAM via `nvidia-smi --query-gpu=memory.used` (NVIDIA) or reported "not measurable" otherwise; `ollama ps` size/processor split recorded.

Subjective (blind human rating, `rate_ui/`):
- Two raters (author + one colleague, minimum), outputs shuffled across models, model identity hidden, original shown.
- 5-point scales: **Grammar**, **Naturalness** (reads as competent disciplinary prose), **Technical precision** (terminology, specificity), **Meaning preservation** (claims, hedges, causality), plus binary "would accept as-is".
- 60 items per model (stratified sample), same items for all models.
- Inter-rater agreement: weighted Cohen's κ reported; κ < 0.4 on a dimension → that dimension reported as unreliable.

### H.4 Selection rule
1. **Hard gates** (any failure → model ineligible): P-num ≥ 99 %, P-cite ≥ 99 %, P-term ≥ 98 %, P-rel ≥ 97 % (after retry), failed_protection ≤ 2 %, standard mode.
2. Among eligible models: rank by mean of Meaning preservation and Naturalness (human), tie-break by "accept as-is" rate.
3. Latency is a constraint, not an objective: median paragraph (≤200 words) total time ≤ 90 s on the user's hardware; models exceeding this remain eligible as "quality mode".
4. Results file published locally with all raw outputs; selection re-run when Ollama or model digest changes.

Expected (unverified) outcome: 4B models will fail P-rel or naturalness gates more often than 8–12B; this is a hypothesis to test, not a decision.

---

## I. Software testing and acceptance criteria

### I.1 Evaluation corpus (fixed, versioned, `bench/corpus/`)
40 passages, 80–300 words each, author-owned or rewritten from own drafts (no third-party copyrighted text verbatim):

| Domain / section | Intro | Lit. review | Methods | Results | Discussion | Concl. | Total |
|---|---|---|---|---|---|---|---|
| Natural-fibre composites (flax/hemp/jute; hygrothermal) | 2 | 2 | 2 | 2 | 2 | 1 | 11 |
| Textile / 3D woven composites (architecture, RVE) | 1 | 1 | 2 | 2 | 1 | 1 | 8 |
| Polymer / bio-matrix composites | 1 | 1 | 1 | 2 | 1 | 0 | 6 |
| Mechanical testing (ILSS, tensile, fatigue, DIC) | 0 | 1 | 2 | 3 | 1 | 0 | 7 |
| Experimental methods (conditioning, porosity, µCT) | 0 | 0 | 3 | 1 | 0 | 0 | 4 |
| Modelling / discussion-heavy | 1 | 1 | 0 | 0 | 2 | 0 | 4 |

Stratification constraints: ≥10 citation-dense (≥4 citations), ≥12 with ≥4 quantities, ≥8 with explicit comparisons between groups, ≥5 with statistical statements, ≥5 with OMML/inline math, ≥6 with acronyms defined in passage, ≥4 deliberately flawed (grammar errors, stacked nominalizations) to test whether edits help.

Gold annotations per passage: protected spans, claim tuples (§E.3 schema), hedge levels, citation anchors, expected section type. Two-pass annotation by author; disagreements logged.

### I.2 Deterministic test suites (CI, must pass)
| Suite | Content | Acceptance |
|---|---|---|
| U-detect | Detector unit tests (numbers, units, chem, math, citations, acronyms) incl. Unicode edge cases | 100 % of 400+ cases |
| U-mask | Mask/unmask, duplication, deletion, mangling, invention | 100 % |
| U-L1 | Token invariants | 100 % |
| U-L2 | Claim extraction on gold corpus | Slot-level F1 ≥ 0.85 for subject/property/value/direction on in-pattern sentences; coverage reported |
| P-L2 perturbation | ≥300 synthetic corruptions of gold passages: value swap (R1), direction flip, comparator swap, condition drop, significance add/remove, hedge strengthening, causal upgrade, citation move | Recall ≥ 0.95 for R1/R2/R5, ≥ 0.85 others; false-BLOCK rate on 120 meaning-preserving paraphrases (hand-written) ≤ 10 % |
| DOCX RT | T-RT0…T-RT15 | 100 % automated rows |
| SEC | DNS-rebinding Host, Origin, token, CSP, ZIP bombs (42.zip-style nested, overlapping-file bomb), XXE, path traversal, egress guard, log redaction | 100 % |
| API contract | OpenAPI schema tests + mock Ollama (timeouts, 404, OOM text, malformed stream, think blocks) | 100 % |
| E2E | Playwright: import → refine sentence → accept 1 of 3 hunks → undo → redo → export | Pass |
| Offline | `verify_offline.ps1`: disable adapters, full E2E | Pass |

### I.3 Model-dependent acceptance (selected model, corpus, standard protection)
| Metric | Type | Threshold |
|---|---|---|
| Numerical preservation (after verification gating, i.e., nothing with BLOCK reaches document) | Deterministic | 100 % [G] |
| Numerical preservation (raw model output) | Deterministic | ≥ 99 % |
| Citation preservation (raw) | Deterministic | ≥ 99 % |
| Terminology preservation (raw) | Deterministic | ≥ 98 % |
| Relationship preservation vs gold (raw) | Deterministic (gold) | ≥ 97 % |
| Unverified share (R8) | Deterministic | Reported; ≤ 30 % target |
| Grammar errors (LanguageTool offline) | Automatic proxy | Output ≤ original on ≥ 90 % passages |
| Readability | Descriptive | No acceptance threshold; reported against section bands |
| Semantic faithfulness (human) | Subjective | Mean ≥ 4.3/5; no item ≤ 2 |
| Naturalness (human) | Subjective | Mean ≥ 3.8/5 and > original-text mean for flawed subset |
| Accept-as-is rate (human) | Subjective | ≥ 60 % proofread, ≥ 40 % natural |
| Latency | Measured | Median ≤ 60 s, p95 ≤ 120 s per ≤200-word paragraph on target hardware (document hardware in result) |
| Memory | Measured | Peak RAM leaves ≥ 4 GB free on target machine with Word open |

---

## J. Prioritised implementation roadmap

| Phase | Deliverable | Exit criterion |
|---|---|---|
| 0 | Corpus (40 passages) + gold annotations + DOCX fixture set | Annotated, reviewed; fixtures open in Word |
| 1 | Security skeleton (FastAPI, middleware, net_guard, intake guard) + health/model checks | SEC suite green |
| 2 | DOCX reader/writer (lxml atoms, classes E/P/R/X), identity export | T-RT0–T-RT11, T-RT13, T-RT15 green |
| 3 | Detectors + protection plan + masking | U-detect, U-mask green |
| 4 | L1 + L2 relation layer + perturbation suite | U-L1, U-L2, P-L2 thresholds met **before any model integration** |
| 5 | Ollama client + refine pipeline (modes × sections) + benchmark harness | Bench run on M1–M5; model selected by §H.4 |
| 6 | Change-sets, hunks, history, undo/redo API | API contract + unit |
| 7 | Frontend: editor, scoped selection, hunk review, integrity panel, history, compare view | E2E green |
| 8 | Track-changes export, backup/restore, secure delete | T-RT12, backup tests |
| 9 | L3 advisory, style profile, footnote-body editing | [X] features behind flags; measured false-alarm rate |

Phases 2 and 4 are the critical path; if L2 cannot meet P-L2 recall, Results/Discussion paragraph modes ship restricted to `proofread`.

---

## K. Functionality classification

| Feature | Level |
|---|---|
| Local-only network behaviour (backend) | G |
| Loopback binding, Host/Origin/token checks, CSP | G |
| Original DOCX never modified; zero-edit export byte-identical | G |
| No BLOCKed edit applied without logged override | G |
| Hunk-level accept/reject, undo/redo, revision history | G (functional) |
| Untouched parts/paragraphs byte/C14N-identical on export | T |
| OPAQUE atoms (fields, OMML, notes refs, hyperlinks, bookmarks) preserved in edited paragraphs | T (fixtures only) |
| Zotero/EndNote refresh works after export | T (manual M1) |
| Track-changes export accepted by Word | T (manual M2) |
| Detector recall on numbers/citations/units | T (corpus) |
| L2 detection of association swaps, direction/comparator/condition/significance/modality/causal changes | T on in-pattern sentences; E elsewhere |
| Rich formatting retention for rewritten words | E (heuristic, warns on loss) |
| Language quality improvement | E (benchmark-dependent) |
| Section auto-classification | T on fixtures, E in general |
| L3 LLM advisory checks | X |
| Style profile | X |
| Footnote/endnote body editing | X (phase 9) |
| Ollama not exposed / no Ollama-side telemetry | E (outside app control; checked and warned) |
| Physical erasure on delete | Not claimed |

---

## L. Unresolved technical risks

1. **L2 coverage ceiling.** Rule-based tuple extraction will miss anaphora, nested comparatives and table-only values. Mitigation is honesty (R8 UNVERIFIED), not completeness. If coverage < 60 % on the corpus, the relation layer's value must be re-evaluated (e.g., constrained-JSON L3 promoted only after it meets P-L2 recall).
2. **Gold-relation bias.** Corpus authored/annotated by one person; extraction rules risk overfitting to the author's phrasing. Need a held-out set of ≥10 passages written by others (with permission).
3. **Run-formatting mapping (§F.4.3)** remains heuristic; italic species names, sub/superscripted symbols in non-protected words, and character styles can be lost → reported, not prevented.
4. **Ollama nondeterminism across versions/backends**; benchmarks are only valid for the recorded version + digest + hardware.
5. **Thinking-model leakage**: hybrid models (`qwen3:8b`, `qwen3.5:9b`) may still emit reasoning text with `think:false` on some Ollama versions; postprocess strips `<think>` but malformed partial blocks may slip through → covered by mock-stream tests only.
6. **CPU-only hardware** may make every ≥8B candidate fail the latency constraint, forcing a quality/latency trade-off the selection rule can only expose, not solve.
7. **Placeholder tokenisation** (`⟦`) unverified per model until benchmark P-tok.
8. **Word-only validation**: manual tests M1–M3 require Microsoft Word; LibreOffice behaviour differs; no automated substitute for "opens without repair".
9. **Human rating capacity**: 60 items × 5–6 models × 2 raters ≈ 700 judgements; under-resourcing this collapses subjective metrics to the author's preference.
10. **Benchmark tag drift**: Ollama tags are mutable; only digests are stable. Spec mandates digest pinning but cannot prevent upstream removal.

Sources for tag verification (2026-11-03): ollama.com/library/qwen3/tags, ollama.com/library/qwen3:4b-instruct-2507-q4_K_M, ollama.com/library/qwen3:4b-instruct-2507-q8_0, ollama.com/library (qwen3.5 sizes), ollama.com/library/gemma3/tags, ollama.com/library/granite4/tags.
