# AI-SDLC

A small React workbench that connects three independent Java services into a demonstrable delivery loop.

```text
Requirement / material
  → Model Gateway: structured Workflow
  → Automation Platform: validation + deterministic compilation
  → Sandbox Gateway: Docker / Playwright execution
  → report and provenance in the workbench
```

## Four repositories

Keep these as siblings for the integration example:

- `sandbox-gateway`: execution control and Docker resource lifecycle.
- `model-gateway`: model requests, provider credentials, SSE and audit.
- `automation-platform`: durable runs, Git snapshots, Workflow compiler and test delivery.
- `ai-sdlc`: user interface, optional Supabase Workspace Edge API and integration deployment.

Repository names describe the intended split; no GitHub publication or running deployment is implied by this README.

## Current implementation

- Requirement input, optional registered Git ref, asynchronous execution list, cancellation, report, artifact downloads and provenance.
- Model mode is visible. Mock generation is not presented as a real LLM evaluation.
- Private operator-token login and optional Supabase email login.
- The browser calls Java APIs through the NAS's same-origin reverse proxy; no cloud Edge Function must reach a private NAS IP.
- Supabase stores service data/artifacts; optional Workspace Edge API stores immutable material snapshots with owner-based access.
- A four-service Docker Compose example plus an on-demand Playwright Runner image.

Source is written. Builds, tests, browser checks, Docker/NAS deployment and public release are **pending validation**. The requested implementation phase does not claim runtime acceptance.

## Development

Node 22.12+:

```bash
npm ci
npm run dev
```

Start the three Java services separately on localhost 8081, 8082 and 8083. Vite proxies the API paths. Set public Supabase configuration in a local `public/config.js` if testing account login; never put a service-role key or provider key there. The image generates `config.js` from public-only environment variables at startup.

The operator token is entered at login and kept only in session storage. Supabase login uses the Supabase session; Java services must have issuer/JWKS/audience verification configured. Do not expose this workbench publicly without HTTPS and appropriate access controls.

## NAS deployment

See [examples/stack/README.md](examples/stack/README.md). This is the single integration recipe; each Java repository also builds and tests independently. Production configuration uses Supabase; H2/local artifacts require an explicit development profile.

## Supabase Workspace function

Apply `supabase/migrations/202609180001_workspaces.sql`, then deploy:

```bash
supabase functions deploy ai-sdlc-workspaces --project-ref YOUR_PROJECT_REF --no-verify-jwt
```

The function itself verifies the user with Supabase Auth. `--no-verify-jwt` does not make its application API anonymous. Material creation uses the server-side service role only after identity verification; user table grants cannot update the material. Run attachment uses the user's JWT and RLS. A run reference is metadata and never an authorization credential.

Operator mode persists the original requirement in the automation task. The separate Workspace table is used with Supabase account login; these modes are shown explicitly.

## Tests and acceptance

```bash
npm test
npm run build
```

NAS acceptance scripts (run in the later debugging phase):

```bash
cd examples/stack
python3 smoke.py
python3 smoke.py --negative
```

The smoke script checks the real task result, idempotency, compiler hash, Docker execution and container cleanup. It prints provider mode so synthetic and actual-model evidence remain distinct.

## Scope

A compact interview/open-source demonstration, not a full enterprise AI-SDLC suite. Complete AICR, defect detection, external Wiki/EC connectors, complex knowledge retrieval, Data Pool, K8s and message-broker infrastructure are outside v0.1. See each service's README for execution and security boundaries.

Apache-2.0. Only original implementation and synthetic data are included.
