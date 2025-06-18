import argparse
from scanner import PortScanner

def parse_args():
    parser = argparse.ArgumentParser(
        description="Basit TCP port tarayici"
    )
    parser.add_argument(
        "-t", "--target", required=True,
        help="Tarama yapilacak IP adresi veya alan adı"
    )
    parser.add_argument(
        "-p", "--ports", required=True,
        help="Port araliği (örn. 1-1024)"
    )
    parser.add_argument(
        "-to", "--timeout", type=float, default=1.0,
        help="Her port için zaman aşimi süresi (saniye)"
    )
    parser.add_argument(
        "-th", "--threads", type=int, default=10,
        help="Ayni anda çalişacak iş parçaciği sayisi"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    start, end = map(int, args.ports.split('-'))
    scanner = PortScanner(
        target=args.target,
        start_port=start,
        end_port=end,
        timeout=args.timeout,
        thread_count=args.threads
    )
    scanner.run()
