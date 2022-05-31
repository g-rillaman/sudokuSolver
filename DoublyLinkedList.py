from typing import Optional

class LinkedListNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.prev = None
        self.next = None

class DoublyCircularLinkedList:
    def __init__(self, value: Optional[int]=None) -> None:
        self.head = None
        if value is not None:
            self.push_on_empty_list(value)

    def push_on_empty_list(self, value):
        new_node = LinkedListNode(value)
        new_node.prev = new_node
        new_node.next = new_node
        self.head = new_node

    def push(self, value) -> None:
        """Add a node with value `value` to the front."""

        if self.head is None:  # Empty initial list
            self.push_on_empty_list(value)
        else:
            # We place the node before the previous head
            new_node = LinkedListNode(value=value)
            new_node.prev = self.head.prev
            new_node.next = self.head

            self.head.prev.next = new_node  # Change next pointer of last node to the new node
            self.head.prev = new_node  # Change prev pointer of previous head node to the new node

            self.head = new_node

    def insert(self, prev_node, value):
        """Insert new node with value `value` after `prev_node`."""

        new_node = LinkedListNode(value=value)

        # Anchor next and prev for new node
        new_node.next = prev_node.next
        new_node.prev = prev_node

        prev_node.next = new_node
        new_node.next.prev = new_node

    def traverse_forward(self):
        node = self.head
        yield node
        node = node.next
        while node != self.head:
            yield node
            node = node.next

    def traverse_backward(self):
        node = self.head
        yield node
        node = node.prev
        while node != self.head:
            yield node
            node = node.prev
