from scripts.steps.base import Step, register

@register
class CommandStep(Step):

    def run(self) -> bool:
        import subprocess
        # TODO: venv
        p = subprocess.Popen(self.config["command"])
        ret = p.wait()
        return ret == 0

    def get_step_detail(self) -> str:
        return f"Running command\n\t{self.config['command']}"

    @classmethod
    def step_name(cls):
        return "command"
