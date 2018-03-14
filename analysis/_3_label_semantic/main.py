from analysis.libs.AnalysisRunner import AnalysisRunner
from analysis._3_label_semantic.for_chinese import for_chinese
from analysis._3_label_semantic.for_english import for_english

DATE = '20180313_'
class LabelSemantics(AnalysisRunner):
    def run_english(self):
        for_english(DATE)
    def run_chinese(self):
        for_chinese(DATE)

LabelSemantics().run()