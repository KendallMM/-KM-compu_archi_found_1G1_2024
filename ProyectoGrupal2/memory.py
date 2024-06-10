class Instruction:
    def __init__(self, opcode, rs=0, rt=0, rd=0, imm=0):
        self.opcode = opcode
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.imm = imm

    def __repr__(self):
        return f"Instruction(opcode='{self.opcode}', rs={self.rs}, rt={self.rt}, rd={self.rd}, imm={self.imm})"

class Memory:
    def __init__(self):
        self.combined_memory = [
            # Instructions for loading matrix A and B elements into registers
            Instruction('LOAD', rs=0, rt=1, imm=0),   # Load a11 to R0
            Instruction('LOAD', rs=0, rt=2, imm=1),   # Load a12 to R1
            Instruction('LOAD', rs=0, rt=3, imm=2),   # Load a13 to R2
            Instruction('LOAD', rs=0, rt=4, imm=3),   # Load a21 to R3
            Instruction('LOAD', rs=0, rt=5, imm=4),   # Load a22 to R4
            Instruction('LOAD', rs=0, rt=6, imm=5),   # Load a23 to R5
            Instruction('LOAD', rs=0, rt=7, imm=6),   # Load a31 to R6
            Instruction('LOAD', rs=0, rt=8, imm=7),   # Load a32 to R7
            Instruction('LOAD', rs=0, rt=9, imm=8),   # Load a33 to R8
            Instruction('LOAD', rs=0, rt=10, imm=9),  # Load b11 to R9
            Instruction('LOAD', rs=0, rt=11, imm=10), # Load b12 to R10
            Instruction('LOAD', rs=0, rt=12, imm=11), # Load b13 to R11
            Instruction('LOAD', rs=0, rt=13, imm=12), # Load b21 to R12
            Instruction('LOAD', rs=0, rt=14, imm=13), # Load b22 to R13
            Instruction('LOAD', rs=0, rt=15, imm=14), # Load b23 to R14
            Instruction('LOAD', rs=0, rt=16, imm=15), # Load b31 to R15
            Instruction('LOAD', rs=0, rt=17, imm=16), # Load b32 to R16
            Instruction('LOAD', rs=0, rt=18, imm=17), # Load b33 to R17

            # Instructions for matrix multiplication
            # C[0][0] = a11*b11 + a12*b21 + a13*b31
            Instruction('MUL', rs=1, rt=10, rd=19),  # R19 = R1 * R10 (a11 * b11)
            Instruction('MUL', rs=2, rt=13, rd=20),  # R20 = R2 * R13 (a12 * b21)
            Instruction('MUL', rs=3, rt=16, rd=21),  # R21 = R3 * R16 (a13 * b31)
            Instruction('ADD', rs=19, rt=20, rd=22), # R22 = R19 + R20 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=23), # R23 = R22 + R21 (C[0][0])

            # C[0][1] = a11*b12 + a12*b22 + a13*b32
            Instruction('MUL', rs=1, rt=11, rd=19),  # R24 = R1 * R11 (a11 * b12)
            Instruction('MUL', rs=2, rt=14, rd=20),  # R25 = R2 * R14 (a12 * b22)
            Instruction('MUL', rs=3, rt=17, rd=21),  # R26 = R3 * R17 (a13 * b32)
            Instruction('ADD', rs=19, rt=20, rd=22), # R27 = R24 + R25 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=24), # R28 = R27 + R26 (C[0][1])

            # C[0][2] = a11*b13 + a12*b23 + a13*b33
            Instruction('MUL', rs=1, rt=12, rd=19),  # R29 = R1 * R12 (a11 * b13)
            Instruction('MUL', rs=2, rt=15, rd=20),  # R30 = R2 * R15 (a12 * b23)
            Instruction('MUL', rs=3, rt=18, rd=21),  # R31 = R3 * R18 (a13 * b33)
            Instruction('ADD', rs=19, rt=20, rd=22), # R32 = R29 + R30 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=25), # R33 = R32 + R31 (C[0][2])

            # C[1][0] = a21*b11 + a22*b21 + a23*b31
            Instruction('MUL', rs=4, rt=10, rd=19),  # R34 = R4 * R10 (a21 * b11)
            Instruction('MUL', rs=5, rt=13, rd=20),  # R35 = R5 * R13 (a22 * b21)
            Instruction('MUL', rs=6, rt=16, rd=21),  # R36 = R6 * R16 (a23 * b31)
            Instruction('ADD', rs=19, rt=20, rd=22), # R37 = R34 + R35 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=26), # R38 = R37 + R36 (C[1][0])

            # C[1][1] = a21*b12 + a22*b22 + a23*b32
            Instruction('MUL', rs=4, rt=11, rd=19),  # R39 = R4 * R11 (a21 * b12)
            Instruction('MUL', rs=5, rt=14, rd=29),  # R40 = R5 * R14 (a22 * b22)
            Instruction('MUL', rs=6, rt=17, rd=21),  # R41 = R6 * R17 (a23 * b32)
            Instruction('ADD', rs=19, rt=29, rd=22), # R42 = R39 + R40 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=27), # R43 = R42 + R41 (C[1][1])

            # C[1][2] = a21*b13 + a22*b23 + a23*b33
            Instruction('MUL', rs=4, rt=12, rd=19), # R44 = R4 * R12 (a21 * b13)
            Instruction('MUL', rs=5, rt=15, rd=20), # R45 = R5 * R15 (a22 * b23)
            Instruction('MUL', rs=6, rt=18, rd=21), # R46 = R6 * R18 (a23 * b33)
            Instruction('ADD', rs=19, rt=20, rd=22), # R47 = R44 + R45 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=28), # R48 = R47 + R46 (C[1][2])
            # C[2][0] = a31*b11 + a32*b21 + a33*b31
            Instruction('MUL', rs=7, rt=10, rd=19),  # R49 = R7 * R10 (a31 * b11)
            Instruction('MUL', rs=8, rt=13, rd=20),  # R50 = R8 * R13 (a32 * b21)
            Instruction('MUL', rs=9, rt=16, rd=21),  # R51 = R9 * R16 (a33 * b31)
            Instruction('ADD', rs=19, rt=20, rd=22), # R52 = R49 + R50 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=29), # R53 = R52 + R51 (C[2][0])

            # C[2][1] = a31*b12 + a32*b22 + a33*b32
            Instruction('MUL', rs=7, rt=11, rd=19),  # R54 = R7 * R11 (a31 * b12)
            Instruction('MUL', rs=8, rt=14, rd=20),  # R55 = R8 * R14 (a32 * b22)
            Instruction('MUL', rs=9, rt=17, rd=21),  # R56 = R9 * R17 (a33 * b32)
            Instruction('ADD', rs=19, rt=20, rd=22), # R57 = R54 + R55 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=30), # R58 = R57 + R56 (C[2][1])

            # C[2][2] = a31*b13 + a32*b23 + a33*b33
            Instruction('MUL', rs=7, rt=12, rd=19),  # R59 = R7 * R12 (a31 * b13)
            Instruction('MUL', rs=8, rt=15, rd=20),  # R60 = R8 * R15 (a32 * b23)
            Instruction('MUL', rs=9, rt=18, rd=21),  # R61 = R9 * R18 (a33 * b33)
            Instruction('ADD', rs=19, rt=20, rd=22), # R62 = R59 + R60 (partial sum)
            Instruction('ADD', rs=22, rt=21, rd=31), # R63 = R62 + R61 (C[2][2])

            # Store results back to memory
            Instruction('STORE', rs=0, rt=23, imm=18), # Store C[0][0] in memory[18]
            Instruction('STORE', rs=0, rt=24, imm=19), # Store C[0][1] in memory[19]
            Instruction('STORE', rs=0, rt=25, imm=20), # Store C[0][2] in memory[20]
            Instruction('STORE', rs=0, rt=26, imm=21), # Store C[1][0] in memory[21]
            Instruction('STORE', rs=0, rt=27, imm=22), # Store C[1][1] in memory[22]
            Instruction('STORE', rs=0, rt=28, imm=23), # Store C[1][2] in memory[23]
            Instruction('STORE', rs=0, rt=29, imm=24), # Store C[2][0] in memory[24]
            Instruction('STORE', rs=0, rt=30, imm=25), # Store C[2][1] in memory[25]
            Instruction('STORE', rs=0, rt=31, imm=26), # Store C[2][2] in memory[26]

            # Data for matrices A and B
            1, 2, 3, 4, 5, 6, 7, 8, 9,   # Matrix A
            10, 11, 12, 13, 14, 15, 16, 17, 18 # Matrix B
        ]



