import sys


class AnalysisRunner():
    def run(self):
        arg_len = len(sys.argv)
        if arg_len == 1:
            self.run_english()
            self.run_chinese()
        else:
            if '--english' in sys.argv:
                self.run_english()
            if '--chinese' in sys.argv:
                self.run_chinese()

    def run_english(self):
        pass

    def run_chinese(self):
        pass
