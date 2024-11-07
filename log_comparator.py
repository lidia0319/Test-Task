import re
from datetime import datetime

# Function to load log entries from a file
def load_log(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Function to parse individual log entries
def parse_log_entry(log_entry):
    # Regex to capture date, operation type (created, modified, deleted), and the file path
    log_pattern = r"(\d+-\d+-\d+ \d+:\d+:\d+:\d+),(\d+) - (File \w+): (.+)"
    match = re.match(log_pattern, log_entry)
    if match:
        date_str, ms, operation, file_path = match.groups()
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date_obj, operation, file_path.strip()
    return None

# Function to compare file operation logs with synchronization logs
def compare_logs(file_operations, sync_operations, result_log):
    # Parse the logs
    file_ops = [parse_log_entry(entry) for entry in file_operations if parse_log_entry(entry)]
    sync_ops = [parse_log_entry(entry) for entry in sync_operations if parse_log_entry(entry)]

    # Map operations by type of file (Source or Replica)
    source_file_operations = [op for op in file_ops if 'Source' in op[2]]
    replica_file_operations = [op for op in file_ops if 'Replica' in op[2]]

    sync_file_operations = {op[2]: op for op in sync_ops}

    errors_found = False

    # Check synchronization of the Source folder
    for date, operation, file in source_file_operations:
        expected_op = 'copied' if operation == 'File created' else operation.lower()
        expected_op = 'removed' if operation == 'File deleted' else expected_op
        sync_key = f"Replica/{file.split('/')[-1]}"
        if sync_key not in sync_file_operations:
            result_log.write(f"[Error] Missing operation for {sync_key} in sync_operations\n")
            errors_found = True
        else:
            sync_op_time, sync_op, sync_file = sync_file_operations[sync_key]
            if expected_op not in sync_op.lower():
                result_log.write(f"[Error] Incorrect operation for {sync_key}: Expected '{expected_op}', found '{sync_op.lower()}'\n")
                errors_found = True

    # Check synchronization of the Replica folder
    for date, operation, file in replica_file_operations:
        if operation == 'File created' or operation == 'File modified':
            expected_op = 'removed'
            sync_key = f"Replica/{file.split('/')[-1]}"
            if sync_key not in sync_file_operations:
                result_log.write(f"[Error] Missing operation for {sync_key} in sync_operations\n")
                errors_found = True
            else:
                sync_op_time, sync_op, sync_file = sync_file_operations[sync_key]
                if expected_op not in sync_op.lower():
                    result_log.write(f"[Error] Incorrect operation for {sync_key}: Expected 'removed', found '{sync_op.lower()}'\n")
                    errors_found = True
    
    if not errors_found:
        result_log.write("Everything was synchronized correctly. No errors found.\n")

# Main function to run the test
def run_test(file_operations_path, sync_operations_path, result_log_path):
    file_operations = load_log(file_operations_path)
    sync_operations = load_log(sync_operations_path)

    with open(result_log_path, 'w') as result_log:
        compare_logs(file_operations, sync_operations, result_log)
    print(f"Test completed. Check the result log file at {result_log_path}.")

# Paths to the log files
file_operations_path = "file_operations.log"
sync_operations_path = "sync_operations.log"
result_log_path = "test_results.log"

# Run the test
run_test(file_operations_path, sync_operations_path, result_log_path)
