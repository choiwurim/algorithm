class BinaryNode:

    def init(self,k,v):
        self.key=k
        self.value=v
        self.left=None
        self.right=None
        self.height=0

    def height_diff(self):
        left_height=self.left.height if self.left else -1
        right_height=self.right.height if self.right else -1
        return left_height-right_height
    
    def compute_height(self):
        left_height=self.left.height if self.left else -1
        right_height=self.right.height if self.right else -1
        self.height=1+max(left_height, right_height)

class BinaryTree:

    def init(self):
        self.root=None
    
    def is_empty(self):
        return self.root is None
    
    def put(self,k,v):
        if k is None:
            raise RuntimeError('key for symbol table cannot be None')
        self.root=self._put(self.root,k,v)
    
    def _put(self,node,k,v):
        if node is None:
            return BinaryNode(k,v)
        if k==node.key:
            node.value=v
            return node
        if k<node.key:
            node.left=self._put(node.left,k,v)
            node=resolve_left_leaning(node)
        else:
            node.right=self._put(node.right,k,v)
            node=resolve_right_leaning(node)
        
        node.compute_height()
        return node

    def remove(self,key):
        self.root=self._remove(self.root, key)

    def remove_min(self,node):
        if node.left is None:
            return node.right
        
        node.left=self.remove_min(node.left)
        node=resolve_right_leaning(node)
        node.compute_height()
        return node
    
    def _remove(self,node,key):
        if node is None:
            return None
        
        if key<node.key:
            node.left=self._remove(node.left,key)
            node=resolve_right_leaning(node)
        elif key>node.key:
            node.right=self._remove(node.right,key)
            node=resolve_left_leaning(node)
        else:
            if node.left is None:   return node.right
            if node.right is None:  return node.left
            
            original=node
            node=node.right
            while node.left:
                node=node.left
            node.right=self.remove_min(original.right)
            node.right=original.left
            node=resolve_left_leaning(node)

        node.compute_height()
        return node
    
    def get(self, key):
        node=self.root
        while node:
            if key==node.key:
                return node.value
            if key<node.key:
                node=node.left
            else:
                node=node.right
        return None
    
    def iter(self):
        for pair in self.inorder(self.root):
            yield pair
    
    def inorder(self,node):
        if node is None:
            return
        for pair in self.inorder(node.left):
            yield pair
        yield (node.key, node.value)
        for pair in self.inorder(node.right):
            yield pair