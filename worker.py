import socket
from scanner import RESULT_LOCK, results

def worker(work_queue, target, timeout):
    while not work_queue.empty():
        port = work_queue.get()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        code = sock.connect_ex((target, port))
        status = "OPEN" if code == 0 else "CLOSED"
        sock.close()
        with RESULT_LOCK:
            results.append((port, status))
        work_queue.task_done()
