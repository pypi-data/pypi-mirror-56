import json
from pathlib import Path

from graphviz import Digraph


def get_colour(percent):
    r = 1 if percent < 0.5 else 1 - percent / 1
    g = percent / 1
    return "#%2x%2x%2x" % (int(r * 255), int(g * 255), 0)


def render_views(path, label=None):
    base_path = Path(path)
    quality_views = sorted(base_path.glob("*.json"), reverse=True)

    dot = Digraph(
        graph_attr={"rankdir": "LR", "style": "filled", "label": label},
        node_attr={"shape": "note", "style": "filled"},
    )

    for component_view in quality_views:
        with open(component_view) as component_file:
            component = json.load(component_file)

            scores = [attribute["score"] for attribute in component["attributes"]]
            total_score = sum(scores)
            attribute_count = len(component["attributes"])

            percentage = total_score / (attribute_count * 10)

            dot.node(
                component["name"],
                component["name"],
                {"fillcolor": get_colour(percentage)},
            )

            if "depends_on" in component:
                for dependency in component["depends_on"]:
                    dot.edge(dependency, component["name"])

    dot.render(base_path.joinpath("quality_view.gv"))
