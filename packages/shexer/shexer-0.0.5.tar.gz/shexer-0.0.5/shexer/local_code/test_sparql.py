
"""
https://www.wikidata.org/wiki/Q5055981  --> concejo de asturias

PREFIX wd: <http://www.wikidata.org/entity/>
 PREFIX wdt: <http://www.wikidata.org/prop/direct/>

"""

from shexer.io.sparql.query import query_endpoint_single_variable

sparql_query = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?p WHERE { ?p wdt:P31 wd:Q5055981}

"""

another_sp_query = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT ?f WHERE {?f <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q5055981> . }"""

result = query_endpoint_single_variable(endpoint_url="https://query.wikidata.org/sparql",
                                        str_query=another_sp_query,
                                        variable_id="f")
print(result)