import os

def process_log_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8', errors='replace') as infile:
        lines = infile.readlines()
    
    error_lines = []
    cap_lines = []
    
    for i in range(len(lines)):
        if lines[i].strip().startswith("r("):
            error_lines.append(str(i + 8))
        if " cap " in lines[i] or " capture " in lines[i]:
            cap_lines.append(str(i + 8))
    
    if error_lines:
        error_message = f"ATTENTION: RUNNING YOUR do-file PRODUCES ERRORS, see line(s) {', '.join(error_lines)}.\n"
    elif cap_lines:
        error_message = f"ATTENTION: It appears as if you use a cap or capture command. We cannot verify, whether your script runs without errors, see line(s) {', '.join(cap_lines)}.\n"
    else:
        error_message = "Your do-file runs without errors.\n"
    
    intro_lines = [
        "\n",
        "This is the log-file generated when running your do-file with the 95%-sample of the SOEP data.\n",
        "\n",
        "All output has been censored. Commented lines, and passages that produce an error message are still visible.\n",
        "\n",
        error_message,
        '\n'
    ]
    
    result_lines = intro_lines + lines[:24]  # Add intro lines and keep the first 24 lines as is
    
    for i in range(24, len(lines)):
        if lines[i].startswith(". *") or lines[i].strip().startswith("r(") or \
           (i + 1 < len(lines) and lines[i + 1].strip().startswith("r(")) or \
           (i + 2 < len(lines) and lines[i + 2].strip().startswith("r(")):
            result_lines.append(lines[i])
        else:
            result_lines.append('\n')  # Blank the line
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(result_lines)
    print(f"Created censored log file: {output_path}")

def move_log_file_to_lib(log_file_path):
    lib_dir = os.path.join(os.path.dirname(log_file_path), 'lib')
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir)
    new_path = os.path.join(lib_dir, os.path.basename(log_file_path))
    os.rename(log_file_path, new_path)
    print(f"Moved {log_file_path} to {new_path}")

def main():
    log_dir = 'ManyDaughters_PC_AnalysisPackage_95/log'
    censored_dir = os.path.join(log_dir, 'censored')
    os.makedirs(censored_dir, exist_ok=True)
    
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            input_path = os.path.join(log_dir, filename)
            output_filename = filename.replace('.log', '_95%.log')
            output_path = os.path.join(censored_dir, output_filename)
            process_log_file(input_path, output_path)
            move_log_file_to_lib(input_path)

if __name__ == "__main__":
    main()