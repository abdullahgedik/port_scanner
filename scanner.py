import socket
import threading
import queue

# Thread-safe storage for scan results
RESULT_LOCK = threading.Lock()
results = []

class PortScanner:
    def __init__(self, target, start_port, end_port, timeout=1.0, thread_count=10):
        """
        :param target: IP address or hostname to scan
        :param start_port: First port in the scan range
        :param end_port: Last port in the scan range
        :param timeout: Timeout for each connection attempt (in seconds)
        :param thread_count: Number of concurrent threads
        """
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.thread_count = thread_count
        self.work_queue = queue.Queue()

    def run(self):
        """Başlaici metot: Hedefin doğrulanmasi, iş kuyruğunun oluşturulmasi,
        iş parçaciklarinin başlatilmasi ve sonuçlarin gösterilmesi işlemlerini yürütür."""
        # Hedef doğrulama
        try:
            self.target = socket.gethostbyname(self.target)
        except socket.gaierror as e:
            print(f"Hedef çözümlemesi başarısız: {e}")
            return

        # Port listesini kuyruğa ekle
        for port in range(self.start_port, self.end_port + 1):
            self.work_queue.put(port)

        print(f"Scanning {self.target} [{self.start_port}-{self.end_port}] with timeout={self.timeout}s using {self.thread_count} threads...")

        # İş parçacıklarını başlat
        threads = []
        for _ in range(self.thread_count):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)

        # Tüm işlerin bitmesini bekle
        self.work_queue.join()

        # Sonuçları yazdır
        open_ports = [port for port, status in results if status == "OPEN"]
        for port, status in sorted(results):
            print(f"Port {port}: {status}")
        print(f"Tarama tamamlandı: {self.work_queue.qsize()} port tarandi, {len(open_ports)} açik port bulundu.")

    def worker(self):
        """Her iş parçaciği tarafindan çaliştirilacak metot: Kuyruktan port numarasi çekip tarama yapar."""
        while True:
            try:
                port = self.work_queue.get_nowait()
            except queue.Empty:
                break

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            try:
                code = sock.connect_ex((self.target, port))
                status = "OPEN" if code == 0 else "CLOSED"
            except Exception:
                status = "ERROR"
            finally:
                sock.close()

            with RESULT_LOCK:
                results.append((port, status))

            self.work_queue.task_done()
