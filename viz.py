import networkx as nx
from csv import DictReader
import matplotlib.pyplot as plt


def main():
    g = make_graph()
    nx.write_gml(g, "author_reviewer.gml")


def make_graph():
    f = open("pr_scrape.csv")
    reader = DictReader(f)
    G = nx.Graph()

    review_relations = {}
    for item in reader:
        key = (item["author"], item["reviewed_by"])
        if key in review_relations:
            review_relations[key] += 1
        else:
            review_relations[key] = 1

    for (author, reviewer), weight in review_relations.items():
        G.add_edge(author, reviewer, weight=weight)
    return G


if __name__ == "__main__":
    main()
