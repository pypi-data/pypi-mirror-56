import unittest

import stepio

class BasicTest(unittest.TestCase):
    def test_programming_project_input_line(self):

        Input = 'programmer person-days: 10~12@50usd; analyst person-days: 11~45@45usd; software package: 1@159.99usd'

        Result = [{u'programmer person-days':
                     {'max_units': u'12',
                          'min_units': u'10',
                          'price_unit': u'usd',
                          'f_units': '',
                          'min_price': u'50',
                          'f_price': '',
                          'max_price': u'50'}
                     },
                    {u'analyst person-days':
                         {'max_units': u'45',
                              'min_units': u'11',
                              'price_unit': u'usd',
                              'f_units': '',
                              'min_price': u'45',
                              'f_price': '',
                              'max_price': u'45'}
                       },
                    {u'software package':
                         {'max_units': u'1',
                              'min_units': u'1',
                              'price_unit': u'usd',
                              'f_units': '',
                              'min_price': u'159.99',
                              'f_price': '', 'max_price': u'159.99'}}]

        self.assertEqual(stepio.parse(Input), Result)

    def test_construction_project_output_line(self):
        Output = 'complete solar assembly drawings: 0~1; solar cell assemblies: 1~2[exp(x)]@5.5~5.9[beta(2,2)((x-a)/(b-a))]h'

        Result = [{u'complete solar assembly drawings':
                       {'max_units': u'1',
                            'min_units': u'0',
                            'price_unit': u'',
                            'f_units': '',
                            'min_price': u'',
                            'f_price': u'',
                            'max_price': u''}},
                    {u'solar cell assemblies':
                         {'max_units': u'2',
                              'min_units': u'1',
                              'price_unit': u'h',
                              'f_units': u'exp(x)',
                              'min_price': u'5.5',
                              'f_price': u'beta(2,2)((x-a)/(b-a))',
                              'max_price': u'5.9'}}]

        self.assertEqual(stepio.parse(Output), Result)

if __name__ == '__main__':
    unittest.main()
