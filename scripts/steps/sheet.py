from scripts.steps.base import Step, register

@register
class SheetStep(Step):

    def run(self) -> bool:
        from sheets.mapper import create_sheet
        create_sheet(self.config)
        return True

    def get_step_detail(self) -> str:
        return f"Creating/Modifying a sheet at {self.config['path']}"

    @classmethod
    def step_name(cls):
        return "sheet"
