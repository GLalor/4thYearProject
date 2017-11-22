import unittest
import optionChainRetrieval

class unitTestReadlist(unittest.TestCase):
    def test_call_payoff(self):
        result = optionChainRetrieval.call_payoff(20,20)
        self.assertEqual(0.0 , result)

    def test_put_payoff(self):
        result = optionChainRetrieval.put_payoff(20,20)
        self.assertEqual(0.0 , result)
    
    def test_sim_option_price_call(self):
        result = optionChainRetrieval.sim_option_price(1,50,2.1024,.367,70,77,"Call")
        self.assertEqual(1.9218778063361091e+65 , result)
    def test_sim_option_price_put(self):
        result = optionChainRetrieval.sim_option_price(1,50,2.1024,.367,70,77,"Put")
        self.assertEqual(0.0 , result)
if __name__ == '__main__':
    unittest.main()