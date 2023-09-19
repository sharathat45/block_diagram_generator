import xml_generate 
import extract_mod 

INPUT_FILE  = "/Users/sharathhebburshivakumar/Downloads/purdue/projects/block_diagram_generator/VX_alu_unit.sv"
OUTPUT_FILE = "/Users/sharathhebburshivakumar/Downloads/purdue/projects/block_diagram_generator/VX_alu_unit.drawio.xml"
INTERFACE_PATH = "/Users/sharathhebburshivakumar/Downloads/purdue/projects/block_diagram_generator/interfaces/"


def main():
  (module_name, input_signals,output_signals) = extract_mod.extract_module_signals(INPUT_FILE, INTERFACE_PATH)

  print(module_name) 
  print("Input Signals:")
  for signal in input_signals:
    print(signal)

  print("\nOutput Signals:")
  for signal in output_signals:
    print(signal)

  xml_generate.generate_xml(module_name, input_signals,output_signals, OUTPUT_FILE)

if __name__ == "__main__":
  main()
