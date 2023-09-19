import uuid

uid = lambda: uuid.uuid4().hex[:20] #20 char uniqque id

graph_dim = (1224,1224) #(dx,dy)
input_cordinates = (160,90)
output_cordinates = (680,90)
Box_cordinates = (280,80)

signal_y_incr = 40

def _genrate_signal(signal_name, coordinates, signal_uid):
  signal_format = f"""
  <mxCell id="{signal_uid}" value="{signal_name}" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;" parent="1" vertex="1">
    <mxGeometry x="{coordinates[0]}" y="{coordinates[1]}" width="40" height="30" as="geometry" />
  </mxCell>
  """
  return signal_format

def __generate_data(box_name, box_dimensions, xml_signals):
  file_uid = uid()
  etag_uid = uid()
  box_uid = uid()

  xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>

  <mxfile host="Electron" modified="2023-09-17T21:57:35.139Z" agent="5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/20.8.16 Chrome/106.0.5249.199 Electron/21.4.0 Safari/537.36" etag="{etag_uid}" version="20.8.16" type="device">
    <diagram name="Page-1" id="{file_uid}">

      <mxGraphModel dx="{graph_dim[0]}" dy="{graph_dim[1]}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
        <root>
          <mxCell id="0" />
          <mxCell id="1" parent="0" />

          <mxCell id="{box_uid}" value="{box_name}" style="rounded=0;whiteSpace=wrap;html=1;" parent="1" vertex="1">
            <mxGeometry x="{Box_cordinates[0]}" y="{Box_cordinates[1]}" width="{box_dimensions[0]}" height="{box_dimensions[1]}" as="geometry" />
          </mxCell>

          {xml_signals}
              
        </root>
      </mxGraphModel>
    </diagram>
  </mxfile>
  """
  return xml_data

def generate_xml(module_name, input_signals, output_signals, output_filename):
  input_signal_y_incr = 0
  output_signal_y_incr = 0
  
  #box height calcuation
  max_height = max(len(input_signals), len(output_signals))
  box_height = (max_height * signal_y_incr) + 20
  box_dimensions = (320, box_height) #(width,height)

  xml_signals = ""
  box_name = module_name

  for signal in input_signals:
    xml_signals = xml_signals + _genrate_signal(signal[2], (input_cordinates[0], input_cordinates[1]+input_signal_y_incr), uid())
    input_signal_y_incr = input_signal_y_incr + signal_y_incr

  for signal in output_signals:
    xml_signals = xml_signals + _genrate_signal(signal[2], (output_cordinates[0], output_cordinates[1]+output_signal_y_incr), uid())
    output_signal_y_incr = output_signal_y_incr + signal_y_incr

  XML_data = __generate_data(box_name, box_dimensions, xml_signals)

  with open(output_filename, "w") as f:
    f.write(XML_data)

  return None