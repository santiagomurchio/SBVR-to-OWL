class ListUtils:

    def same_elements_ignore_order(self, list1, list2):
        if len(list1) != len(list2):
            return false

        for element in list2:
            if element not in list2:
                return false

        return true
