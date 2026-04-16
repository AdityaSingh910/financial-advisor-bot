Security incident: exposed secret

Summary
- A Groq API key was accidentally committed to `backend/.env` and has been removed from the repository history.
- A backup of the original history was saved to branch `backup-main` on the remote.

Immediate actions (YOU must do these now)
1. Revoke the exposed Groq API key immediately from the provider dashboard and create a new key.
2. Revoke/rotate any other secrets that may have been stored in `backend/.env`.

What I did in the repo
- Removed `backend/.env` from all commits using `git filter-repo`.
- Added `.gitignore` to prevent committing `backend/.env` in the future.
- Committed helper files and force-pushed a cleaned history to `origin`.
- Created remote branch `backup-main` that contains the previous (unrewritten) history.

How collaborators should update their local clones
Option A — easiest (recommended): reclone the repository

    git clone https://github.com/AdityaSingh910/financial-advisor-bot.git

Option B — if you have uncommitted local work you want to preserve

    # fetch cleaned remote
    git fetch origin --prune
    # switch to a new temporary branch and preserve local changes
    git checkout -b my-work-backup
    git stash push -m "wip-backup" || true
    # delete and re-create local main to match remote
    git branch -D main
    git checkout -b main origin/main
    # reapply your stashed work
    git checkout my-work-backup
    git stash pop || true

Notes
- Even though the secret was removed from history, you must rotate/revoke the key because it may have been exposed.
- Do not re-add real secrets to the repository. Use environment variables set on the host, a secrets manager, or GitHub Secrets for CI.
- Consider enabling GitHub Secret Scanning and branch protections to avoid future leaks.

If you want, I can create a short collaborator notice (README or issue) and a follow-up checklist to secure other credentials.
