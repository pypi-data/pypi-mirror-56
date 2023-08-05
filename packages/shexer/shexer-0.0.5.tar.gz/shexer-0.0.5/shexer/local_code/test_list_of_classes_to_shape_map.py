
from shexer.utils.translators.list_of_classes_to_shape_map import ListOfClassesToShapeMap
from shexer.model.graph.endpoint_sgraph import EndpointSGraph
from shexer.utils.dict import reverse_keys_and_values

sgraph = EndpointSGraph(endpoint_url="https://query.wikidata.org/bigdata/namespace/wdq/sparql")

namespaces_dict = {"http://www.wikidata.org/entity/" : "wd",
                   "http://www.wikidata.org/prop/direct/": "wdt"}

lts = ListOfClassesToShapeMap(sgraph=sgraph,
                              prefix_namespaces_dict=reverse_keys_and_values(namespaces_dict))

target_classes = ["http://www.wikidata.org/entity/Q44062313", "http://www.wikidata.org/entity/Q54856362"]

result = lts.str_class_list_to_shape_map_sparql_selectors(str_list=target_classes,
                                                          instantiation_property="http://www.wikidata.org/prop/direct/P1344")

for an_item in result.yield_items():
    print("------------")
    print(an_item.shape_label)
    print(an_item.node_selector.get_target_nodes())
print("Done!")