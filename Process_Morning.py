import AI_News4 as ai
import Weather as w
import Ukraine_News as u
import Voice_Tools3 as v
import Custom_News2 as cn
import Training_Optimizer5 as t
import datetime as d

v.Get_Answer('Wish me good morning', 'morning', 'silent')
v.Get_Answer('Tell me a random motivational quote', 'motivate', 'silent')
v.Get_Answer('Tell me a random joke', 'joke', 'silent')
ai.Present_AInews('ainews','silent')
w.Present_Weather('weather','silent')
u.Present_Ukrainenews('ukrainenews', 'silent')
cn.present_custom_news('ai tools', 'custom', 'silent')
today = d.date.today()
today_formatted = today.strftime("%A, %B %d")
currday = today_formatted
currpredict = str(t.Predict_SPY())
spyscript = 'For today ' + currday + ' the prediction is that there is a ' + currpredict + ' percent probability that the SPY index will be 5% higher four weeks from today.'
v.Play_Prompt(spyscript, 'spy', 'silent')

