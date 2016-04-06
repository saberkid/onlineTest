# status
#               1:pre_test
#               2:being under test
#               3:after_test

class test():
    def __init__(self, pre_test=2, under_test= 5, after_test=3):
        self.pre_test = pre_test
        self.under_test = under_test
        self.after_test = after_test
        self.status = 1

