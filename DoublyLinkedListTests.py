import unittest

from DoublyLinkedList import DoublyCircularLinkedList, LinkedListNode

class TestCreation(unittest.TestCase):
    def test_creation_of_list(self) -> None:
        expected = LinkedListNode(1)
        expected.prev = expected
        expected.next = expected
        actual = DoublyCircularLinkedList(1)
        
        self.assertEqual(actual.head.value, expected.value)
        self.assertEqual(actual.head.prev.value, expected.prev.value)
        self.assertEqual(actual.head.next.value, expected.next.value)


class TestPush(unittest.TestCase):
    def test_push_on_list(self) -> None:
        lst = DoublyCircularLinkedList(0)
        for i in range(1,5):
            lst.push(i)

        self.assertEqual(
            [item.value for item in lst.traverse_forward()],
            [4, 3, 2, 1, 0]
        )
        self.assertEqual(
            [item.value for item in lst.traverse_backward()],
            [4, 0, 1, 2, 3]
        )
    
    def test_push_on_empty_list(self) -> None:
        lst = DoublyCircularLinkedList()
        lst.push(1)

        self.assertEqual(
            [item.value for item in lst.traverse_forward()],
            [1]
        )


class TestInsert(unittest.TestCase):
    def test_insert_in_middle(self) -> None:
        lst = DoublyCircularLinkedList(0)
        lst.push(2)
        lst.push(3)
        lst.insert(lst.head.next, 1)

        self.assertEqual(
            [item.value for item in lst.traverse_forward()],
            [3, 2, 1, 0]
        )
        self.assertEqual(
            [item.value for item in lst.traverse_backward()],
            [3, 0, 1, 2]
        )


if __name__ == "__main__":
    unittest.main()