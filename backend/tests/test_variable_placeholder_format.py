import unittest

from backend.schemas import GlobalVariableCreate, GlobalVariableRead, Step, TestCaseStepWrite
from backend.utils.variable_render import normalize_variable_placeholders, render_step_data


class VariablePlaceholderFormatTests(unittest.TestCase):
    def test_normalize_variable_placeholders_removes_inner_spaces(self):
        self.assertEqual(
            normalize_variable_placeholders("hello {{ NAME }} / {{PRICE}} / {{ ORDER_ID_1 }}"),
            "hello {{NAME}} / {{PRICE}} / {{ORDER_ID_1}}",
        )

    def test_render_keeps_legacy_spaced_placeholder_compatible(self):
        self.assertEqual(render_step_data("hello {{ NAME }}", {"NAME": "AutoDroid"}), "hello AutoDroid")

    def test_step_schema_normalizes_legacy_placeholder_fields(self):
        step = Step(action="input", selector="{{ FIELD }}", value="{{ VALUE }}")

        self.assertEqual(step.selector, "{{FIELD}}")
        self.assertEqual(step.value, "{{VALUE}}")

    def test_standard_step_schema_normalizes_args_and_platform_selector(self):
        step = TestCaseStepWrite(
            action="input",
            args={"text": "{{ NAME }}"},
            platform_overrides={"android": {"selector": "{{ FIELD }}", "by": "text"}},
        )

        self.assertEqual(step.args["text"], "{{NAME}}")
        self.assertEqual(step.platform_overrides.android.selector, "{{FIELD}}")

    def test_global_variable_value_is_normalized(self):
        item = GlobalVariableCreate(key="TOKEN", value="Bearer {{ TOKEN_RAW }}")

        self.assertEqual(item.value, "Bearer {{TOKEN_RAW}}")

    def test_global_variable_read_value_is_normalized_for_existing_data(self):
        item = GlobalVariableRead(id=1, env_id=1, key="TOKEN", value="Bearer {{ TOKEN_RAW }}", created_at=None)

        self.assertEqual(item.value, "Bearer {{TOKEN_RAW}}")


if __name__ == "__main__":
    unittest.main()
