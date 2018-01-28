from AnalysisLib.ProcessFile import scale_database
from ReadParameterFile import get_parameter_dict
import re
param = get_parameter_dict()

#storing words to rate the attitude scale
#att_scale1_words = scale_database(param['political.attitudes.scale'] + "/scale1.txt")
#att_scale2_words = scale_database(param['political.attitudes.scale'] + "/scale2.txt")
#att_scale3_words = scale_database(param['political.attitudes.scale'] + "/scale3.txt")

#storing words to rate the perception scale
#percep_scale1_words = scale_database(param['policies.perception.scale'] + "/scale1.txt")
#percep_scale2_words = scale_database(param['policies.perception.scale'] + "/scale2.txt")
#percep_scale3_words = scale_database(param['policies.perception.scale'] + "/scale3.txt")
#percep_scale4_words = scale_database(param['policies.perception.scale'] + "/scale4.txt")
#percep_scale5_words = scale_database(param['policies.perception.scale'] + "/scale5.txt")

#storing words to rate the popularity scale
#popular_words = scale_database(param['popular.political'] + "/popular.txt")
#not_popular_words = scale_database(param['popular.political'] + "/notpopular.txt")
def search_scale(category, num, sentence, _language = 'both'): #pass the sentence to be interpreted in database
    #print(texts)
    #storing words to rate the attitude scale
    
    att_scale1_words = scale_database(param['political.attitudes.scale'] + "/scale1.txt")
    att_scale2_words = scale_database(param['political.attitudes.scale'] + "/scale2.txt")
    att_scale3_words = scale_database(param['political.attitudes.scale'] + "/scale3.txt")
    
    #storing words to rate the perception scale
    percep_scale1_words = scale_database(param['policies.perception.scale'] + "/scale1.txt")
    percep_scale2_words = scale_database(param['policies.perception.scale'] + "/scale2.txt")
    percep_scale3_words = scale_database(param['policies.perception.scale'] + "/scale3.txt")
    percep_scale4_words = scale_database(param['policies.perception.scale'] + "/scale4.txt")
    percep_scale5_words = scale_database(param['policies.perception.scale'] + "/scale5.txt")
 
    #storing words to rate the popularity scale
    popular_words = scale_database(param['popular.political'] + "/popular.txt")
    not_popular_words = scale_database(param['popular.political'] + "/notpopular.txt")
    
    #storing words to rate the polarity scale
    if _language == "english":
        pos_words = scale_database(param['polarity.political'] + "/english_positive.txt")
        neg_words = scale_database(param['polarity.political'] + "/english_negative.txt")
    elif _language == "chinese":
        pos_words = scale_database(param['polarity.political'] + "/chinese_positive.txt", "chinese")
        neg_words = scale_database(param['polarity.political'] + "/chinese_negative.txt", "chinese")
    elif _language == 'both':
        pos_words = scale_database(param['polarity.political'] + "/positive.txt")
        neg_words = scale_database(param['polarity.political'] + "/negative.txt")

    #sentence_list = texts.split('.')
    #for sentence in sentence_list:
    if category == "Attitude":
        if num == 1:
            for words in att_scale1_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
                
        elif num == 2:
            for words in att_scale2_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
        elif num == 3:
            for words in att_scale3_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
                
    elif category == "Perception":
        if num == 1:
            for words in percep_scale1_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
        elif num == 2:
            for words in percep_scale2_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
        elif num == 3:
            for words in percep_scale3_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
        elif num == 4:
            for words in percep_scale4_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
        elif num == 5:
            for words in percep_scale5_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
                
    elif category == "Popularity":
        if num == 1:
            for words in popular_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
        elif num == 2:
            for words in not_popular_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
                
    elif category == "Polarity":
        if num == 1:
            for words in neg_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True
        elif num == 2:
            for words in pos_words:
                words = words.replace(" ",".*")
                p = re.compile(words)
                if p.search(sentence):
                    return True  
    return False