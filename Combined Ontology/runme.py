#!/usr/bin/env python3

exec(open("./ontology.py").read())
exec(open("./graph.py").read())

add_tuples_from_file("news_input.txt")
onto.save()
g = generate_graph(onto)
graph_draw(g, vertex_text=g.vp.labels, vertex_fill_color = g.vp.colors, vertex_font_size=10, edge_text=g.ep.labels, edge_font_size=10, output_size=(1920,1080), vertex_text_position=0)