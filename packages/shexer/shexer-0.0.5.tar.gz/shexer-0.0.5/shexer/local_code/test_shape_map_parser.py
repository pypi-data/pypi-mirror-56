from shexer.io.shape_map.shape_map_parser import FixedShapeMapParser, JsonShapeMapParser

namespaces_dict = {"http://wikidata.org/entity/" : "wd"}

raw_json = """
    [
  { "nodeSelector": "<http://data.example/node1>",
    "shapeLabel": "<http://schema.example/Shape2>"
    },
  { "nodeSelector": "<http://data.example/node1>",
    "shapeLabel": "<http://schema.example/Shape2>"
    }
]
"""

raw_fixed = """
#Ignore
<toni>@<Persona>

#Ignore as well
wd:Toni@wd:persona,
{FOCUS wd:algo _}@<Cualquiera>

"""

jparser = JsonShapeMapParser(namespaces_prefix_dict=namespaces_dict,
                             sgraph=None)

map = jparser.parse_shape_map(raw_content=raw_json)

for item in map.yield_items():
    print(item.shape_label, item.node_selector)

print("----")

fparser = FixedShapeMapParser(namespaces_dict,
                              sgraph=None)

map = fparser.parse_shape_map(raw_content=raw_fixed)
for item in map.yield_items():
    print(item.shape_label, item.node_selector)

print("----")
