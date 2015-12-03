import unittest
import sudoku
import copy


class SudokuTester(unittest.TestCase):
    def test_loads_dumps(self):
        with open("solved.su", "r") as f:
            dat = f.read().strip()
        sudoku_arry = sudoku.loads(dat)
        self.assertEqual(len(sudoku_arry), 9)
        self.assertEqual(len(sudoku_arry[0]), 9)
        sudoku_string = sudoku.dumps(sudoku_arry)
        self.assertEqual(sudoku_string, dat)

    def test_fill_spaces(self):
        with open("solved.su", "r") as f:
            dat = f.read().strip()
            solved = sudoku.loads(dat)

        unsolved = copy.copy(solved)
        unsolved[2][2] = 0  # mark a single space as unknown
        self.assertFalse(sudoku.validate(unsolved))
        self.assertEqual(sudoku.count_unknown(unsolved), 1)

        # Can we solve it?
        maybe_solved = sudoku.fill_spaces(unsolved)
        self.assertEqual(sudoku.count_unknown(maybe_solved), 0)
        self.assertEqual(maybe_solved, solved)
        self.assertTrue(sudoku.validate(maybe_solved))

    def test_solve(self):
        with open("solved.su", "r") as f:
            dat = f.read().strip()
            solved = sudoku.loads(dat)

        with open("unsolved.su", "r") as f:
            dat = f.read().strip()
            unsolved = sudoku.loads(dat)

        hopefully_solved = sudoku.solve(unsolved)
        self.assertEqual(hopefully_solved, solved)

    def test_validate(self):
        with open("solved.su", "r") as f:
            dat = f.read().strip()
        # This test sudoku is a valid one!
        sudoku_arry = sudoku.loads(dat)
        self.assertTrue(sudoku.validate(sudoku_arry))

        # Violate several rules...
        sudoku_arry[0][0] = 6
        sudoku_arry[1][1] = 6
        self.assertFalse(sudoku.validate(sudoku_arry))

        # Try using an unsolved sudoku!
        with open("unsolved.su", "r") as f:
            dat = f.read().strip()
        # This sudoku is not even solved!
        sudoku_arry = sudoku.loads(dat)
        self.assertFalse(sudoku.validate(sudoku_arry))

    def test_square_to_psuedo_row(self):
        with open("solved.su", "r") as f:
            dat = f.read().strip()
        sudoku_arry = sudoku.loads(dat)
        self.assertEqual(
            sudoku.square_to_psuedo_row(sudoku_arry, 0, 0),
            [1, 2, 3, 4, 5, 6, 7, 8, 9])

        self.assertEqual(
            sudoku.square_to_psuedo_row(sudoku_arry, 2, 2),
            [9, 7, 8, 3, 1, 2, 6, 4, 5])

        self.assertEqual(
            sudoku.square_to_psuedo_row(sudoku_arry, 1, 0),
            [4, 5, 6, 7, 8, 9, 1, 2, 3])

        self.assertEqual(
            sudoku.square_to_psuedo_row(sudoku_arry, 0, 1),
            [2, 3, 1, 5, 6, 4, 8, 9, 7])

    def test_column_to_psuedo_row(self):
        with open("solved.su", "r") as f:
            dat = f.read().strip()
        sudoku_arry = sudoku.loads(dat)
        self.assertEqual(
            sudoku.column_to_psuedo_row(sudoku_arry, 0),
            [1, 4, 7, 2, 5, 8, 3, 6, 9])

        self.assertEqual(
            sudoku.column_to_psuedo_row(sudoku_arry, 1),
            [2, 5, 8, 3, 6, 9, 1, 4, 7])

        self.assertEqual(
            sudoku.column_to_psuedo_row(sudoku_arry, 3),
            [4, 7, 1, 5, 8, 2, 6, 9, 3])

        self.assertEqual(
            sudoku.column_to_psuedo_row(sudoku_arry, 8),
            [9, 3, 6, 7, 1, 4, 8, 2, 5])

    def test_validate_num_list(self):
        # correct and sorted
        row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertTrue(sudoku.validate_row(row))

        # too short
        row = [1, 2, 3, 4, 5, 6, 7, 9]
        self.assertFalse(sudoku.validate_row(row))

        # too long
        row = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertFalse(sudoku.validate_row(row))

        # correct but unsorted
        row = [2, 1, 3, 4, 5, 6, 7, 9, 8]
        self.assertTrue(sudoku.validate_row(row))

        # correct but unsorted
        row = [8, 7, 2, 5, 4, 6, 1, 9, 3]
        self.assertTrue(sudoku.validate_row(row))

        # duplicate number
        row = [1, 2, 3, 3, 5, 6, 7, 8, 9]
        self.assertFalse(sudoku.validate_row(row))

        # contains a 0, the "no knowledge" special value
        row = [1, 2, 0, 4, 5, 6, 7, 8, 9]
        self.assertFalse(sudoku.validate_row(row))


if __name__ == '__main__':
    unittest.main()
