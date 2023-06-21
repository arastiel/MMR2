class PQueue:
    def __init__(self):
        self.items = []

    def push(self, u, value):
        """appends [u, value] to self.items"""
        self.items.append([u, value])
        # O(1)

    def decrease_key(self, u, value):
        """changes value of node u"""
        item = next(item for item in self.items if item[0] == u)
        item[1] = value
        # next: O(n)
        # for loop in next: O(n)
        # → O(n) + O(n) = O(2n) element O(n)

    def pop_min(self):
        """removes the node with smallest value, returns None if no nodes in self.items"""
        if len(self.items) == 0:
            return None
        else:
            min_val = min(item[1] for item in self.items)
            min_item = [item for item in self.items if item[1] == min_val][0]
            self.items.remove(min_item)
            return min_item[0]

            # min: O(n)
            # for loop in der min: O(n) → min bestimmen O(n) + O(n)
            # remove: O(n)
            # for loop in remove: O(n) → pop_min (O(n) + O(n)) element O(n) ? not sure



if __name__ == '__main__':
    pqueue = PQueue()
    pqueue.push(123, 10)
    pqueue.push(125, 15)
    pqueue.push(127, 2)

    print(pqueue.items)

    pqueue.decrease_key(125, 1)

    print(pqueue.items)

    pqueue.pop_min()

    print(pqueue.items)