# Contributing

This repository follows a PR-style workflow to mirror professional team delivery.

## Branching Strategy

Create branches from `main` using one of these prefixes:
- `feature/<scope>`
- `fix/<scope>`
- `docs/<scope>`
- `chore/<scope>`
- `refactor/<scope>`
- `test/<scope>`

Examples:
- `feature/ai-policy-ranking`
- `fix/jwt-token-expiry`
- `docs/architecture-update`

## Commit Convention

Use Conventional Commits:
- `feat: add advisor confidence scoring`
- `fix: handle invalid token on /api/auth/me`
- `docs: add azure app service runbook`
- `test: add regression test for invalid password`
- `refactor: move query logic to repositories`
- `chore: add seed data for demo account`

## Recommended Workflow

1. Sync main branch.

```bash
git checkout main
git pull origin main
```

2. Create a focused branch.

```bash
git checkout -b feature/my-change
```

3. Make small commits as milestones.

```bash
git add .
git commit -m "feat: <small completed scope>"
```

4. Push branch and open a PR.

```bash
git push -u origin feature/my-change
```

5. Complete PR checklist using `.github/PULL_REQUEST_TEMPLATE.md`.

6. Merge with a merge commit to preserve branch history.

```bash
git checkout main
git merge --no-ff feature/my-change -m "merge: integrate <scope>"
git push origin main
```

## Code Review Expectations

- Verify auth, validation, and secret handling.
- Confirm tests cover new behavior.
- Check docs are updated for API or workflow changes.
- Ensure no unrelated refactors are mixed into one PR.

## Issue Workflow

Use GitHub Issues to track bugs and enhancements:
- Create issue with expected vs actual behavior.
- Reference issue in PR with `Closes #<id>`.
- Add final verification note before closing.
