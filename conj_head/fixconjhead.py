from udapi.core.block import Block

# pylint: disable=no-self-use


class fixconjhead(Block):
    """This block attempts to fix the cases where the coordinating conjunction is attached
    to the first conjunct, instead of the trailing conjunct as per UDv2 guidelines. While 
    changing the attachments, the condition of projectivity is checked at each step.
    This algorithm only works for languages where we are sure that the coordinating conjunction
    occurs in between the conjuncts, and not in the final form (like sa, for example)."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    
    def process_tree(self, root):
        for node in root.descendants:
            # change the head of the node
            if self.wrongHead(node):
                if not self.changeHead_sibling(node):
                    if not self.changeHead_aunt(node):
                        if not self.changeHead_granny(node):
                            pass
    
    
    def isCconj(self, node):
        if node.upos == "CCONJ" and node.udeprel == "cc":
            return True
        return False
    
    
    def wrongHead(self, node):
        if self.isCconj(node) and node.parent.precedes(node) and not node.parent.is_root():
            return True
        return False
    
    
    def changeHead_sibling(self, node):
        """Initially, we try to attach the node to the next sibling of the conjunction.
        We want to minimise the chances of a case where the node needs to go up the tree."""
        orig_parent = node.parent
        count = 0
        tgt = None
        for sibling in node.parent.children:
            if node.precedes(sibling) and sibling.upos not in ["SYM", "PUNCT", "X"]:
                tgt = sibling
                count += 1
        if count == 1:
            """If there is just one child (not including PUNCT/SYM/X),
            change the head of the conjunction to this child.
            Nothing else to do"""
            node.parent = tgt
            if node.is_nonprojective() or node.parent.is_root():
                node.parent = orig_parent
            else:
                return True
        else:
            """change the head to the first instance.
            We give first priority to a node with deprel as conj,
            and then check for other dependent clause heads"""
            for sibling in node.parent.children:
                if sibling.udeprel == "conj" and node.precedes(sibling):
                    node.parent = sibling
                    if node.is_nonprojective() or node.parent.is_root():
                        node.parent = orig_parent
                    else:
                        return True
            for sibling in node.parent.children:
                if sibling.udeprel in ["obl", "xcomp", "nmod", "nsubj"] and node.precedes(sibling):
                    node.parent = sibling
                    if node.is_nonprojective() or node.parent.is_root():
                        node.parent = orig_parent
                    else:
                        return True
        return False
    
    
    def changeHead_aunt(self, node):
        """Latch on to the next aunt (sibling of the parent node). Again, more
        priority to a node with conj deprel, followed by other
        dependent clause heads"""
        orig_parent = node.parent
        if not node.parent.is_root():
            grandparent = node.parent.parent
            aunts = [x for x in grandparent.children if node.precedes(x)]
            if aunts != []:
                aunt = aunts[0]
                node.parent = aunts[0]
                """make sure the attachment to the aunt is projective in nature"""
                if node.is_nonprojective() or node.parent.is_root():
                    node.parent = orig_parent
                else:
                    return True
        """No candidate aunt found. Nothing we can do"""
        return False

    
    def changeHead_granny(self, node):
        """lowest priority allotted to moving up the tree"""
        orig_parent = node.parent
        if not node.parent.is_root():
            granny = node.parent.parent
            node.parent = granny
            if node.is_nonprojective() or node.parent.is_root():
                node.parent = orig_parent
            else:
                return True
        return False
