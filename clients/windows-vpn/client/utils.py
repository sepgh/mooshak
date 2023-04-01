import subprocess
import threading
import time

from termcolor import cprint


def popen_and_call(on_proc, popen_args, popen_kwargs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    on_exit when the subprocess completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that
    would give to subprocess.Popen.
    """

    def run_in_thread(on_proc, popen_args, popen_kwargs):
        proc = subprocess.Popen(*popen_args, **popen_kwargs)
        on_proc(proc)
        proc.wait()
        return

    thread = threading.Thread(target=run_in_thread, args=(on_exit, on_proc, popen_args, popen_kwargs), daemon=True)
    thread.start()
    # returns immediately after the thread starts
    return thread


def retry_on_false(number_of_retries, func, args=None, kwargs=None):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    retry = 0
    output = False
    while retry < number_of_retries and output is False:
        if retry != 0:
            time.sleep(2)
            cprint("Retrying ...", "yellow")
        output = func(*args, **kwargs)
        retry += 1
    return output


def log_popen_pipe(p, stdfile, err=False):
    mark = "ERR> " if err else "LOG> "
    with open("mylog.txt", "w") as f:

        while p.poll() is None:
            f.write(mark + stdfile.readline())
            f.flush()

        # Write the rest from the buffer
        f.write(stdfile.read())


def print_popen_pipe(name, p, stdfile, err=False, color="yellow"):
    mark = f"[{name}] ERR> " if err else f"[{name}] LOG> "
    while p.poll() is None:
        cprint(mark + stdfile.readline().decode("utf-8"), color)


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
