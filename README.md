# Personal Engineering Harness Workspace

This repository is the **public engineering workspace** for the Personal Engineering Harness.

The harness itself is operated from ChatGPT. Durable private continuity belongs in the private memory repository; this repository contains only public-safe engineering artifacts, experiments, tests, documentation, branches, and pull requests.

## Start a run

The human-facing entry point can be as abstract as:

`/goal 私のキャリアを富ませて`

The agent is responsible for reconstructing the current situation, compiling the goal, discovering useful work, defining completion criteria, implementing the selected work, verifying it, and stopping at a reviewable pull request by default.

See [HARNESS.md](HARNESS.md) for the operating contract.

## Public/private boundary

Do not copy raw private memory, personal context, credentials, tokens, session dumps, or other sensitive source material into this repository. Public artifacts should contain only the minimum public-safe rationale needed to review the engineering work.

## Verification

Run:

```bash
python tools/verify_workspace.py
python -m unittest discover -s tests -v
```

CI runs the same checks on pull requests and on pushes to `main`.

## Merge boundary

Harness work should normally be developed on a branch and proposed through a pull request. Merge remains a human decision.
