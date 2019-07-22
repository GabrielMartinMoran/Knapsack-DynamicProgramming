from KnapsackSolver import *
from Item import *
import unittest

DATASET_1 = [
    Item("Item 1",  8, 4),
    Item("Item 2",  5, 6),
    Item("Item 3",  2, 5),
    Item("Item 4",  7, 8),
    Item("Item 5",  2, 1),
    Item("Item 6",  8, 2),
    Item("Item 7",  4, 6),
    Item("Item 8",  3, 4),
    Item("Item 9",  2, 5),
    Item("Item 10", 9, 7),
    Item("Item 11", 2, 7),
    Item("Item 12", 4, 5),
    Item("Item 13", 6, 10),
]

DATASET_2 = [
    Item("Item 1",  8, 5),
    Item("Item 2",  4, 3),
    Item("Item 3",  1, 2),
    Item("Item 4",  6, 4)
]

DATASET_3 = [
    Item("Item 1",  2, 16),
    Item("Item 2",  3, 19),
    Item("Item 3",  4, 23),
    Item("Item 4",  5, 28)
]

# Usar con capacidad 1000 -> El valor resultante deberia ser 9147
DATASET_4 = [
    Item(7880846611, 995, 100),
    Item(6903898342, 485, 94),
    Item(2209302251, 326, 506),
    Item(1972671328, 248, 416),
    Item(2050866823, 421, 992),
    Item(7682047498, 322, 649),
    Item(7167350944, 795, 237),
    Item(6832517700, 43, 457),
    Item(1274041128, 845, 815),
    Item(7732569959, 955, 446),
    Item(5077314363, 252, 422),
    Item(8178059980, 9, 791),
    Item(9454748442, 901, 359),
    Item(8834058005, 122, 667),
    Item(7568538319, 94, 598),
    Item(7400285010, 738, 7),
    Item(2099431833, 574, 544),
    Item(2126041922, 715, 334),
    Item(7781935834, 882, 766),
    Item(4915980454, 367, 994),
    Item(1908862758, 984, 893),
    Item(3337009944, 299, 633),
    Item(9722689025, 433, 131),
    Item(1177491983, 682, 428),
    Item(3555973828, 72, 700),
    Item(4486171743, 874, 617),
    Item(6181392997, 138, 874),
    Item(6454084210, 856, 720),
    Item(8267525455, 145, 419),
    Item(5902278156, 995, 794),
    Item(5705651171, 529, 196),
    Item(1582999949, 199, 997),
    Item(1778561954, 277, 116),
    Item(5455447328, 97, 908),
    Item(5391046775, 719, 539),
    Item(2596766829, 242, 707),
    Item(1524398298, 107, 569),
    Item(8748549008, 122, 537),
    Item(1928579270, 70, 931),
    Item(9605404513, 98, 726),
    Item(8161126081, 600, 487),
    Item(5349721853, 645, 772),
    Item(2958237855, 267, 513),
    Item(7708812233, 972, 81),
    Item(6975337493, 895, 943),
    Item(4589571746, 213, 58),
    Item(1820218026, 748, 303),
    Item(6609976517, 487, 764),
    Item(8618369105, 923, 536),
    Item(1918200629, 29, 724),
    Item(2438270910, 674, 789),
    Item(1710859448, 540, 479),
    Item(8832007604, 554, 142),
    Item(3923302579, 467, 339),
    Item(8163642896, 46, 641),
    Item(6947777084, 710, 196),
    Item(3860841241, 553, 494),
    Item(6555836636, 191, 66),
    Item(9500994408, 724, 824),
    Item(2549324681, 730, 208),
    Item(3891215548, 988, 711),
    Item(5387807134, 90, 800),
    Item(9176875751, 340, 314),
    Item(6904995321, 549, 289),
    Item(2293255552, 196, 401),
    Item(3260957377, 865, 466),
    Item(2807108213, 678, 689),
    Item(5913162172, 570, 833),
    Item(6769239041, 936, 225),
    Item(4046864754, 722, 244),
    Item(1180565844, 651, 849),
    Item(8540176733, 123, 113),
    Item(1007664343, 431, 379),
    Item(5978329571, 508, 361),
    Item(5032505408, 585, 65),
    Item(7567194673, 853, 486),
    Item(6084252189, 642, 686),
    Item(5001584984, 992, 286),
    Item(2341351461, 725, 889),
    Item(8046437600, 286, 24),
    Item(7356912275, 812, 491),
    Item(2651888547, 859, 891),
    Item(5350815514, 663, 90),
    Item(2938710967, 88, 181),
    Item(2220020488, 179, 214),
    Item(9075884377, 187, 17),
    Item(9491031043, 619, 472),
    Item(4436870092, 261, 418),
    Item(6532107861, 846, 419),
    Item(8702194664, 192, 356),
    Item(9078148955, 261, 682),
    Item(5141711866, 514, 306),
    Item(9421698433, 886, 201),
    Item(9543961064, 530, 385),
    Item(1463898026, 849, 952),
    Item(3248157926, 294, 500),
    Item(6772376684, 799, 194),
    Item(5187558145, 391, 737),
    Item(4517323088, 330, 324),
    Item(8520448627, 298, 992),
    Item(9174257534, 790, 224),
]

class Test(unittest.TestCase):

    def get_solution(self, knapsack_capacity, items):
        solver = KnapsackSolver()
        solution, table = solver.solve(items, knapsack_capacity)
        return solution
    
    def test_dataset_1(self):
        solution = self.get_solution(20, DATASET_1)
        self.assertEqual(solution.total_value, 38)
        self.assertEqual(solution.total_weight, 20)

    def test_dataset_2(self):
        solution = self.get_solution(15, DATASET_2)
        self.assertEqual(solution.total_value, 11)
        self.assertEqual(solution.total_weight, 15)

    def test_dataset_3(self):
        solution = self.get_solution(7, DATASET_3)
        self.assertEqual(solution.total_value, 44)
        self.assertEqual(solution.total_weight, 7)

if __name__ == '__main__':
    unittest.main()