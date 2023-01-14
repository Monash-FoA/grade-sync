from scripts.steps.base import Step, register

@register
class DownloadStep(Step):

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.is_folder = config.get("folder", False)

    def run(self) -> bool:
        import gdown
        if self.is_folder:
            gdown.download_folder(url=self.config["source"], output=self.config["dest"])
        else:
            gdown.download(url=self.config["source"], output=self.config["dest"])
        return True

    def get_step_detail(self) -> str:
        return f"Downloading {'folder' if self.is_folder else 'file'}."

    @classmethod
    def step_name(cls):
        return "download"
