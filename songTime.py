from os import system
from datetime import datetime

def human_time(datetime_obj=datetime.now()):
    
    hr = int(datetime_obj.hour)
    mi = int(datetime_obj.minute)
    
    singles = ["one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine","ten", "eleven","twelve"]
    teens = ["ten", "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
    tens = ["twenty","thirty", "forty","fifty"]
    
    if(mi==0):
        human_str = singles[hr-1]
    else:
        div = mi / 10
        if(mi<10):
            human_str = singles[hr-1] + " oh " + singles[mi-1]
        if(div==1):
            human_str = singles[hr-1] +" "+ teens[mi-10] 
        else:
            rem = mi%10
            human_str = singles[hr-1] +" "+ tens[div-2] +" "+ singles[rem-1]

    return human_str

current=human_time()

system('say -v Victoria The current time is '+current)
# system("say -v Victoria it is currently `date +%H%M`")