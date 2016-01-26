__author__ = 'shako'

class SimpleParser(object):
    keyword_dict_lv0 = {"ERROR": 10, "Error": 8}
    keyword_dict_lv1 = {"Gecko": 6, "Javascript": 4}
    parsing_result =[]

    def parse_data(self, input_data_path):
        with open(input_data_path) as f:
            for strLine in f.readlines():
                for keyword in self.keyword_dict_lv0:
                    if keyword in strLine:
                        tmp_result = {'stdLog': strLine,
                                      'score': self.keyword_dict_lv0[keyword]}
                        for keyword2 in self.keyword_dict_lv1:
                            if keyword2 in strLine:
                                tmp_result['score'] += self.keyword_dict_lv1[keyword2]
                        self.parsing_result.append(tmp_result)

    def output_data(self, output_data_path):
        writting_data = []
        for data in self.parsing_result:
            if data['score'] >= 8:
                writting_data.append(data['stdLog'])
        with open(output_data_path, "w+") as f:
            f.writelines(writting_data)
