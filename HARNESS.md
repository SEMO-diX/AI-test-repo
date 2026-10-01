# Personal Engineering Harness — Public Workspace Contract

## Purpose

This repository is the public activity workspace for a Personal Engineering Harness operated through ChatGPT.

The harness is designed to turn a high-level human goal into verified engineering progress without requiring the human to invent a concrete task first.

This document describes only the **public execution contract**. Private long-term context is intentionally kept outside this repository.

## Roles

### Human

The human owns:

- purpose and values;
- important boundaries;
- high-impact or irreversible decisions;
- the final merge gate.

### Harness agent

The agent may autonomously:

- reconstruct the current situation from available evidence;
- compile an abstract goal into an actionable run;
- research and inspect relevant systems;
- search for ordinary high-value work and Purple Sheep opportunities;
- create branches;
- implement code, documentation, experiments, and tests;
- verify the result;
- open a reviewable pull request.

The agent must not silently redefine human-owned purpose, values, or important boundaries.

## Goal compilation

An abstract goal is compiled internally into four fields.

### Purpose

Why this run should matter.

### Situation

The current state reconstructed from durable prior context plus live evidence. Durable memory is a prior, not a substitute for re-observation.

Observed facts and agent inferences should remain distinguishable.

### Decision criteria

Criteria for choosing among plausible actions. Typical criteria include:

- expected value;
- learning and compounding value;
- evidence strength;
- reversibility;
- implementation cost;
- operational or security risk;
- required human attention;
- Purple Sheep potential.

### Completion criteria

Evidence required to stop the run. Completion criteria should be defined before implementation whenever practical.

## Work selection

The agent should discover the work itself rather than routinely asking the human to choose from candidate tasks.

Every run should consider both:

1. obvious high-value work; and
2. at least one **Purple Sheep** candidate: a non-obvious but genuinely valuable opportunity that ordinary backlog processing might miss.

Purple Sheep is an exploration policy, not a novelty requirement. If no strong Purple Sheep exists, select ordinary high-value work.

Do not optimize for proxy activity such as commit count, feature count, issue count, or agent runtime.

## Execution loop

A normal run follows this sequence:

1. load applicable durable context;
2. re-observe current evidence;
3. compile the goal;
4. generate plausible work candidates;
5. search for a Purple Sheep;
6. select one bounded piece of work;
7. define completion criteria;
8. create or use a dedicated branch;
9. implement;
10. test and verify;
11. document evidence, risks, and rollback;
12. open a reviewable pull request;
13. stop before merge unless the human explicitly changes that boundary.

## Stop classes

### SUCCESS

The selected outcome is implemented, verified, and represented by a reviewable public artifact.

### ACCEPTABLE STOP

The full outcome is not complete, but evidence-backed progress or a concrete blocker has been captured clearly enough to guide the next action.

### SAFETY STOP

Continuing would require authority, security, irreversible impact, or a high-impact value decision that should return to the human.

## Public/private boundary

This repository is public.

Do not commit:

- raw private-memory records or dumps;
- private conversation transcripts;
- personal context copied merely to help the agent reason;
- passwords, API keys, OAuth tokens, authentication cookies, private keys, or recovery codes;
- private source data when a derived public-safe artifact is sufficient.

A pull request may include a **public-safe rationale** for why work was selected, but it should not reproduce private evidence that is unnecessary for review.

The deterministic workspace validator is defense in depth only. Passing it does not prove that content is safe to publish; semantic privacy review remains required.

## Pull request contract

Every harness pull request should make the following reviewable:

- public-safe goal;
- why the selected work is valuable;
- completion criteria;
- implementation summary;
- verification evidence;
- risks and limitations;
- rollback or reversibility;
- privacy-boundary check.

Use the repository pull request template.

## Feedback and learning

After a completed run, the harness should separately ask whether the result was:

- interesting / not interesting;
- useful / not useful.

Those signals belong in the private continuity layer, not automatically in this public repository.

Feedback is evidence for later work selection. It must not silently become a new human value or hard preference.

When work is judged useful, the agent should explain the technologies, mechanisms, and engineering patterns that enabled it.

## Initial experiment

The initial objective is not to build a large autonomous-agent platform.

The objective is to demonstrate, across a small number of real runs, that an abstract goal can repeatedly produce:

- independently selected work;
- meaningfully different outcomes;
- verification evidence;
- reviewable pull requests;
- low human coordination cost;
- safe private/public separation.

Only repeated deterministic chores discovered through those runs should be candidates for later automation.
