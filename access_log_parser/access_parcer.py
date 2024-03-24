import tarfile
import re
import json
from collections import defaultdict
import os


def parse_log_line(line):
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    date_pattern = r'\[([^\[\]]+)\]'
    method_pattern = r'"(\w+)\s([^"]+)\sHTTP/\d\.\d"'
    duration_pattern = r'(\d+)$'

    match = re.search(f'{ip_pattern} - - {date_pattern} {method_pattern} \d+ \d+ ".+?" ".+?" {duration_pattern}', line)
    if match:
        ip = match.group(1)
        date = match.group(2)
        method = match.group(3)
        url = match.group(4)
        duration = int(match.group(5))

        return {
            "ip": ip,
            "date": date,
            "method": method,
            "url": url,
            "duration": duration
        }
    else:
        return None


def analyze_log_file(log_file):
    result = {
        "top_ips": defaultdict(int),
        "top_longest": [],
        "total_stat": defaultdict(int),
        "total_requests": 0
    }

    for line in log_file:
        line = line.decode('utf-8')
        entry = parse_log_line(line)
        if entry:
            result["top_ips"][entry["ip"]] += 1
            result["total_stat"][entry["method"]] += 1
            result["total_requests"] += 1
            result["top_longest"].append(entry)

    result["top_ips"] = dict(sorted(result["top_ips"].items(), key=lambda x: x[1], reverse=True)[:3])
    result["top_longest"] = sorted(result["top_longest"], key=lambda x: x["duration"], reverse=True)[:3]

    return result


def main(log_dir):
    if os.path.isfile(log_dir) and log_dir.endswith('.tar.gz'):
        with tarfile.open(log_dir, 'r') as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith('.log'):
                    log_file = tar.extractfile(member)
                    result = analyze_log_file(log_file)
                    output_file = member.name.replace('.log', '_result.json')
                    with open(output_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(json.dumps(result, indent=2))
    elif os.path.isdir(log_dir):
        for file_name in os.listdir(log_dir):
            if file_name.endswith('.tar.gz'):
                file_path = os.path.join(log_dir, file_name)
                with tarfile.open(file_path, 'r') as tar:
                    for member in tar.getmembers():
                        if member.isfile() and member.name.endswith('.log'):
                            log_file = tar.extractfile(member)
                            result = analyze_log_file(log_file)
                            output_file = member.name.replace('.log', '_result.json')
                            with open(output_file, 'w') as f:
                                json.dump(result, f, indent=2)
                            print(json.dumps(result, indent=2))
    else:
        print("Invalid directory or file path")


if __name__ == "__main__":
    log_dir = input("Enter the directory path where the log files are located: ")
    main(log_dir)
