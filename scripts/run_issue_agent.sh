#!/usr/bin/env bash
set -euo pipefail

ISSUE_NUMBER="${1:?usage: scripts/run_issue_agent.sh <issue-number>}"
REPO_DIR="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$REPO_DIR"

if [[ "$(git branch --show-current)" == "main" ]]; then
  echo "Refusing to run the autonomous agent directly on main." >&2
  exit 2
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Refusing to start with a dirty worktree." >&2
  exit 2
fi

git fetch origin main
BRANCH="agent/issue-${ISSUE_NUMBER}"
git switch -c "$BRANCH" "origin/main"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
ISSUE_FILE="$TMP_DIR/issue.json"
gh issue view "$ISSUE_NUMBER" --json number,title,body,url > "$ISSUE_FILE"

python - "$ISSUE_FILE" <<'PY' > "$TMP_DIR/prompt.txt"
import json, pathlib, sys
issue = json.loads(pathlib.Path(sys.argv[1]).read_text())
print("Work only on GitHub Issue #{}: {}".format(issue["number"], issue["title"]))
print("Issue URL: {}".format(issue["url"]))
print("\nISSUE BODY\n----------")
print(issue.get("body") or "(no body)")
print("\nOPERATING CONTRACT\n-------------------")
print("Implement only safe L0/L1 work. Do not deploy production, change auth/authorization, destroy data, expose credentials, or perform other L2/L3 side effects. Produce a tested implementation and leave high-impact work as a proposal.")
print("Create a concise summary of changes, tests, risks, rollback, and approval level in your final output.")
PY

export SUITE_WORKSPACE="$REPO_DIR"
uv run python main.py "$(cat "$TMP_DIR/prompt.txt")" | tee "$TMP_DIR/agent-output.txt"

python -m compileall -q .
python evals/run_local.py > "$TMP_DIR/evals.txt"

git status --short
if [[ -z "$(git status --porcelain)" ]]; then
  echo "Agent produced no repository changes; no PR will be opened."
  exit 0
fi

git add -A
git commit -m "agent: implement issue #${ISSUE_NUMBER}"
git push --set-upstream origin "$BRANCH"

PR_BODY="## Autonomous implementation for #${ISSUE_NUMBER}\n\nThis draft PR was produced by the guarded issue-agent runner.\n\n### Verification\n- Python compile check passed\n- Approval-policy evaluation suite passed\n\n### Safety\nThe runner started from main on an `agent/issue-*` branch and does not merge or deploy production changes. High-impact work remains subject to the repository approval policy."
gh pr create --draft --base main --head "$BRANCH" --title "agent: implement #${ISSUE_NUMBER}" --body "$PR_BODY"
