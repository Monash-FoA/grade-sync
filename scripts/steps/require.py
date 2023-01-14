from scripts.steps.base import Step, register

@register
class RequireStep(Step):

    def run(self) -> bool:
        import time
        import os

        self.running = True
        # See if the last modified on the file is within time.
        path = self.config["path"]
        if os.path.exists(path):
            ftime = os.path.getmtime(path)
            ctime = time.time()
            if ctime - ftime < 60 * 60 * self.config.get("lifetime", 0):
                return True
        else:
            if "wait_message" in self.config:
                print(self.config["wait_message"])
            while self.running:
                time.sleep(1)
                if os.path.exists(path):
                    break
            return True

        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class NotifyEventHandler(FileSystemEventHandler):
            def on_created(this, event):
                self.running = False
            def on_modified(this, event):
                self.running = False

        observer = Observer()
        observer.schedule(NotifyEventHandler(), path)
        observer.start()
        if "wait_message" in self.config:
            print(self.config["wait_message"])
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        return True

    def get_step_detail(self) -> str:
        return f"Waiting for you to download a file to {self.config['path']}"

    @classmethod
    def step_name(cls):
        return "require"
