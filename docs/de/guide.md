# Die Plattform verwenden

Der Actions-Workflow für Qualität richtet Python 3.12 ein, führt FastAPI und Tests aus und veröffentlicht diese Anleitung von `main` auf GitHub Pages. Die kleine Weboberfläche wird unter `/` bereitgestellt, wenn die API in einem Workflow oder einer kurzlebigen Entwicklungsumgebung läuft. Sie listet Bibliothekseinträge, verarbeitet erfundene Eingaben, zeigt Schutzstatus und speichert Bewertung und Kommentar in SQLite.

## API-Übersicht

- `GET /api/library` listet versionierte Prompts, Agents und Skills.
- `POST /api/run/{id}` führt einen Eintrag aus. Personenbezogene Daten und Vertraulichkeitsmarker werden vorher blockiert.
- `POST /api/approvals/{run_id}` speichert eine benannte menschliche Entscheidung; externe Aktionen werden nie ausgeführt.
- `POST /api/feedback` speichert Bewertung von 1 bis 5 und Kommentar.
- `GET /api/audit` liefert das aktuelle Audit-Protokoll.

Standardmäßig läuft ein deterministischer Mock. Der Model-Smoke-Job in Actions versucht `sshleifer/tiny-gpt2`; bei Fehlern wird der Mock verwendet. Ergebnisse sind Demos und müssen von Menschen geprüft werden.
