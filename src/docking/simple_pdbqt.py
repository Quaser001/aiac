import os

def get_atom_type(element):
    """Maps element to AutoDock atom type."""
    element = element.capitalize()
    # AutoDock 4 atom types: C, A (aromatic C), N, O, S, P, F, Cl, Br, I, Mg, Na, K, Zn, Ca, Fe, Mn
    if element in ['C', 'N', 'O', 'S', 'H', 'P', 'F', 'Cl', 'Br', 'I', 'Mg', 'Zn', 'Fe', 'Ca']:
        return element
    return 'C' # Fallback to Carbon for unknown to prevent Vina crash

def get_center_of_mass(pdbqt_path):
    """Calculates geometric center of PDBQT atoms."""
    x_sum, y_sum, z_sum = 0.0, 0.0, 0.0
    count = 0
    try:
        with open(pdbqt_path, 'r') as f:
            for line in f:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    try:
                        # PDBQT: X(30-38), Y(38-46), Z(46-54)
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        x_sum += x
                        y_sum += y
                        z_sum += z
                        count += 1
                    except ValueError:
                        continue
        if count > 0:
            return (x_sum/count, y_sum/count, z_sum/count)
    except Exception:
        pass
    return (0.0, 0.0, 0.0)

def pdb_to_pdbqt(pdb_path, output_path):
    """
    Converts PDB to PDBQT by adding partial charge (0.00) and atom type.
    Keeps coordinates intact.
    """
    with open(pdb_path, 'r') as f_in, open(output_path, 'w') as f_out:
        for line in f_in:
            if not (line.startswith("ATOM") or line.startswith("HETATM") or line.startswith("TER") or line.startswith("END")):
                continue
                
            if line.startswith("ATOM") or line.startswith("HETATM"):
                # PDB Format: http://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM
                # We need to append charge and type.
                # Vina parses strictly. PDBQT is PDB + Charge (cols 71-76) + Type (78-79)
                
                # Strip newlines
                line = line.rstrip()
                
                # Parse PDB columns
                # Serial(7-11), Name(13-16), ResName(18-20), Chain(22), ResSeq(23-26), X(31-38), Y(39-46), Z(47-54)
                # Notes: 1-based indexing in spec, 0-based in python strip()
                try:
                    serial = int(line[6:11])
                    name = line[12:16]
                    resName = line[17:20]
                    chain = line[21]
                    resSeq = int(line[22:26])
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                except ValueError:
                    continue # Skip malformed lines

                # Determine Element/Type
                element = line[76:78].strip()
                if not element:
                     element = name.strip()[0]
                atom_type = get_atom_type(element)

                # Reconstruct PDBQT line
                # ATOM  12345  NAME RES C 1234    X.xxx   Y.yyy   Z.zzz  1.00  0.00    0.000 A 
                # Specs: 
                # 1-6 Rec, 7-11 Ser, 13-16 Name, 18-20 Res, 22 Ch, 23-26 Seq
                # 31-38 X, 39-46 Y, 47-54 Z
                # 55-60 Occ, 61-66 Temp
                # 71-76 Charge, 78-79 Type
                
                # We use default Occ=1.00, Temp=0.00, Charge=0.000
                
                pdbqt_line = f"ATOM  {serial:5d} {name:<4} {resName:<3} {chain}{resSeq:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00    {0.000:6.3f} {atom_type}\n"
                f_out.write(pdbqt_line)
            
            elif line.startswith("TER") or line.startswith("END"):
                f_out.write(line + "\n")
            # Ignored: HEADER, TITLE, REMARK, etc.

    return True

def sdf_to_pdbqt(sdf_path, output_path):
    """
    Parses simple SDF (V2000) and writes rigid PDBQT.
    Supports only basic atoms and coords.
    """
    atoms = []
    
    with open(sdf_path, 'r') as f:
        lines = f.readlines()
        
    start_idx = -1
    end_idx = -1
    
    # Find Atom Block (Look for V2000)
    for i, line in enumerate(lines):
        if "V2000" in line:
            start_idx = i + 1
            # Parse Counts
            try:
                parts = line.split()
                num_atoms = int(parts[0])
                num_bonds = int(parts[1])
                end_idx = start_idx + num_atoms
            except:
                return False
            break
            
    if start_idx == -1 or end_idx == -1:
        return False
        
    # extract atoms
    # x y z symbol
    for i in range(start_idx, end_idx):
        if i >= len(lines): break
        line = lines[i]
        parts = line.split()
        if len(parts) >= 4:
            x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
            sym = parts[3]
            atoms.append({'x': x, 'y': y, 'z': z, 'sym': sym})

    if not atoms:
        return False

    with open(output_path, 'w') as f:
        f.write("ROOT\n")
        for idx, atom in enumerate(atoms):
            # Format as HETATM
            # HETATM    1  C   LIG     1       0.000   0.000   0.000  1.00  0.00     0.000 C
            atom_type = get_atom_type(atom['sym'])
            
            # Formatter
            # HETATM (6)
            # Serial (5)
            # Space (1)
            # Name (4) -> Sym + ID
            # ResName (3) -> LIG
            # Chain (1) -> ' '
            # ResSeq (4) -> 1
            # ICode (1) -> ' '
            # X (8.3)
            # Y (8.3)
            # Z (8.3)
            # Occ (6.2) -> 1.00
            # Temp (6.2) -> 0.00
            # Charge (6.3) -> 0.000 (Corrected width)
            # Type (Space + Type)
            
            name = f"{atom['sym']}{idx+1}"[:4].ljust(4)
            # Fixed width strict formatting:
            # HETATM ser:5 name:4 res:3 C seq:4    X...
            line = f"HETATM{idx+1:5d} {name} LIG     1    {atom['x']:8.3f}{atom['y']:8.3f}{atom['z']:8.3f}  1.00  0.00    {0.000:6.3f} {atom_type}\n"
            f.write(line)
            
        f.write("ENDROOT\n")
        f.write("TORSDOF 0\n")
        
    return True
