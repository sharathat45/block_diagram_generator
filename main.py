import re
from os import path

INPUT_FILE  = "/Users/sharathhebburshivakumar/Downloads/purdue/projects/block_diagram_generator/VX_alu_unit.sv"
OUTPUT_FILE = "/Users/sharathhebburshivakumar/Downloads/purdue/projects/block_diagram_generator/VX_alu_unit.drawio.xml"
INTERFACE_PATH = "/Users/sharathhebburshivakumar/Downloads/purdue/projects/block_diagram_generator/interfaces/"

# Define a list to store input and output signals
input_signals = []
output_signals = []

def extract_interface_signals(interface_name, interface_module):
  interface_path = path.join(INTERFACE_PATH, interface_name+".sv")
  interface_signals = {}
  extract_if_module_flag = False

  # Open and read the VX_alu_req_if interface file
  with open(interface_path, 'r') as if_file:
    if_content = if_file.readlines()
    
    for line in if_content:
      line = line.strip() 
      
      if line.startswith("wire") or line.startswith("reg"):
        signal_list = line.split()
        if len(signal_list)==2:
          signal_name = signal_list[1].replace(';', '')
          signal_length = None
          signal_type = signal_list[0] 
        else:
          signal_name = signal_list[2].replace(';', '')
          signal_length = signal_list[1]
          signal_type = signal_list[0]

        interface_signals[signal_name] = (signal_type, signal_length, f"{interface_name}.{signal_name}")

      elif f"modport {interface_module}" in line:
        extract_if_module_flag = True

      elif extract_if_module_flag == True:
        if line.startswith("input"):
          signal_name = line.split()[1].replace(',', '')
          input_signals.append(interface_signals[signal_name])
        elif line.startswith("output"):
          signal_name = line.split()[1].replace(',', '')
          input_signals.append(interface_signals[signal_name])
        elif line.startswith(");"):  
          extract_if_module_flag = False

  return None

def extract_module_signals(module_file_path):

  # Regular expressions to match input and output declarations
  input_pattern = r'\binput\b\s+(wire|reg)?\s*(\[[^\]]+\])?\s*(\w*)'
  output_pattern = r'\binput\b\s+(wire|reg)?\s*(\[[^\]]+\])?\s*(\w*)'
  interface_pattern = r'\b(VX_\w+_if)\b.(\w+)'
  module_name_pattern = r'module\s+(\w+)\s+'

  # input_pattern = r'\binput\b\s+(wire|reg)?\s*((?:\[\d+:\d+\])+\s*)?\s*(\w*)' for 2dim mod interface

  # Open and read the SystemVerilog file
  with open(module_file_path, 'r') as sv_file:
    sv_content = sv_file.read()

    # Find all input signals and store them in the input_signals list
    input_matches = re.finditer(input_pattern, sv_content)
    for match in input_matches:
        signal_type = match.group(1)
        signal_length = match.group(2)
        signal_name = match.group(3)
        input_signals.append((signal_type, signal_length, signal_name))

    # Find all output signals and store them in the output_signals list
    output_matches = re.finditer(output_pattern, sv_content)
    for match in output_matches:
        signal_type = match.group(1)
        signal_length = match.group(2)
        signal_name = match.group(3)
        output_signals.append((signal_type, signal_length, signal_name))

    # Find all signals from interface and append them in the list
    interface_matches = re.finditer(interface_pattern, sv_content)
    interface_matches = tuple(interface_matches)
    for match in interface_matches:
      interface_name = match.group(1)
      interface_module = match.group(2)
      extract_interface_signals(interface_name, interface_module)

    module_name_match = re.search(module_name_pattern, sv_content)
    if module_name_match:
        module_name = module_name_match.group(1)
    else:
        module_name = "Module name not found"

  return (module_name, input_signals, output_signals)

def main():
  (module_name, input_signals,output_signals) = extract_module_signals(INPUT_FILE)

  print(module_name) 
  print("Input Signals:")
  for signal in input_signals:
      print(signal)

  print("\nOutput Signals:")
  for signal in output_signals:
      print(signal)

if __name__ == "__main__":
  main()