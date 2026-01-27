---
description: Review downstream Fedora dist-git PRs created by Packit. Analyzes spec file changes, sources, changelogs, and provides merge recommendations.
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Review and analyze Fedora dist-git pull requests created by Packit automation. This command helps maintainers:
- Verify spec file changes are correct
- Check source archives and checksums
- Validate changelog entries
- Review automated updates from upstream
- Make informed merge/close decisions
- Ensure compliance with Fedora packaging guidelines

## Process

### 1. **Identify an update to Review**

Run following command to see pull requests for a given update for a selected dist-git branch.
```bash
./review-packit-distgit-update.py <VERSION> <BRANCH>
```

### 2. **Review proposed pull requests**

Production and staging Packit instances opened these pull requests. Also 2 workflows were utilized: propose_downstream and pull_from_upstream.
Make sure that all 4 pull requests are the same. Report any inconsistencies you find.