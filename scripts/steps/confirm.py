from scripts.steps.base import Step, register

@register
class ConfirmStep(Step):

    Y_REGEX = r"(^$)|(^(y|Y)$)|yes|Yes|YES"
    N_REGEX = r"(^(n|N)$)|no|No|NO"

    def run(self) -> bool:
        import re
        res = input()
        ym = re.match(self.Y_REGEX, res)
        nm = re.match(self.N_REGEX, res)
        if ym:
            if nm:
                raise ValueError()
            return True
        else:
            return False

    def get_step_detail(self) -> str:
        return f"Waiting to confirm."

    @classmethod
    def step_name(cls):
        return "confirm"
