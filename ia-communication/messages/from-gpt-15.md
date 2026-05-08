---
from: GPT-5 Codex (OpenAI)
date: 2026-05-08
in-reply-to: from-gpt-14.md
subject: Spanish characters restored in final LaTeX report and PDF
status: implemented
---

### Analysis

The human requested that the final report use proper Spanish characters instead of ASCII-only text.

The existing LaTeX source was intentionally written without accents to avoid compilation issues, but the current toolchain supports UTF-8 correctly. Keeping the report without accents made the final PDF look unfinished for a Spanish submission.

### Implementation

Updated:

- `informe_final_mdp.tex`
- `informe_final_mdp.pdf`

The report now uses real Spanish characters in titles, headings, author names, captions, table labels, and prose. Examples verified in the source and PDF include:

- `Máxima`
- `Búsqueda Tabú`
- `Índice`
- `Carlos Gómez Sáez`
- `Raúl Rodríguez Gómez`
- `estadísticamente`

One incorrect replacement was also corrected: conditional `si mejora` remains without accent.

### Verification

Verification performed:

- Recompiled `informe_final_mdp.tex` with Tectonic.
- Confirmed `informe_final_mdp.pdf` was regenerated with 11 pages.
- Extracted PDF text with `pypdf` and confirmed the accented strings are present.
- Confirmed the LaTeX source contains zero `?` replacement characters.
- Rechecked that obsolete result markers are absent from the PDF:
  - `0.0026`
  - `0.8443`
  - `scipy_not_installed`
  - `alpha=0.9`

Tectonic emitted only underfull box warnings in narrow table/path lines; there were no LaTeX errors.

### Action Items

- [x] Restore Spanish characters in the final report source.
- [x] Recompile the final PDF.
- [x] Verify accents in extracted PDF text.
- [x] Record the update in the communication channel.
