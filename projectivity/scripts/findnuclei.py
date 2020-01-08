from udapi.core.block import Block
from itertools import combinations

# pylint: disable=no-self-use


class findnuclei(Block):
    """
    This block attempts to find the variation nucleus in a given non-projective tree, for each non-projective edge.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_gap_nodes = []
        self.gap_degree = 0
        self.vn = set()
        
    def process_tree(self, root):
        max_gap_degree = 2
        self.gap_degree = self.get_gap_degree(root)
        if self.gap_degree > max_gap_degree:
            return

        for node in root.descendants:
            if node.is_nonprojective():
                head = node.parent
                dependent = node
                gap_nodes = [x[1] for x in self.all_gap_nodes if x[0] == node]
                if len(gap_nodes) != 0:
                    gap_nodes = gap_nodes[0]
                else:
                    continue
                if all([x.upos == "PUNCT" or x.udeprel == "punct" for x in gap_nodes]):
                    continue
                vn_nodes = self.get_gap_heads(gap_nodes, node)
                for tuplex in self.generate_vn(head, dependent, vn_nodes):
                    if len(tuplex) >= 4:
                        self.vn.add(tuplex)
                        self.print_occurrence(tuplex, node)
        return
        
    def get_gap_degree(self, root):
        """
        for every node u in the tree:
                compute the projection of the node, i.e., get the set of nodes containing u and all its descendants
                sort the nodes in the projection according to word order
                find the number of gaps. A gap is a contiguous linear sequence of words of the sentence that are not members of the projection but are surrounded by nodes that are in the projection.
                    so basically, if the first node of the projection is at position i and the last node at position j, you iterate from i to j and check for each word whether it is in the projection.
                    If not, it is in the gap. If the previous word was also in a gap, they are in the same gap. But every time you encounter a word that is in the projection, the current gap ends,
                    and when you find another non-member word, it starts a new gap. Count the number of gaps. Note it as the gap degree of the node u.
                when you have done this with every node, find the node which had the highest gap degree. That is the gap degree of the tree.
        """
        current_gap_degree = 0
        for node in root.descendants:
            if node.is_nonprojective():
                if node.upos == "PUNCT" or node.udeprel == "punct":
                    continue
                gapnodes = []
                head = node.parent
                from_node = node
                to_node = node.parent
                if node.parent.ord < node.ord:
                    from_node, to_node = to_node, from_node
                check_set = [x for x in root.descendants if from_node.ord < x.ord < to_node.ord]
                in_proj = True
                node_gd = 0
                for cand_node in check_set:
                    if cand_node in head.descendants and not in_proj:
                        node_gd += 1
                        in_proj = True
                    elif cand_node not in head.descendants:
                        gapnodes.append(cand_node)
                        if in_proj:
                            node_gd += 1
                            in_proj = False
                if not all([x.upos == "PUNCT" or x.udeprel == "punct" for x in gapnodes]):
                    self.all_gap_nodes.append((node, gapnodes))
                current_gap_degree = max(node_gd, current_gap_degree)
        return current_gap_degree

    def get_gap_heads(self, gapnodes, curr_node):
        """
        This function is to generate the gap nucleus. The procedure is explained in form of comments.
        """
        gap_heads = [x for x in gapnodes]
        head = curr_node.parent
        for cand_node in gapnodes:
            if cand_node.parent == head and cand_node.is_nonprojective():
                for x in cand_node.descendants(add_self=True):
                    """
                    There exists a node in gap, attached to the same head non-projectively
                    Remove all associations of this node, since we are interested in looking at the non-projective attachment from head -> dependent
                    Removing this node will help us combine the dependents later, if they have the same set of variation nuclei
                    """
                    if x in gap_heads:
                        gap_heads.remove(x)
                continue
            if head in cand_node.descendants:
                """
                This Node is on a higher plane than projective edge.
                """
                if not cand_node.parent.is_root():
                    """
                    Case 1: This Node is Root
                        Can't remove all descendants because that'll make everything go away.
                        Keep it as such, without any changes
                    Case 2: This Node is not Root
                        Remove all the descendants of this node that are not head's descendants
                    """
                    removal_candidates = [x for x in cand_node.descendants(add_self=False) if x not in head.descendants and x in gap_heads]
                    for x in removal_candidates:
                        gap_heads.remove(x)
            else:
                if not cand_node.is_leaf():
                    """
                    Non-leaf Node. Remove all descendants from gap_heads list
                    """
                    for x in cand_node.descendants(add_self=False):
                        if x in gap_heads:
                            gap_heads.remove(x)
                else:
                    """
                    Leaf Node. Remove from gap_heads if punctuation. Otherwise, let it be.
                    """
                    if (cand_node.upos == "PUNCT" or cand_node.udeprel == "punct") and cand_node in gap_heads:
                        gap_heads.remove(cand_node)
        return gap_heads

    def generate_vn(self, head, dependent, nodeslist):
        """Generate all combinations possible for a given gap nucleus, and generate variation nucleus out of it"""
        for i in range(1, len(nodeslist)+1):
            for j in list(combinations(nodeslist, i)):
                vn = (head, )
                vn += j
                vn += (dependent, )
                yield self.generate_data(vn)
     
    def generate_data(self, vn):
        """
        In case there are no lemmas available (fro language), add forms instead
        """
        node_tuple = tuple()
        for node in vn:
            if node.lemma == "_":
                node_tuple += (node.form.lower(),)
            else:
                node_tuple += (node.lemma,)
        return node_tuple
    
    def print_occurrence(self, tuplex, node):
        """
        Print (variation_nuclei, node_address) pairs. One item per line
        """
        print(" ".join(tuplex), node.address(), sep="\t")
