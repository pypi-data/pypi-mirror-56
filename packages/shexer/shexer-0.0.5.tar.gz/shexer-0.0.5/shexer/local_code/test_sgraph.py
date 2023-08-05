from shexer.model.graph.endpoint_sgraph import EndpointSGraph
from shexer.model.graph.rdflib_sgraph import RdflibSgraph
from rdflib.graph import Graph


# sgraph = EndpointSGraph(endpoint_url="https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sgraph = EndpointSGraph(endpoint_url="https://query.wikidata.org/sparql")

for a_triple in sgraph.yield_class_triples_of_an_s(target_node="http://www.wikidata.org/entity/Q51602692",
                                                   instantiation_property="http://www.wikidata.org/prop/direct/P31"):
    print(a_triple)


for a_triple in sgraph.yield_p_o_triples_of_target_nodes(target_nodes=["http://www.wikidata.org/entity/Q29"],
                                                         instantiation_property="http://www.wikidata.org/prop/direct/P31",
                                                         already_visited=None,
                                                         depth=1,
                                                         classes_at_last_level=True,
                                                         strict_syntax_with_uri_corners=False):
    print(a_triple)

print("Done!")

rdflib_graph = Graph()
rdflib_graph.parse("files\\example_turtle.ttl", format="turtle")

sgraph = RdflibSgraph(rdflib_graph=rdflib_graph)
result = sgraph.query_single_variable(str_query="select ?p where {?s ?p ?o .}",
                                      variable_id="?p")

print(result)
for a_triple in sgraph.yield_p_o_triples_of_target_nodes(target_nodes=["http://www.perceive.net/schemas/relationship/foo"],
                                                         depth=1,
                                                         classes_at_last_level=True,
                                                         instantiation_property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                                         strict_syntax_with_uri_corners=False):
    print(a_triple)
print("Done!")
