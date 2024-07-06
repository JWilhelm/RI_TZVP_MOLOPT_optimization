import os

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
input_file = os.path.join(os.getcwd(), "RI_opt.inp")

GTH_POTENTIAL_file    = "/pc2/groups/hpc-prf-metdyn/eprop2d1_Jan/02_compile_CP2K/50_Hedin_shift/cp2k/data/GTH_POTENTIALS"
molopt_basis_file     = "/pc2/groups/hpc-prf-metdyn/eprop2d1_Jan/02_compile_CP2K/50_Hedin_shift/cp2k/data/BASIS_MOLOPT"
molopt_ucl_basis_file = "/pc2/groups/hpc-prf-metdyn/eprop2d1_Jan/02_compile_CP2K/50_Hedin_shift/cp2k/data/BASIS_MOLOPT_UCL"

# Ensure the template file exists
if not os.path.exists(input_file):
    print(f"Template file '{input_file}' does not exist. Please create it first.")
    exit(1)

# get all GTH pseudos for each element
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
    directory_name = f"{atomic_number:02d}_{symbol}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    os.chdir(directory_name)
    
    # Loop over the number of RI basis functions from 10 to 99
    for ri_basis in range(10, 100, 5):
        subdirectory_name = f"RI_{ri_basis:02d}"
        if not os.path.exists(subdirectory_name):
            os.makedirs(subdirectory_name)
        
        # Copy the RI_opt.inp file into the new subdirectory
        subdirectory_path = os.path.join(os.getcwd(), subdirectory_name)
        new_file_path = os.path.join(subdirectory_path, 'RI_opt.inp')
        
        with open(input_file, 'r') as template:
            content = template.read()
        
        # Replace the placeholder with the actual spin multiplicity
        content = content.replace("REPLACE_MULTIPLICITY", str(spin_multiplicity))
        content = content.replace("REPLACE_ELEMENT", symbol)
        
        # Write the new content to the new file
        with open(new_file_path, 'w') as new_file:
            new_file.write(content)
    
    # Navigate back to the parent directory
    os.chdir('..')
