from shexer.shaper import Shaper
from shexer.consts import NT


target_classes = [
    "http://www.wikidata.org/entity/Q11448906",
]
output_file = "shaper_example.shex"
input_nt_file = "files\\selected_awards.nt"

shaper = Shaper(target_classes=target_classes,
                graph_file_input=input_nt_file,
                instantiation_property="http://www.wikidata.org/prop/direct/P31",
                input_format=NT)  # Default rdf:type

shaper.shex_graph(output_file=output_file,
                  aceptance_threshold=0.1)

print("Done!")

