#!/usr/bin/env bash
# Stamp __version__ in open-prs before autorel tags the release.
# NEXT_VERSION and NEXT_TAG are set by autorel.
set -euo pipefail

: "${NEXT_VERSION:?NEXT_VERSION must be set}"
: "${NEXT_TAG:?NEXT_TAG must be set}"

sed -i "s/^__version__ = .*/__version__ = \"${NEXT_VERSION}\"/" open-prs

git add open-prs
git -c user.name="github-actions[bot]" \
    -c user.email="github-actions[bot]@users.noreply.github.com" \
    commit -m "chore: release ${NEXT_TAG}"
git push origin HEAD:main
