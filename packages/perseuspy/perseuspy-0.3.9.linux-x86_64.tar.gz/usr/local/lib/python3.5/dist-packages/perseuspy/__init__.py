"""
perseuspy module for Python-Perseus interop.
"""
from perseuspy.version import version_string as __version__
import perseuspy.dependent_peptides
import perseuspy.io.perseus.matrix
# Monkey-patching pandas
import pandas as pd
pd.DataFrame.to_perseus = perseuspy.io.perseus.matrix.to_perseus
pd.read_perseus = perseuspy.io.perseus.matrix.read_perseus

import perseuspy.io.perseus.network
from perseuspy.io.perseus.network import read_networks, write_networks
import networkx as nx
nx.from_perseus = perseuspy.io.perseus.network.from_perseus
nx.to_perseus = perseuspy.io.perseus.network.to_perseus
