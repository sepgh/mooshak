import threading

from termcolor import cprint


class VerbosePrinter:

    def __init__(self, process, name, color="red", out=True, err=True):
        self.process = process
        self.stopped = False
        self.name = name
        self.color = color
        self._out = out
        self._err = err

    def print_if_not_empty(self, txt: str, _type):
        txt = txt.strip()
        if txt == "":
            return
        cprint(f"[{self.name}] {_type} > " + txt, color=self.color, on_color="on_white")

    def start(self):
        def run_out_thread():
            while not self.stopped:
                self.print_if_not_empty(self.process.stdout.readline().decode("utf-8"), "O")

        def run_err_thread():
            while not self.stopped:
                self.print_if_not_empty(self.process.stderr.readline().decode("utf-8"), "E")

        if self._out:
            thread1 = threading.Thread(target=run_out_thread, daemon=False)
            thread1.start()

        if self._err:
            thread2 = threading.Thread(target=run_err_thread, daemon=False)
            thread2.start()

    def stop(self):
        self.stopped = True
