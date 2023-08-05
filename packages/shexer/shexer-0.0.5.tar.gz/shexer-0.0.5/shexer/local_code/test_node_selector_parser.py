from shexer.io.shape_map.node_selector.node_selector_parser import NodeSelectorParser

namespaces_dict = {"http://www.wikidata.org/entity/" : "wd",
                   "http://www.wikidata.org/prop/direct/": "wdt"}
endpoint = "https://query.wikidata.org/sparql"

isolated_node = "<http://algo.es>"
isolated_prefixed_node = "wd:algo"

focus_exp = "{FOCUS wdt:P31 wd:Q5055981}"
sparql_exp = "SPARQL 'select ?p WHERE {?p wd:p31 wd:Q5}'"

parser = NodeSelectorParser(prefix_namespaces_dict=namespaces_dict, endpoint_url=endpoint)

# r = parser.parse_node_selector(isolated_node)
# print(r.raw_selector)
# print(r.get_target_nodes())
# print("------")
#
# r = parser.parse_node_selector(isolated_prefixed_node)
# print(r.raw_selector)
# print(r.get_target_nodes())
# print("------")
#
# r = parser.parse_node_selector(focus_exp)
# print(r.raw_selector)
# print(r.sparql_query_selector)
# print("------")
#
# r = parser.parse_node_selector(sparql_exp)
# print(r.raw_selector)
# print(r.sparql_query_selector)
# print("------")

focus_obj = "{wd:Q5 wd:P31 FOCUS}"
focus_wild = "{_ wd:P31 FOCUS}"

# r = parser.parse_node_selector(focus_obj)
# print(r.raw_selector)
# print(r.sparql_query_selector)
# print("------")

r = parser.parse_node_selector(focus_exp)
# print(r.raw_selector)
# print(r.sparql_query_selector)
# print(str(r.sparql_query_selector))
for an_item in r.get_target_nodes():
    print(an_item)
print("------")

# focus_bad_b = "{wd:Q5 FOCUS _}"
# focus_too_many_focus = "{FOCUS wd:P31 FOCUS}"
# focus_no_focus = "{wd:Q5 wd:P31 wd:Q7}"
# focus_bad_prefix = "{weee:Q5 wd:P31 FOCUS}"
#
# try:
#     r = parser.parse_node_selector(focus_bad_b)
#     # print(r.raw_selector)
#     # print(r.sparql_query_selector)
#     # print("------")
#     raise RuntimeError()
# except BaseException as e:
#     print("Tuuuto bene " + str(e))
#     print("Uyuy")
#
#
# try:
#     r = parser.parse_node_selector(focus_too_many_focus)
#     # print(r.raw_selector)
#     # print(r.sparql_query_selector)
#     # print("------")
#     raise RuntimeError()
# except BaseException as e:
#     print("Tuuuto bene " + str(e))
#
# try:
#     r = parser.parse_node_selector(focus_no_focus)
#     # print(r.raw_selector)
#     # print(r.sparql_query_selector)
#     # print("------")
#     raise RuntimeError()
# except BaseException as e:
#     print("Tuuuto bene " + str(e))
#
# try:
#     r = parser.parse_node_selector(focus_bad_prefix)
#     # print(r.raw_selector)
#     # print(r.sparql_query_selector)
#     # print("------")
#     raise RuntimeError()
# except BaseException as e:
#     print("Tuuuto bene " + str(e))
#
# print("---------------------")
#
# sparql_wrong_keyword = "SPARQL 'select ?p WEHHHHHH {?p wd:p31 wd:Q5}'"
# sparql_wrong_prefix = "SPARQL 'select ?p WHERE {?p wd:p31 wehh:Q5}'"
#
# r = parser.parse_node_selector(sparql_wrong_prefix)
# print(r.raw_selector)
# print(r.sparql_query_selector)
# print("------")