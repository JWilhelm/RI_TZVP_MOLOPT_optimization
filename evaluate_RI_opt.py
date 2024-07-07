import os

improvement = 0.5

root_dir = os.getcwd()  # Set root directory to the current directory

# Collect all directories to process
directories_to_process = []

for dirpath, _, filenames in os.walk(root_dir):
    if "cp2k.out" in filenames:
        directories_to_process.append(dirpath)

# Sort directories alphabetically
directories_to_process.sort()

min_error = 100.0

for dirpath in directories_to_process:
    file_path = os.path.join(dirpath, "cp2k.out")
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the last occurrence of the line containing "DI/|Emp2|"
    for i, line in enumerate(lines):
        if "DI/|Emp2|" in line:
            accuracy = line
            
    error = float(accuracy.split()[2])

    if error < min_error*(1-improvement):
       min_error = error
       print(f"Directory: {dirpath} {error}")

