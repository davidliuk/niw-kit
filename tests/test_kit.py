"""End-to-end checks for tools/kit.py on synthetic cases and the blank template."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import kit
from tools.build_support import BuildError

KIT_ROOT = Path(__file__).resolve().parents[1]


def _tools_available() -> bool:
    try:
        for tool in ("pandoc", "typst", "pdfinfo", "pdftoppm", "pdfunite"):
            kit.resolve_executable(tool)
    except BuildError:
        return False
    return True


def write_case(root: Path, *, petition: str, phrase: str = "Build reliable tools.") -> kit.Case:
    (root / "workproduct").mkdir(parents=True)
    (root / "data").mkdir()
    (root / "workproduct/01_Petition.md").write_text(petition, encoding="utf-8")
    (root / "workproduct/05_Index.md").write_text(
        "# Exhibit List\n\n<!-- EXHIBIT_TABLES -->\n", encoding="utf-8"
    )
    (root / "case.json").write_text(json.dumps({
        "schema_version": 1,
        "case_id": "synthetic",
        "applicant_name": "Alex Example",
        "manifest": "data/manifest.json",
        "registry": "data/registry.json",
        "petition": "workproduct/01_Petition.md",
        "exhibit_index_source": "workproduct/05_Index.md",
        "locked_phrases": [{
            "name": "endeavor", "text": phrase, "files": ["workproduct/01_Petition.md"],
        }],
    }), encoding="utf-8")
    artifact = lambda path, order: {
        "path": path, "display_title": path, "artifact_class": "FILING_FACING",
        "include_in_review_packet": True, "clean_copy_ruleset": "FILING_V2",
        "packet_order": order,
    }
    (root / "data/manifest.json").write_text(json.dumps({
        "schema_version": 1,
        "artifacts": [artifact("workproduct/01_Petition.md", 10),
                      artifact("workproduct/05_Index.md", 20)],
    }), encoding="utf-8")
    (root / "data/registry.json").write_text(json.dumps({
        "schema_version": 1,
        "series": [{"id": "B", "title": "Degree", "order": 1, "exhibits": [
            {"id": "B-1", "title": "Diploma", "order": 1,
             "file_path": "evidence/B/B-1_Diploma.pdf", "source": "University",
             "date_display": "2025", "supports": "Advanced degree"},
            {"id": "B-2", "title": "Transcript", "order": 2,
             "file_path": "evidence/B/B-2_Transcript.pdf", "source": "University",
             "date_display": "2025"},
        ]}],
    }), encoding="utf-8")
    return kit.load_case(root)


class CheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)

    def test_clean_draft_passes_with_missing_payload_warnings(self) -> None:
        case = write_case(self.directory, petition=(
            "Build reliable tools. Degree [Exhibits B-1–B-2].\n"
        ))
        report = kit.check_case(case, final=False)
        self.assertEqual(report.errors, [])
        self.assertTrue(any("missing payload" in item for item in report.warnings))

    def test_final_check_blocks_missing_payloads_and_placeholders(self) -> None:
        case = write_case(self.directory, petition=(
            "Build reliable tools. {{NAME}} [Exhibits B-1, B-2].\n"
        ))
        errors = kit.check_case(case, final=True).errors
        self.assertTrue(any("unfilled placeholders" in item for item in errors))
        self.assertTrue(any("missing payload" in item for item in errors))

    def test_guide_comments_are_not_scanned(self) -> None:
        case = write_case(self.directory, petition=(
            "Build reliable tools. <!-- GUIDE: replace {{NAME}} TODO --> "
            "[Exhibits B-1, B-2].\n"
        ))
        report = kit.check_case(case, final=False)
        self.assertEqual(report.errors, [])
        self.assertFalse(any(
            "unfilled placeholders" in item or "draft marker" in item
            for item in report.warnings
        ))

    def test_undefined_and_uncited_exhibits_fail(self) -> None:
        case = write_case(self.directory, petition="Build reliable tools. [Exhibit B-9].\n")
        errors = kit.check_case(case, final=False).errors
        self.assertTrue(any("undefined exhibit B-9" in item for item in errors))
        self.assertTrue(any("uncited exhibit B-1" in item for item in errors))

    def test_locked_phrase_drift_fails(self) -> None:
        case = write_case(self.directory, petition="Build tools. [Exhibits B-1, B-2].\n")
        errors = kit.check_case(case, final=False).errors
        self.assertTrue(any("drifted" in item for item in errors))

    def test_private_identifier_fails(self) -> None:
        case = write_case(self.directory, petition=(
            "Build reliable tools. A-number A123456789 [Exhibits B-1, B-2].\n"
        ))
        errors = kit.check_case(case, final=False).errors
        self.assertTrue(any("A-number" in item for item in errors))


@unittest.skipUnless(_tools_available(), "pandoc, typst, and poppler are required")
class BuildTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)

    def test_stubs_online_and_freeze(self) -> None:
        case = write_case(self.directory, petition=(
            "# Petition\n\nBuild reliable tools. [Exhibits B-1–B-2].\n"
        ))
        self.assertEqual(len(kit.build_stubs(case)), 2)
        final_errors = kit.check_case(case, final=True).errors
        self.assertTrue(any("generated placeholder" in item for item in final_errors))

        out = kit.build_online(case, draft=True)
        manifest = json.loads((out / "upload_manifest.json").read_text())
        names = [item["file"] for item in manifest["files"]]
        self.assertEqual(names[:2], ["00_Petition_Letter.pdf", "01_Exhibit_Index.pdf"])
        self.assertTrue(all(item["bytes"] <= case.upload_limit_bytes for item in manifest["files"]))
        self.assertTrue(all(item["placeholder"] for item in manifest["files"][2:]))

        binder = kit.build_binder(case)
        self.assertEqual(kit.pdf_page_count(binder), 4)  # two covers + two stubs

        kit.freeze(case, "test")
        self.assertEqual(kit.verify_frozen(case), [])
        (case.root / "evidence/B/B-1_Diploma.pdf").write_bytes(b"changed")
        self.assertEqual(kit.verify_frozen(case), ["changed evidence/B/B-1_Diploma.pdf"])


class TemplateTests(unittest.TestCase):
    def test_blank_template_passes_draft_check(self) -> None:
        case = kit.load_case(KIT_ROOT / "case-template")
        report = kit.check_case(case, final=False)
        self.assertEqual(report.errors, [], "\n".join(report.errors))

    def test_blank_template_fails_final_check(self) -> None:
        case = kit.load_case(KIT_ROOT / "case-template")
        self.assertTrue(kit.check_case(case, final=True).errors)


if __name__ == "__main__":
    unittest.main()
