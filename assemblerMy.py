def convertBinToHex(bin_str):
    hex_str = ""
    bin_to_hex = {
        "0000": "0", "0001": "1", "0010": "2", "0011": "3",
        "0100": "4", "0101": "5", "0110": "6", "0111": "7",
        "1000": "8", "1001": "9", "1010": "A", "1011": "B",
        "1100": "C", "1101": "D", "1110": "E", "1111": "F"
    }
    
    # Process the binary string in chunks of 4 bits
    for i in range(0, len(bin_str), 4):
        chunk = bin_str[i:i+4]
        hex_str += bin_to_hex.get(chunk, "Invalid")
    
    return hex_str

def checkInstruction(inst):
    instruction_map = {
        "lw": "0001", "sw": "0101", "bne": "0100",
        "beq": "0011", "addi": "0010", "jmp": "0110",
        "nop": "0111", 
    }
    return instruction_map.get(inst, "Invalid instruction")

def checkFunction(func):
    instruction_map = {
        "add": "000", "sub": "001", "and": "010", "or": "011",
        "srl": "111", "slt": "101", "sll": "110", "nor": "100"
    }
    return instruction_map.get(func, "Invalid instruction")

def checkRegister(reg):
    register_map = {
        "$r0": "00000", "$r1": "00001", "$r2": "00010", "$r3": "00011",
        "$r4": "00100", "$r5": "00101", "$r6": "00110", "$r7": "00111",
        "$r8": "01000", "$r9": "01001", "$r10": "01010", "$r11": "01011",
        "$r12": "01100", "$r13": "01101", "$r14": "01110", "$r15": "01111"
    }
    return register_map.get(reg, "Invalid register")

def decimalToBinary(num, bits):
    if num < 0:
        num = (1 << bits) + num
    return bin(num)[2:].zfill(bits)

# Main processing
with open("inputs", "r") as readf, open("outputs", "w") as writef:
    writef.write("v2.0 raw\n")

    for line in readf:
        splitted = line.strip().split()

        if splitted[0] in ["add", "sub", "and", "or", "nor", "slt"]:
            opcode = "0000"
            func = checkFunction(splitted[0])
            rd = checkRegister(splitted[1])
            rs = checkRegister(splitted[2])
            rt = checkRegister(splitted[3])
            shamt = "00"
            binary_instruction = opcode + rs + rt + rd + shamt + func
        
        elif splitted[0] in ["srl", "sll"]:
            opcode = '0000'
            func = checkFunction(splitted[0])
            rt = checkRegister(splitted[1])
            rd = checkRegister(splitted[2])
            shamt = decimalToBinary(int(splitted[3]), 2) 
            binary_instruction = opcode + '00000' + rt + rd + shamt + func

        elif splitted[0] in ["lw", "sw", "beq", "bne", "addi"]:
            opcode = checkInstruction(splitted[0])
            rs = checkRegister(splitted[1])
            rt = checkRegister(splitted[2])
            immediate = decimalToBinary(int(splitted[3]), 10)  # Use 10 bits for immediate
            binary_instruction = opcode + rs + rt + immediate

        elif splitted[0] == "jmp":
            opcode = checkInstruction(splitted[0])
            address = decimalToBinary(int(splitted[1]), 20)  # Use 20 bits for address
            binary_instruction = opcode + address

        else:
            binary_instruction = "Invalid instruction"

        hex_instruction = convertBinToHex(binary_instruction)
        writef.write(hex_instruction + "\n")
readf.close()
writef.close()