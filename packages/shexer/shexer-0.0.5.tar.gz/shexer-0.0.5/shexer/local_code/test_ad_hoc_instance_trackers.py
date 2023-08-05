from shexer.core.instances.mappings.shape_map_instance_tracker import ShapeMapInstanceTracker
from shexer.core.instances.instance_tracker import InstanceTracker
from shexer.core.instances.mix.mixed_instance_tracker import MixedInstanceTracker
from shexer.io.shape_map.shape_map_parser import FixedShapeMapParser
from shexer.model.graph.rdflib_sgraph import RdflibSgraph
from shexer.model.graph.endpoint_sgraph import EndpointSGraph
from shexer.io.graph.yielder.remote.sgraph_from_selectors_triple_yielder import SgraphFromSelectorsTripleYielder
from shexer.consts import WIKIDATA_INSTACE_OF


sgraph = RdflibSgraph(source_file="files\\example_turtle.ttl", format="turtle")
sgraph = EndpointSGraph(endpoint_url="https://query.wikidata.org/bigdata/namespace/wdq/sparql")

namespaces_dict = {"http://www.wikidata.org/entity/" : "wd",
                   "http://www.perceive.net/schemas/relationship/" : "rel",
                   "http://www.wikidata.org/prop/direct/" : "wdt"}

sm_parser = FixedShapeMapParser(namespaces_prefix_dict=namespaces_dict,
                                sgraph=sgraph)


raw_fixed = """
#Ignore
{FOCUS wdt:P1344 wd:Q44062313}@<Hackatonero>


#Ignore as well

"""

map = sm_parser.parse_shape_map(raw_content=raw_fixed)

selectors_triples_yielder = SgraphFromSelectorsTripleYielder(shape_map=map,
                                                             depth=1,
                                                             classes_at_last_level=True,
                                                             instantiation_property=WIKIDATA_INSTACE_OF)

tracker_node = ShapeMapInstanceTracker(shape_map=map)
# result = tracker_node.track_instances()
# print(result)
print("Done node!")

tracker_instances = InstanceTracker(track_hierarchies=False,
                                    all_classes_mode=True,
                                    triples_yielder=selectors_triples_yielder,
                                    instantiation_property=WIKIDATA_INSTACE_OF,
                                    target_classes=None)
# result = tracker_instances.track_instances()
# print(result)
print("Done instances!")

mixed_tracker = MixedInstanceTracker([tracker_node, tracker_instances])
result = mixed_tracker.track_instances()
print(result)



# tracker_instance = InstanceTracker


print("Done!")
