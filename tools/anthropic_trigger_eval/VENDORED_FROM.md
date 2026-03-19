# Vendored Source

This directory contains a project-owned copy of the Anthropic skill-creator
trigger-eval harness.

Source captured on 2026-03-19 from the locally installed skill-creator cache:

- `/Users/whatsup/.claude/plugins/cache/claude-plugins-official/skill-creator/b36fd4b75301/skills/skill-creator/scripts/run_eval.py`
- `/Users/whatsup/.claude/plugins/cache/claude-plugins-official/skill-creator/b36fd4b75301/skills/skill-creator/scripts/utils.py`

Why vendored here:

- the trigger-eval algorithm is Anthropic-specific and should preserve Claude
  discoverability semantics
- the repository must not depend on an unversioned user-local plugin cache for
  reproducible QA
- project scripts should call a repository path, then record outputs under
  `eval/`
