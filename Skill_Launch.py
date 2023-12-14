import Weather as w
import AI_News4 as ai
import Voice_Tools3 as v
import Ukraine_News as uk
import Custom_News2 as cn
import Training_Optimizer5 as p

def Check_If_Skill(question):
    skills = []
    skills.append('weather')
    skills.append('AI news')
    skills.append('ukraine')
    skills.append('news')
    skills.append('prediction')
    skills.append('good morning')

    if v.Phrase_Exists(question, 'weather'):
        if 'weather' in skills:
            print('weather found')
            return True
    elif v.Phrase_Exists(question, 'AI news'):
        if 'AI news' in skills:
            print('ai news found')
            return True
    elif v.Phrase_Exists(question, 'ukraine'):
        if 'ukraine' in skills:
            print('ukraine news found')
            return True
    elif v.Phrase_Exists(question, 'news'):
        if 'news' in skills:
            print('other news found')
            return True
    elif v.Phrase_Exists(question, 'prediction'):
        if 'prediction' in skills:
            print('market prediction analysis launched')
            return True
    elif v.Phrase_Exists(question, 'good morning'):
        if 'prediction' in skills:
            print('good morning launched')
            return True
    return False

def Run_Skill(quest):
    if v.Phrase_Exists(quest,'weather') == True:
        print("running weather" )
        w.Present_Weather()
    elif v.Phrase_Exists(quest,'AI news') == True:
        print("running ai news" )
        ai.Present_AInews()
    elif v.Phrase_Exists(quest,'ukraine') == True:
        print("running ukraine" )
        uk.Present_Ukrainenews()
    elif v.Phrase_Exists(quest, 'news') == True:
        print("running other news")
        cn.get_news_summaries(quest)
    elif v.Phrase_Exists(quest, 'prediction') == True:
        print("running market prediction")
        p.Predict_SPY()
    else:
        print("running custom" )
        cn.get_news_summaries(quest)
        return