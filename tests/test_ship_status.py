"""Post-merge badge is ship-pipeline status, not “any workflow succeeded.”"""

from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone
from importlib.util import module_from_spec, spec_from_loader
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_loader = SourceFileLoader("open_prs", str(ROOT / "open-prs"))
_spec = spec_from_loader(_loader.name, _loader)
assert _spec is not None
mod = module_from_spec(_spec)
_loader.exec_module(mod)

REPO = {"name": "types", "owner": {"login": "logfoxai"}}


def suite(name: str, conclusion: str | None, updated_at: str | None = "2026-08-20T19:00:00Z") -> dict:
    return {
        "conclusion": conclusion,
        "updatedAt": updated_at,
        "workflowRun": {
            "workflow": {"name": name},
            "databaseId": 1,
            "runNumber": 9,
            "url": "https://example.test/run/1",
        },
    }


def status(suites: list[dict]):
    return mod._workflow_status_from_rollup(suites, REPO)


class ShipWorkflowNameTests(unittest.TestCase):
    def test_release_deploy_publish_are_ship(self):
        for name in ("release", "Release", "deploy", "npm-publish", "Publish package"):
            self.assertTrue(mod._is_ship_workflow(name), name)

    def test_ci_and_unrelated_names_are_not_ship(self):
        for name in ("CI", "lint", "test", None, ""):
            self.assertFalse(mod._is_ship_workflow(name), name)


class WorkflowStatusFromShipPipelineTests(unittest.TestCase):
    def test_ci_only_success_is_not_a_release(self):
        ws, failures = status([suite("CI", "SUCCESS")])
        self.assertIsNone(ws)
        self.assertEqual(failures, [])

    def test_ci_only_failure_is_not_a_release_failure(self):
        ws, failures = status([suite("CI", "FAILURE")])
        self.assertIsNone(ws)
        self.assertEqual(failures, [])

    def test_release_success_is_success(self):
        ws, failures = status([suite("CI", "SUCCESS"), suite("release", "SUCCESS")])
        self.assertEqual(ws["status"], "success")
        self.assertEqual(failures, [])

    def test_publish_and_deploy_names_count_as_ship(self):
        for name in ("publish", "deploy"):
            ws, _ = status([suite(name, "SUCCESS")])
            self.assertEqual(ws["status"], "success", name)

    def test_release_failure_is_failure(self):
        ws, failures = status(
            [suite("CI", "SUCCESS"), suite("release", "FAILURE")],
        )
        self.assertEqual(ws["status"], "failure")
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["workflow"], "release")

    def test_release_in_progress_is_running(self):
        ws, _ = status(
            [suite("CI", "SUCCESS"), suite("release", None)],
        )
        self.assertEqual(ws["status"], "running")

    def test_skipped_release_only_is_not_a_release(self):
        ws, _ = status([suite("release", "SKIPPED")])
        self.assertIsNone(ws)

    def test_success_plus_skipped_ship_is_success(self):
        ws, _ = status([suite("release", "SUCCESS"), suite("publish", "SKIPPED")])
        self.assertEqual(ws["status"], "success")

    def test_no_suites_is_not_a_release(self):
        ws, _ = status([])
        self.assertIsNone(ws)

    def test_newer_successful_release_wins_over_stale_failure(self):
        ws, failures = status([
            suite("release", "FAILURE", "2026-08-20T18:00:00Z"),
            suite("release", "SUCCESS", "2026-08-20T19:00:00Z"),
        ])
        self.assertEqual(ws["status"], "success")
        self.assertEqual(failures, [])

    def test_newer_failed_release_wins_over_stale_success(self):
        ws, failures = status([
            suite("release", "SUCCESS", "2026-08-20T18:00:00Z"),
            suite("release", "FAILURE", "2026-08-20T19:00:00Z"),
        ])
        self.assertEqual(ws["status"], "failure")
        self.assertEqual(len(failures), 1)

    def test_timed_out_release_includes_failure_details(self):
        ws, failures = status([suite("release", "TIMED_OUT")])
        self.assertEqual(ws["status"], "failure")
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["workflow"], "release")

    def test_newer_skipped_release_does_not_hide_prior_failure(self):
        ws, failures = status([
            suite("release", "FAILURE", "2026-08-20T18:00:00Z"),
            suite("release", "SKIPPED", "2026-08-20T19:00:00Z"),
        ])
        self.assertIsNotNone(ws)
        self.assertEqual(ws["status"], "failure")
        self.assertEqual(len(failures), 1)


class ResolveDeploymentBadgeTests(unittest.TestCase):
    def test_no_ship_status_stays_merged(self):
        now = datetime.now(timezone.utc)
        pr = {
            "url": "https://example.test/pr/1",
            "merged_at": (now - timedelta(minutes=2)).isoformat(),
        }
        shown = mod._resolve_deployment(pr, None, now, {})
        self.assertEqual(shown["deploy"], "merged")

    def test_ship_success_badge_key_is_success(self):
        now = datetime.now(timezone.utc)
        pr = {
            "url": "https://example.test/pr/2",
            "merged_at": (now - timedelta(minutes=2)).isoformat(),
        }
        shown = mod._resolve_deployment(
            pr,
            {"status": "success", "completed_at": now - timedelta(minutes=1)},
            now,
            {},
        )
        self.assertEqual(shown["deploy"], "success")

    def test_success_badge_says_released_not_deployed(self):
        self.assertIn("released", mod.DEPLOY_BADGES["success"])
        self.assertNotIn("deployed", mod.DEPLOY_BADGES["success"])

    def test_running_badge_says_releasing(self):
        self.assertIn("releasing", mod.DEPLOY_BADGES["running"])
        self.assertNotIn("deploying", mod.DEPLOY_BADGES["running"])


if __name__ == "__main__":
    unittest.main()
