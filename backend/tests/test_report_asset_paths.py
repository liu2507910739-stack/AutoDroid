import unittest

from sqlmodel import Session, SQLModel, create_engine

from backend.api.reports import _normalize_report_asset_path, get_report_detail
from backend.models import TestExecution, TestResult, TestScenario


class ReportAssetPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

        scenario = TestScenario(name="scenario-1")
        self.session.add(scenario)
        self.session.commit()
        self.session.refresh(scenario)

        execution = TestExecution(
            scenario_id=scenario.id,
            scenario_name="scenario-1",
            status="FAIL",
            executor_name="tester",
        )
        self.session.add(execution)
        self.session.commit()
        self.session.refresh(execution)
        self.execution_id = execution.id

    def tearDown(self) -> None:
        self.session.close()

    def test_normalize_report_asset_path_strips_reports_anchor(self):
        self.assertEqual(
            _normalize_report_asset_path("/Users/old/AutoDroid/reports/screenshots/exec_1_step_2.png"),
            "screenshots/exec_1_step_2.png",
        )
        self.assertEqual(
            _normalize_report_asset_path(r"C:\Users\old\AutoDroid\reports\screenshots\exec_1_step_3.png"),
            "screenshots/exec_1_step_3.png",
        )
        self.assertEqual(
            _normalize_report_asset_path("screenshots/exec_1_step_4.png"),
            "screenshots/exec_1_step_4.png",
        )

    def test_report_detail_returns_normalized_screenshot_path(self):
        self.session.add(
            TestResult(
                execution_id=self.execution_id,
                step_name="[case] failed step",
                step_order=1,
                status="FAIL",
                duration=100,
                screenshot_path="/Users/old/AutoDroid/reports/screenshots/exec_9_step_1.png",
                report_display={
                    "display_text": "OCR提取变量 ORDER_ID",
                    "preview_type": "screenshot",
                },
            )
        )
        self.session.commit()

        detail = get_report_detail(self.execution_id, session=self.session)

        self.assertEqual(len(detail.steps), 1)
        self.assertEqual(detail.steps[0].screenshot_path, "screenshots/exec_9_step_1.png")
        self.assertEqual(detail.steps[0].report_display["display_text"], "OCR提取变量 ORDER_ID")
        self.assertEqual(detail.steps[0].report_display["preview_path"], "screenshots/exec_9_step_1.png")


if __name__ == "__main__":
    unittest.main()
