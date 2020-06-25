import my_checkers
import unittest


class TestsPieces(unittest.TestCase):
    def setUp(self):
        self.pieces = my_checkers.Pieces()

    def test_friendly(self):
        self.assertEqual(my_checkers.Pieces.getFrendly(self.pieces), {'pawn': 1, 'king': 3})

    def test_enemy(self):
        self.assertEqual(my_checkers.Pieces.getEnemy(self.pieces), {'pawn': 2, 'king': 4})

    def test_placing(self):
        board1 = [[0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0]]
        board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        my_checkers.Pieces.place_starting_pieces(self.pieces, board)
        self.assertEqual(board, board1)

    def test_valid_move(self):
        board1 = [[0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0]]
        self.assertFalse(self.pieces.is_valid_move(board1, 0, 1, 5, 0, 1))

    def test_valid_selection(self):
        board1 = [[0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0]]
        self.assertTrue(self.pieces.is_valid_selection(board1, 0, 1))

    def test_no_chips(self):
        board1 = [[0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0]]
        self.assertTrue(self.pieces.no_chips_between(board1, 1, 2, 6, 1, 1))

    def test_is_valid_king_move(self):
        board1 = [[0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0]]
        self.assertFalse(self.pieces.is_valid_king_move(board1,0,1,7,6,1,False))


class TestColors(unittest.TestCase):
    def setUp(self):
        self.color = my_checkers.Colors()

    def test_green(self):
        self.assertEqual(self.color.Black, (0, 0, 0))

    def test_WHITE(self):
        self.assertEqual(self.color.White, (255, 255, 255))

    def test_GOLD(self):
        self.assertEqual(self.color.Gold, (255, 215, 0))

    def test_GREY(self):
        self.assertEqual(self.color.Grey, (128, 128, 128))


if __name__ == '__main__':
    unittest.main()
