# Diagnostic Techniques

Read the section matching the current uncertainty. Use existing tools and project
commands; do not run every recipe. Active experiments require a safe authorized
environment. Preserve incident evidence and containment. When a check is unavailable,
state what observation would distinguish the remaining explanations.

## Useful Feedback and Reproduction

Write the broken contract as an observable question before simplifying the input.
For example, “can tenant B receive tenant A's cached result?” requires both tenants
and a shared cache; a single-tenant green test removes the trigger.

1. Run the current check against the observed unfixed behavior. Confirm that it
   reaches the relevant path and fails for the reported reason, not setup failure.
2. Minimize one dimension while preserving that failure. Keep the original failing
   case as a reference; less code does not guarantee an equivalent mechanism.
3. Match the oracle to the contract: output/invariant for logic, completion and
   cleanup for asynchronous work, distributions under a fixed workload for latency.
4. If an existing test passes despite a confirmed defect, inspect its assertions,
   inputs and boundary. Verify oracle sensitivity with the unfixed revision or an
   authorized isolated control; do not simulate the system under test itself.

If reproduction is unavailable, inspect existing traces and contrast affected versus
unaffected cases. A precise narrowing of the failure boundary is useful progress,
with an explicit limit on any correction claim.

## Experiment Selection

Use a small working note when there are competing explanations:

| Explanation | Supporting / conflicting observation | Next discriminating observation | Result and next action |
|---|---|---|---|
| Suspected mechanism | Evidence with identity and source | What differs if this explanation is wrong? | Confirmed, rejected, or still unresolved |

Do not assign invented probability percentages or populate a fixed number of rows.
For a clear defect, one prediction and a decisive check are enough. For ambiguity,
prefer a check that splits plausible explanations, can run in current conditions,
and has acceptable cost and disturbance. State what each outcome would change
before executing it. Several cheap checks that cannot change the decision are
less useful than one targeted observation of the failing boundary.

**Example: a new handler's expected log is absent.** Existing build identity can
separate an old artifact from current code. With a current artifact, request routing
and a boundary trace distinguish an unreached handler from filtered log output.
Rebuilding first changes the evidence without resolving these alternatives. Absence
of a log proves absence of execution only if that logging channel is known observable.

When two factors may interact, compare the relevant combinations. If a failure needs
both a particular locale and a reused connection, changing either alone can hide it;
record the joint condition rather than declaring one factor the entire cause.

## Trace the Violated Invariant

Start at the first observed bad value, then follow its producers and transformations
backward. At each boundary, ask what must be true, who owns that promise, and where
it was last observed true. Trace control flow forward from the real entry point to
check whether that producer is reached. Join traces by request/task/process identity.

Instrument actual inputs, outputs, ordering and state at the narrow boundary; capture
state before the failing call. A stack trace may show where corruption was detected,
not where it began. Assertions expose internal invariant violations; external input
needs intentional validation and an appropriate error contract.

**Example: retries create duplicate charges.** Trace operation identity across the
caller, retry loop and payment adapter. Distinguish the retry trigger from the missing
idempotency guarantee. Test repeated delivery and the response-loss boundary in an
isolated fake external service or sandbox, never by charging real users to reproduce.
Verify both deduplication and legitimate distinct operations before calling it fixed.

## Bisection and Differential Diagnosis

Use a known-good comparison whose environment and oracle are understood.

- **History:** use `git bisect` in an isolated checkout with known-good/bad revisions
  and a repro command. Preserve local edits. Mark revisions with unrelated build or
  setup failures untestable; do not classify them as reproductions. A bisected commit
  narrows the introduction point but still needs a mechanism explanation.
- **Input:** remove chunks while the same failure persists, then check that the
  minimized input retains the original mechanism. Interactions may span chunks;
  inability to halve further does not prove a single offending value.
- **Configuration:** compare effective values and their precedence, then apply
  selected differences in isolation. A declared configuration may not be the loaded one.
- **Execution path:** observe the invariant mid-path to locate the first divergence,
  then narrow observation to that segment. An early return changes semantics; use it
  only as an explicit isolated intervention, not as neutral instrumentation.

For “works here, fails there,” compare artifact, dependencies, effective configuration,
data, locale/encoding, permissions, time, hardware and concurrency as relevant.
Changing a context and observing recovery supports a hypothesis; identify the causal
boundary before generalizing it. Intermittent bisection needs a justified observation
budget or a controlled schedule; one green run is not a reliable good/bad verdict.

## Runtime and Skill-Loading Failures

Locate the first failing boundary rather than treating installation as execution:

| Boundary | Useful evidence | Misleading shortcut |
|---|---|---|
| Package identity | Actual path, bytes/revision, file name and resource closure | File exists, therefore the intended copy is used |
| Host discovery | Host-specific search roots, trust/settings and discovery result | Another host lists the package, therefore this one finds it |
| Parse and read | Native frontmatter result and referenced-file reads | Static YAML parses, therefore native loading succeeded |
| Invocation | Selection/body-read or execution trace tied to the request | Skill is listed, therefore it was selected and followed |
| Dependencies | Executable/interpreter identity, imports, cwd, permissions and effective configuration | A shell command works, therefore the hook's environment matches |
| Work outcome | Observable result at the user's failure boundary | Successful activation, therefore the task is solved |

Choose the first unknown or contradictory boundary and inspect its actual consumer.
For a hook failing to import a module while a terminal command succeeds, compare the
configured interpreter and dependency environment before editing application logic.
Record concrete tool errors without treating missing access as proof of a broken Skill.
Use existing identity and traces; do not automatically reinstall, clear caches or
modify global trust. If a remedy changes host configuration, respect that operation's
actual scope and authorization.

## Concurrency, Asynchrony and Flaky Failures

Identify the shared resource, owners, lifecycle and ordering needed for the failure.
Compare isolated versus suite execution and fresh versus reused state as clues;
these differences can reflect timing, resources or leakage, so they do not prove one
specific cause. Serialization is a discriminator, not proof that the race is fixed.

Reproduce the relevant interleaving using barriers, controlled callbacks or an existing
scheduler hook in isolated tests. Keep the concurrency that activates the bug. For a
check-then-write race, force both actors past the read before either writes and observe
the invariant. After correction, verify allowed parallel behavior as well as that case.

Wait on the actual completion condition with a bounded timeout and diagnostic state.
A longer sleep can hide a missing synchronization edge. Condition waiting alone does
not repair lost ownership, duplicate callbacks or unpropagated cancellation. Follow
cancellation, timeout and cleanup through all children; check residual processes,
locks, listeners or tasks when the reported completion leaves work running.

For intermittent evidence, retain attempts, failures, conditions and budget. Use stress
or injected latency only where safe. If the budget cannot resolve a rare failure,
report the remaining uncertainty rather than rerunning selectively until green.

## Performance Regressions

Define the target metric and workload: latency distribution, throughput, memory or
resource use; include correctness and load constraints. Match revisions, data, warmup,
cache state and environment. Compare repeated runs and distinguish test noise from a
stable change; a faster response that drops work is a correctness regression.

Use the symptom to choose the observation: CPU profiles for computation, allocation
and heap evidence for memory, waits/queues/locks for contention, traces and query plans
for storage or network paths. Measure the critical path before optimizing an expensive
function that may not explain user latency. Separate time spent executing from waiting.

Form a mechanism hypothesis and predict which measured component will change after
correction. Verify the target workload and relevant tradeoffs, such as increased memory,
starvation or worse tail latency. Keep results scoped to the tested conditions.

## Multiple Causes and Changed Symptoms

A failure may require a trigger plus several enabling conditions. Link evidence by
identity and scenario; split mechanisms only when observations support that split.
If no single explanation accounts for all observations, test interactions or separate
failure populations rather than forcing one root cause.

After a patch changes the signature, compare the same inputs on old and new revisions:

- **Introduced regression:** the patch breaks a previously working contract; inspect
  the change and adjust or revert the affected patch within scope.
- **Unmasked defect:** removal of an earlier failure exposes another mechanism;
  preserve a supported first correction and isolate the newly reachable failure.
- **Changed symptom:** the original mechanism remains and merely fails differently;
  revisit the explanation instead of counting the first issue as resolved.

A changed stack trace alone decides none of these. Preserve linked observations and
patch identities so later debugging does not confuse effects from different versions.

## Fix-Layer Selection

Find the earliest owned boundary where the required invariant can be restored without
breaking another contract. When an internal producer creates invalid state, correct it
there rather than scattering guards at every consumer. When inputs cross a trust
boundary or the producer is outside local control, validation at the receiving adapter
can be the correct fix. A defensive check is useful when it enforces a real contract;
catching and ignoring a failed operation may merely conceal the defect.

For an external-dependency workaround, isolate it, record limitations and removal
conditions, and prepare an upstream report without sending it unless authorized.
Requirements or architecture contradictions require an evidenced upstream decision;
local patch count alone cannot justify that escalation. Retain intentional observability
with its purpose and remove temporary probes after capturing useful evidence.
