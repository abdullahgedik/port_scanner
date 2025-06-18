# test_scan.py

from scanner import PortScanner

# python -m http.server 8000
# python cli.py -t localhost -p 8000-8000 -to 1.0 -th 2

if __name__ == "__main__":
    # localhost üzerinde 8000 portunu tarayalım
    scanner = PortScanner(
        target="127.0.0.1",
        start_port=8000,
        end_port=8000,
        timeout=1.0,
        thread_count=2
    )
    scanner.run()
