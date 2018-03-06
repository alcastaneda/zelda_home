from os import system
from datetime import datetime

def human_time(datetime_obj=datetime.now()):
    
    hr = int(datetime_obj.hour)
    mi = int(datetime_obj.minute)
    tod = " a m"

    singles = ["one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine","ten", "eleven","twelve"]
    teens = ["ten", "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
    tens = ["twenty","thirty", "forty","fifty"]
    
    if(hr>12):
        hr = hr-12
        tod = " p m"
    if(mi==0):
        human_str = singles[hr-1]
    else:
        div = mi / 10
        if(mi<10):
            human_str = singles[hr-1] + " oh " + singles[mi-1]+tod
        if(div==1):
            human_str = singles[hr-1] +" "+ teens[mi-10]+tod 
        else:
            rem = mi%10
            human_str = singles[hr-1] +" "+ tens[div-2] +" "+ singles[rem-1]+tod

    return human_str


# for MAC
# system('say -v Victoria The current time is '+human_time())
system('say The current time is '+human_time())