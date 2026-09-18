# v0.2 validation — 2026-09-18

## Local

- Java suites: Sandbox 20, Model 26, Automation 23; all pass.
- Four console test suites: 2 each. Four production builds pass.
- Runner tests: 5 pass, including real HTTP fixture validation.
- Existing deployment configuration suite: 11 pass.

## Real NAS + Supabase

- Four consoles and three Java services deployed in Docker Compose with additive Flyway migrations.
- Twelve case assets seeded: six Web and six API. All six API executions pass; five Web executions pass and the intentional missing-text assertion fails as expected.
- Six screenshots and execution evidence written to private Supabase Storage. Stored PNG bytes verified; cross-owner reads for cases and artifacts denied.
- AI CR, Markdown case generation, Web compilation and API compilation complete through the persistent task runtime and model gateway. Mock/fixture mode is displayed in the result.
- Compiled workflow/spec hashes match actual Runner output.

## Browser

Reviewed the actual deployed pages through a loopback test transport that maps a synthetic test marker to the existing demo user's JWT, avoiding real credentials in UI traces. It does not modify production authentication.

Verified: four-platform switch, API filter, case detail and deterministic compiled script, UI-triggered API execution, model playground response, Sandbox report and screenshot preview, DD findings/evidence, and saving an AI-SDLC compiled workflow to the case library. A saved case was read back from the database.

## Boundaries

Real-provider AI analysis, arbitrary hostile code isolation, full enterprise DD repository exploration, test-plan scheduling and broad external target coverage are not claimed. Provider/runtime settings are inspected in the console and configured by the deployment operator.

## Deployment delta

The product UI, Web/API runtime, case/review capabilities and sample runs above were deployed and verified. A subsequent bounded Storage network retry patch passed local tests but its final deployment was interrupted when SSH became unavailable. Runtime images continued serving the accepted v0.2 functionality. Treat this small reliability patch as source-verified until a fresh deployment is recorded.
