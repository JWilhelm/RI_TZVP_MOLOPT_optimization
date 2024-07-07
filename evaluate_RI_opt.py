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

    last_subdir = os.path.basename(os.path.normpath(dirpath))

    # Find the last occurrence of the line containing "DI/|Emp2|"
    last_line_basis_set_name = False
    for i, line in enumerate(lines):
        if "DI/|Emp2|" in line:
            accuracy = line
        if "OPTIMIZATION STEP NUMBER" in line:
            last_opt_step = int(line.split()[3])
        if last_line_basis_set_name:
            n_set = int(line)
            last_line_basis_set_name = False
        if "RI_opt_basis" in line:            
            last_line_basis_set_name = True

    error = float(accuracy.split()[2])

    if error < min_error*(1-improvement):
       min_error = error
#       print(f"Directory: {dirpath} {error} {n_set}")

       counter = 0
       opt_step = 0
       print_basis = False
       for i, line in enumerate(lines):

         if "OPTIMIZATION STEP NUMBER" in line:
           opt_step = int(line.split()[3])

         if opt_step == last_opt_step:
           line_split = line.split()
           if len(line_split) > 1:
             if line_split[1] == "RI_opt_basis":
               print_basis = True
             if print_basis and counter < 2*n_set + 1:
               counter = counter + 1
               if counter == 1:
                 print("")
                 print("# RI basis set for "+line_split[0]+f", GTH pseudo, relative accuracy of RI-MP2: {error:.1e}")
                 print(line_split[0]+"  RI_"+last_subdir+f"_{error:.1e}")
                 print("   "+str(n_set))
               else:
                 print(str(line), end='')





       
