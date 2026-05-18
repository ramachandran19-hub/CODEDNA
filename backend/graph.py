import networkx as nx
from pyvis.network import Network
import os


# =====================================
# 🧠 FORMAT LABEL
# =====================================
def format_label(filename):

    base = os.path.basename(filename)

    name = base.replace(".py", "")
    name = name.replace("_", " ")

    return name.title()


# =====================================
# 🧠 DETECT LAYER
# =====================================
def detect_layer(filename):

    lower = filename.lower()

    if "main" in lower or "app" in lower:
        return 0

    elif "api" in lower or "route" in lower:
        return 1

    elif (
        "service" in lower
        or "analyzer" in lower
        or "engine" in lower
    ):
        return 2

    return 3


# =====================================
# 🗺 GENERATE GRAPH
# =====================================
def generate_code_map(code_files, structure_data):

    # 🔥 HARD LIMIT
    code_files = code_files[:40]
    structure_data = structure_data[:40]

    G = nx.DiGraph()

    internal_files = set()

    # =====================================
    # 📄 STORE INTERNAL FILES
    # =====================================
    for file in code_files:

        internal_files.add(file["file"])

    # =====================================
    # 🧠 BUILD NODES
    # =====================================
    for file, struct in zip(code_files, structure_data):

        filename = file["file"]

        imports = file.get("imports", [])

        layer = detect_layer(filename)

        degree = len(imports)

        label = format_label(filename)

        # =====================================
        # 🎨 COLORS
        # =====================================
        if layer == 0:
            color = "#00ff88"

        elif layer == 1:
            color = "#4da6ff"

        elif layer == 2:
            color = "#b366ff"

        else:
            color = "#7f8c8d"

        # =====================================
        # 📏 SIZE
        # =====================================
        size = 18 + (degree * 2)

        # =====================================
        # 🧠 TOOLTIP
        # =====================================
        title = f"""
        <b>{label}</b><br><br>

        📄 {filename}<br>
        ⚙️ Functions: {len(struct["functions"])}<br>
        🔗 Imports: {degree}
        """

        # =====================================
        # ➕ NODE
        # =====================================
        G.add_node(
            filename,
            label=label,
            color=color,
            size=size,
            title=title,
            layer=layer
        )

    # =====================================
    # 🔗 BUILD EDGES
    # =====================================
    for file in code_files:

        source = file["file"]

        imports = file.get("imports", [])

        for imp in imports:

            # 🔥 ONLY INTERNAL FILES
            matched = None

            for internal in internal_files:

                if imp in internal:
                    matched = internal
                    break

            if matched:

                G.add_edge(source, matched)

    # =====================================
    # 🌌 CREATE NETWORK
    # =====================================
    net = Network(
        height="850px",
        width="100%",
        bgcolor="#0d1117",
        font_color="white",
        directed=True
    )

    # 🔥 VERY IMPORTANT
    net.toggle_physics(False)

    # =====================================
    # ➕ ADD NODES
    # =====================================
    for node, data in G.nodes(data=True):

        net.add_node(
            node,
            label=data.get("label", node),
            title=data.get("title", node),
            color=data.get("color", "#7f8c8d"),
            size=data.get("size", 20),
            level=data.get("layer", 3),
            shape="dot"
        )

    # =====================================
    # ➕ ADD EDGES
    # =====================================
    for source, target in G.edges():

        net.add_edge(
            source,
            target,
            color="#00ffaa",
            width=1.5,
            arrows="to"
        )

    # =====================================
    # ⚡ FAST LAYOUT
    # =====================================
    net.set_options("""
    var options = {

      "layout": {

        "hierarchical": {

          "enabled": true,
          "direction": "UD",
          "sortMethod": "directed",

          "nodeSpacing": 90,
          "treeSpacing": 120,
          "levelSeparation": 100
        }
      },

      "physics": {
        "enabled": false
      },

      "nodes": {

        "font": {
          "size": 14
        }
      },

      "edges": {

        "smooth": false
      },

      "interaction": {

        "hover": true,
        "navigationButtons": true
      }
    }
    """)

    # =====================================
    # 💾 SAVE
    # =====================================
    output_path = "code_map.html"

    net.save_graph(output_path)

    return output_path