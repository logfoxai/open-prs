#!/usr/bin/env bash
# Bake NEXT_VERSION into open-prs for the release tag. Does not push to main —
# autorel tags this commit; brew/curl install from the tag tarball.
set -euo pipefail

: "${NEXT_VERSION:?NEXT_VERSION must be set}"
: "${NEXT_TAG:?NEXT_TAG must be set}"

sed -i "s/^__version__ = .*/__version__ = \"${NEXT_VERSION}\"/" open-prs

git add open-prs
git -c user.name="github-actions[bot]" \
    -c user.email="github-actions[bot]@users.noreply.github.com" \
    commit -m "chore: release ${NEXT_TAG}"
