import os
import itertools

exp_min_init = 0.15
exp_max_init = 28.0

# List of chemical elements with their atomic numbers, symbols, and spin multiplicities up to element 99
elements = [
    (1, 'H', 2), (2, 'He', 1), (3, 'Li', 2), (4, 'Be', 1), (5, 'B', 2),
    (6, 'C', 3), (7, 'N', 4), (8, 'O', 3), (9, 'F', 2), (10, 'Ne', 1),
    (11, 'Na', 2), (12, 'Mg', 1), (13, 'Al', 2), (14, 'Si', 1), (15, 'P', 4),
    (16, 'S', 3), (17, 'Cl', 2), (18, 'Ar', 1), (19, 'K', 2), (20, 'Ca', 1),
    (21, 'Sc', 2), (22, 'Ti', 3), (23, 'V', 4), (24, 'Cr', 7), (25, 'Mn', 6),
    (26, 'Fe', 5), (27, 'Co', 4), (28, 'Ni', 3), (29, 'Cu', 2), (30, 'Zn', 1),
    (31, 'Ga', 2), (32, 'Ge', 1), (33, 'As', 4), (34, 'Se', 3), (35, 'Br', 2),
    (36, 'Kr', 1), (37, 'Rb', 2), (38, 'Sr', 1), (39, 'Y', 2), (40, 'Zr', 3),
    (41, 'Nb', 2), (42, 'Mo', 7), (43, 'Tc', 6), (44, 'Ru', 5), (45, 'Rh', 4),
    (46, 'Pd', 3), (47, 'Ag', 2), (48, 'Cd', 1), (49, 'In', 2), (50, 'Sn', 1),
    (51, 'Sb', 2), (52, 'Te', 3), (53, 'I', 2), (54, 'Xe', 1), (55, 'Cs', 2),
    (56, 'Ba', 1), (57, 'La', 2), (58, 'Ce', 1), (59, 'Pr', 4), (60, 'Nd', 5),
    (61, 'Pm', 6), (62, 'Sm', 7), (63, 'Eu', 8), (64, 'Gd', 9), (65, 'Tb', 8),
    (66, 'Dy', 7), (67, 'Ho', 6), (68, 'Er', 5), (69, 'Tm', 4), (70, 'Yb', 3),
    (71, 'Lu', 2), (72, 'Hf', 3), (73, 'Ta', 2), (74, 'W', 5), (75, 'Re', 6),
    (76, 'Os', 5), (77, 'Ir', 4), (78, 'Pt', 3), (79, 'Au', 2), (80, 'Hg', 1),
    (81, 'Tl', 2), (82, 'Pb', 1), (83, 'Bi', 4), (84, 'Po', 3), (85, 'At', 2),
    (86, 'Rn', 1), (87, 'Fr', 2), (88, 'Ra', 1), (89, 'Ac', 2), (90, 'Th', 3),
    (91, 'Pa', 4), (92, 'U', 5), (93, 'Np', 6), (94, 'Pu', 7), (95, 'Am', 8),
    (96, 'Cm', 9), (97, 'Bk', 8), (98, 'Cf', 7), (99, 'Es', 6)
]

# Template for RI_opt.inp
input_file        = os.path.join(os.getcwd(), "RI_opt.inp")
RI_def2_TZVP_file = os.path.join(os.getcwd(), "BASIS_RI_def2-TZVPP-RIFIT")
data_dir = "/pc2/groups/hpc-prf-metdyn/eprop2d1_Jan/02_compile_CP2K/50_Hedin_shift/cp2k/data/"

GTH_POTENTIAL_file    = data_dir+"GTH_POTENTIALS"
molopt_basis_file     = data_dir+"BASIS_MOLOPT"
molopt_ucl_basis_file = data_dir+"BASIS_MOLOPT_UCL"

####################### get all GTH pseudos for each element #########################################
with open(GTH_POTENTIAL_file, 'r') as file:
    data = file.read()
lines = data.splitlines()
gth_potentials = []

# Loop through each line to find PBE GTH potentials
for line in lines:
    if "GTH-PBE-q" in line and not "old" in line:
        parts = line.split()
        element = parts[0]
        potential = parts[1]
        gth_potentials.append((element, potential))
        print(element, potential)

# Create directories for each element and navigate into each one
for atomic_number, symbol, spin_multiplicity in elements:

    if(atomic_number < 34 or atomic_number > 34):
      continue

    directory_name = f"{atomic_number:02d}_{symbol}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    os.chdir(directory_name)

    ####################### get RI-def2_TZVP basis set for the element ##############################
    # Open and read the file
    with open(RI_def2_TZVP_file, 'r') as file_RI_def2_TZVP:
        lines = file_RI_def2_TZVP.readlines()
    
    # Initialize variables
    exp_RI_def2_TZVP = [[0 for _ in range(12)] for _ in range(12)]
    parsing = False
    n_l = [0,0,0,0,0,0,0]
    
    # Iterate through each line in the file
    for line in lines:
        line = line.strip()
    
        # Check for the start of the element's basis set
        if line.startswith(symbol):
            parsing = True
            continue
    
        # Stop parsing when the next element is encountered
        if parsing and line and line[0].isalpha() and not line.startswith(symbol):
            break
    
        # Skip comments and empty lines
        if line.startswith("#") or not line:
            continue
    
        # Parse basis function lines
        if parsing:
            parts = line.split()

            if len(parts) == 5:  
                angular_momentum = int(parts[2])
                n_l[angular_momentum] = n_l[angular_momentum] + 1
            if len(parts) == 2:
                exponent = float(parts[0])
                if exponent > exp_min_init and exponent < exp_max_init:
                   exp_RI_def2_TZVP[angular_momentum][n_l[angular_momentum]-1] = exponent
   
    # Loop over the number of RI basis functions in the basis
    for N_RI in range(10, 150, 5):

        if N_RI < 100:
           subdirectory_name = f"RI_0{N_RI:02d}"
        else:
           subdirectory_name = f"RI_{N_RI:02d}"
        if not os.path.exists(subdirectory_name):
            os.makedirs(subdirectory_name)

        # Generate all possible 7-tuples
        for s in range(n_l[0]+1):
         for p in range(n_l[1]+1):
          for d in range(n_l[2]+1):
           for f in range(n_l[3]+1):
            for g in range(n_l[4]+1):
             for h in range(n_l[5]+1):
              for i in range (n_l[6]+1):
               n_tot = s + 3*p + 5*d + 7*f + 9*g + 11*h + 13*i
               if n_tot != N_RI:
                 continue
               print(s,p,d,f,g,h,i,N_RI)

               for element_gth_potential in gth_potentials:

                 if element_gth_potential[0] != symbol:
                   continue

                 subsubdir_name = element_gth_potential[1]+f"_{N_RI}_{s}_{p}_{d}_{f}_{g}_{h}_{i}"

                 # Copy the RI_opt.inp file into the new subdirectory
                 subdirectory_path = os.path.join(os.getcwd(), subdirectory_name+"/"+subsubdir_name)
                 if not os.path.exists(subdirectory_path):
                     os.makedirs(subdirectory_path)

                 tailored_input_file = os.path.join(subdirectory_path, 'RI_opt.inp')
                 
                 with open(input_file, 'r') as template:
                     content = template.read()

                 # Replace the placeholder with the actual spin multiplicity
                 content = content.replace("REPLACE_MULTIPLICITY", str(spin_multiplicity))
                 content = content.replace("REPLACE_ELEMENT", symbol)
                 content = content.replace("REPLACE_POTENTIAL", element_gth_potential[1])
                 
                 # Write the new content to the new file
                 with open(tailored_input_file, 'w') as new_file:
                     new_file.write(content)
 
                 print("you write that file")
 
                 initial_RI_basis_file = os.path.join(subdirectory_path, 'INITIAL_RI_BASIS')  
                 with open(initial_RI_basis_file, 'w') as new_file:
                   new_file.write("RI_initial")
                   new_file.write(str(s+p+d+f+g+h+i))
                   for i_s in range(s):
                      new_file.write("1 0 0 1 1")
                      exp = exp_RI_def2_TZVP[0][n_l[0]-i_s]
                      new_file.write(str(exp)+"  1.0")
#                   for i_p in range(p):
#                   for i_d in range(d):
#                   for i_f in range(f):
#                   for i_g in range(g):
#                   for i_h in range(h):
#                   for i_i in range(i):
  
    
    # Navigate back to the parent directory
    os.chdir('..')
