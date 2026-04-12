import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.rules import *


class RulesTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(RULES[1].computation(231), ORD_GT)

    def test_2(self):
        self.assertEqual(RULES[2].computation(123), ORD_LT)

    def test_3(self):
        self.assertEqual(RULES[3].computation(153), ORD_GT)

    def test_4(self):
        self.assertEqual(RULES[4].computation(142), ORD_EQ)

    def test_5(self):
        self.assertEqual(RULES[5].computation(123), 1)
        self.assertEqual(RULES[5].computation(223), 0)

    def test_6(self):
        self.assertEqual(RULES[6].computation(123), 0)
        self.assertEqual(RULES[6].computation(113), 1)

    def test_7(self):
        self.assertEqual(RULES[7].computation(123), 1)
        self.assertEqual(RULES[7].computation(124), 0)

    def test_8(self):
        self.assertEqual(RULES[8].computation(123), 1)
        self.assertEqual(RULES[8].computation(223), 0)
        self.assertEqual(RULES[8].computation(121), 2)
        self.assertEqual(RULES[8].computation(111), 3)

    def test_9(self):
        self.assertEqual(RULES[9].computation(123), 1)

    def test_10(self):
        self.assertEqual(RULES[10].computation(123), 0)

    def test_11(self):
        self.assertEqual(RULES[11].computation(123), ORD_LT)
        self.assertEqual(RULES[11].computation(223), ORD_EQ)

    def test_12(self):
        self.assertEqual(RULES[12].computation(123), ORD_LT)
        self.assertEqual(RULES[12].computation(423), ORD_GT)

    def test_13(self):
        self.assertEqual(RULES[13].computation(123), ORD_LT)
        self.assertEqual(RULES[13].computation(122), ORD_EQ)

    def test_14(self):
        self.assertEqual(RULES[14].computation(123), 2)
        self.assertEqual(RULES[14].computation(223), -1)
        self.assertEqual(RULES[14].computation(421), 0)

    def test_15(self):
        self.assertEqual(RULES[15].computation(123), 0)
        self.assertEqual(RULES[15].computation(253), 1)
        self.assertEqual(RULES[15].computation(133), -1)

    def test_16(self):
        self.assertEqual(RULES[16].computation(123), True)
        self.assertEqual(RULES[16].computation(122), False)

    def test_17(self):
        self.assertEqual(RULES[17].computation(123), 1)
        self.assertEqual(RULES[17].computation(124), 2)

    def test_18(self):
        self.assertEqual(RULES[18].computation(123), 0)
        self.assertEqual(RULES[18].computation(122), 1)

    def test_19(self):
        self.assertEqual(RULES[19].computation(123), ORD_LT)
        self.assertEqual(RULES[19].computation(423), ORD_EQ)
        self.assertEqual(RULES[19].computation(523), ORD_GT)

    def test_20(self):
        self.assertEqual(RULES[20].computation(123), 1)
        self.assertEqual(RULES[20].computation(121), 2)
        self.assertEqual(RULES[20].computation(111), 3)

    def test_21(self):
        self.assertEqual(RULES[21].computation(123), False)
        self.assertEqual(RULES[21].computation(111), False)
        self.assertEqual(RULES[21].computation(121), True)
        self.assertEqual(RULES[21].computation(113), True)

    def test_22(self):
        self.assertEqual(RULES[22].computation(123), 1)
        self.assertEqual(RULES[22].computation(125), 1)
        self.assertEqual(RULES[22].computation(531), -1)
        self.assertEqual(RULES[22].computation(122), 0)

    def test_23(self):
        self.assertEqual(RULES[23].computation(123), ORD_EQ)
        self.assertEqual(RULES[23].computation(124), ORD_GT)

    def test_24(self):
        self.assertEqual(RULES[24].computation(123), 3)
        self.assertEqual(RULES[24].computation(423), 2)
        self.assertEqual(RULES[24].computation(135), 1)

    def test_25(self):
        self.assertEqual(RULES[25].computation(123), 3)
        self.assertEqual(RULES[25].computation(423), 2)
        self.assertEqual(RULES[25].computation(135), 1)
        self.assertEqual(RULES[25].computation(432), 3)
        self.assertEqual(RULES[25].computation(431), 2)
        self.assertEqual(RULES[25].computation(531), 1)

    def test_26(self):
        self.assertEqual(RULES[26].computation(123), [True, True, False])

    def test_27(self):
        self.assertEqual(RULES[27].computation(154), [True, False, False])

    def test_28(self):
        self.assertEqual(RULES[28].computation(123), [True, False, False])

    def test_29(self):
        self.assertEqual(RULES[29].computation(123), [False, False, True])

    def test_30(self):
        self.assertEqual(RULES[30].computation(143), [False, True, False])

    def test_31(self):
        self.assertEqual(RULES[31].computation(123), [False, True, True])

    def test_32(self):
        self.assertEqual(RULES[32].computation(124), [False, False, True])

    def test_33(self):
        self.assertEqual(RULES[33].computation(123), [1, 0, 1])

    def test_34(self):
        self.assertEqual(RULES[34].computation(123), [True, False, False])
        self.assertEqual(RULES[34].computation(112), [True, True, False])

    def test_35(self):
        self.assertEqual(RULES[35].computation(123), [False, False, True])
        self.assertEqual(RULES[35].computation(122), [False, True, True])

    # def test_36(self):
    #     self.assertEqual(RULES[36].computation(123), [])

    # def test_37(self):
    #     self.assertEqual(RULES[37].computation(123), [])

    # def test_38(self):
    #     self.assertEqual(RULES[38].computation(123), [])

    # def test_39(self):
    #     self.assertEqual(RULES[39].computation(123), [])

    # def test_40(self):
    #     self.assertEqual(RULES[40].computation(123), [])

    # def test_41(self):
    #     self.assertEqual(RULES[41].computation(123), [])

    # def test_42(self):
    #     self.assertEqual(RULES[42].computation(123), [])

    # def test_43(self):
    #     self.assertEqual(RULES[43].computation(123), [])

    # def test_44(self):
    #     self.assertEqual(RULES[44].computation(123), [])

    # def test_45(self):
    #     self.assertEqual(RULES[45].computation(123), [])

    # def test_46(self):
    #     self.assertEqual(RULES[46].computation(123), [])

    # def test_47(self):
    #     self.assertEqual(RULES[47].computation(123), [])

    # def test_48(self):
    #     self.assertEqual(RULES[48].computation(123), [])


if __name__ == "__main__":
    unittest.main()
