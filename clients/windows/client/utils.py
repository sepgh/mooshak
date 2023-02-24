import subprocess
import threading


def popen_and_call(on_exit, on_proc, popen_args, popen_kwargs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    on_exit when the subprocess completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that
    would give to subprocess.Popen.
    """
    def run_in_thread(on_exit, on_proc, popen_args, popen_kwargs):
        proc = subprocess.Popen(*popen_args, **popen_kwargs)
        on_proc(proc)
        proc.wait()
        on_exit()
        return
    thread = threading.Thread(target=run_in_thread, args=(on_exit, on_proc, popen_args, popen_kwargs))
    thread.start()
    # returns immediately after the thread starts
    return thread
