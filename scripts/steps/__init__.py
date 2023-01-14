from .download import DownloadStep
from .require import RequireStep
from .sheet import SheetStep
from .command import CommandStep
from .confirm import ConfirmStep
from .base import STEPS

def run_steps(step_list: list):
    for i, step in enumerate(step_list):
        print(f"=== STEP #{i} ===")
        for step_name, step_class in STEPS.items():
            if step_name == step["type"]:
                step_obj = step_class(step)
                if "message" in step:
                    print(step["message"])
                print(step_obj.get_step_detail())
                step_obj.run()
                break
