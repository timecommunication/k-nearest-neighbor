# implemented by the kd-tree
import numpy as np


class Node:

    def __init__(self, value=None, matrix=None):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.matrix = matrix
        self.left_vectors = None
        self.right_vectors = None

    def construct_branch(self, current_sort_dimension):
        if len(self.matrix) == 0:
            return False

        # the matrix was sorted based on the specific dimension
        T_ranked = self.matrix[self.matrix[:, current_sort_dimension].argsort()]

        # get the middle index
        mid_index = len(T_ranked) // 2
        median_vector = T_ranked[mid_index, :]

        self.value = median_vector

        # save the children nodes to the specific branch
        self.left_vectors = T_ranked[:mid_index, :]
        self.right_vectors = T_ranked[mid_index + 1:, :]
        return True

    @staticmethod
    def show_node_info(node):
        print('-----------')
        print("root node's value:\n", node.value)
        print("root's left children nodes:\n", node.left_vectors)
        print("root's right children nodes:\n", node.right_vectors)


class NodeQueue:

    def __init__(self):
        self.nodes_queue = list()


class KdTree:

    @staticmethod
    def move_sort_cursor(depth, dimension):
        return depth % dimension

    def __init__(self, matrix):
        self.nodes_num = len(matrix)
        self.current_depth = 0
        self.dimension = matrix.ndim

        # initialize the root node
        self.root = Node(matrix=T)
        self.root.construct_branch(0)

    def generate_kd_tree(self):

        # initialize the kd-tree traversal list
        nq = NodeQueue()
        nq.nodes_queue.append(self.root)

        # use the pre-order (root-prior-traversal) to define the node's value
        cur = self.root
        for i in range(self.nodes_num):
            # move the sort dimension circularly
            self.current_depth += 1
            current_sort_dimension = self.move_sort_cursor(self.current_depth, self.dimension)

            cur = nq.nodes_queue.pop(0)

            # define the left node
            cur.left = Node(matrix=cur.left_vectors)
            cur.left.construct_branch(current_sort_dimension)
            nq.nodes_queue.append(cur.left)

            # define the right node
            cur.right = Node(matrix=cur.right_vectors)
            cur.right.construct_branch(current_sort_dimension)
            nq.nodes_queue.append(cur.right)

            # set the parent node for the children nodes
            cur.left.parent = cur
            cur.right.parent = cur

            # print current node's info
            Node.show_node_info(cur)

    def get_the_nearest_node(self, vector):

        cur = self.root
        self.current_depth = -1
        while True:
            try:
                if cur.left.value == None and cur.right.value==None:
                    break
            except ValueError:
                pass
            self.current_depth += 1
            index = self.move_sort_cursor(self.current_depth, self.dimension)
            print('index:', index, '^^^^^^', 'compare to ', cur.value)
            if vector[index] <= cur.value[index]:
                cur = cur.left
            elif vector[index] > cur.value[index]:
                cur = cur.right

        print(vector, 'input vector')
        print(cur.value, 'is the nearest leaf node(up-to-down-search)')
        return cur


if __name__ == '__main__':

    # data-set
    T = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    T = np.array(T)
    print(T)
    print("T's dimension is ", T.ndim)

    # construct the kd-tree
    kd_tree = KdTree(matrix=T)
    kd_tree.generate_kd_tree()

    unknown = np.array([6.2, 3.8])
    up_to_down_result = kd_tree.get_the_nearest_node(unknown)














