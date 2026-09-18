# Changelog

## 0.2.0 — 2026-09-18

- Four complete, independently buildable React consoles with unified navigation, metric cards, searchable lists, detailed drawers and private artifact previews.
- Web/API case assets with immutable revisions, deterministic Workflow v2 compilation and real execution history; no scheduling subsystem added.
- Real HTTP API assertions and expanded Web actions/locators, plus operator-registered target profiles and screenshots.
- DD-style AI CR, Markdown case generation and automatic case compilation with evidence/provenance, persisted input/output and save-to-case flow.
- Supabase Storage artifact catalogue: Markdown, source, JSON, compiled scripts, reports, logs and screenshots. No additional S3 service or credentials.
- Twelve executable sample cases, eleven expected passes and one deliberately failing case verified on the Docker host; four capability tasks verified with explicit mock output.
- Browser-verified platform switching, API filtering, compilation preview, UI-triggered execution, model playground, stored screenshot preview and compilation-to-case save.

Model generation remains explicitly mock until a real provider is configured. The open Markdown/source review is not the complete enterprise repository-wide DD toolchain. Tests remain constrained by registered target policies.

## 0.1.0 — 2026-09-18

Initial standalone source release, part of the four-repository AI-SDLC demo.

- Java 21 / Spring Boot services, a React workbench and a constrained Playwright Runner.
- Independently configured Supabase resources, with an explicit two-project demo layout.
- A NAS Docker Compose integration validated for successful and intentionally failing runs, owner-scoped access, private artifacts, deterministic compiler hashes and container cleanup.
- Apache-2.0 source, reproducible setup examples, tests and CI.

Model generation is explicitly mock in the accepted demo. Real-provider validation, public hostile-code isolation, production capacity and the broader enterprise AI-SDLC feature set are not claimed. See README for this repository's scope and API.
