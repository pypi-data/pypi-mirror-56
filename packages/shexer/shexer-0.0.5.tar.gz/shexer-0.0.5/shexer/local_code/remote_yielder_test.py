from shexer.io.graph.yielder.rdflib_triple_yielder import RdflibTripleYielder
from shexer.consts import RDF_XML


yielder = RdflibTripleYielder(source="http://xmlns.com/foaf/spec/20140114.rdf",
                              input_format=RDF_XML,
                              allow_untyped_numbers=True)

for a_triple in yielder.yield_triples(parse_namespaces=True):
    print(a_triple[0])
    print(a_triple[1])
    print(a_triple[2])
    print("----------")