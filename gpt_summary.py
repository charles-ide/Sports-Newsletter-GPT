'''
(c) 2023 Charles Ide
This module is used to access OpenAI's API
'''

import openai
import os

# A function that takes the text of an article and returns a ChatGPT summary
# TODO: Refactor our prompt engineering into a separate module
def summarize_text(article_text):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    print(article_text)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": "For the following article text, I want you to generate a 4 to 6 word shortened article title and a 4 to 5 sentence summary of the article. \
            I also want you to classify the sport the article is discussing. \
                \n\nReturn your response in the format:\nTitle - \nSport - \nSummary - \n\n\nText -  " + article_text
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    sample_text = "PARIS (AP) — Paris Saint-Germain’s highly-rated teenager Warren Zaïre-Emery was called up by France coach Didier Deschamps for the first time on Thursday.Aged 17, the PSG academy product has been in impressive form since the start of the season despite intense competition in midfield at his club.He has scored two goals and delivered two assists in 10 league matches, and caught the eye last month on Europe’s biggest stage with two assists as PSG beat AC Milan 3-0 in the Champions League.“He’s here with us because he’s got what it takes to perform at the very highest level, even if there is competition at his position,” Deschamps said. “What he is capable of achieving with his club at such a young age shows an enormous potential and maturity.”Other newsMan United manager Ten Hag under more pressure as international break loomsMourinho and Sarri exchange jibes ahead of Rome derby in Serie AWorld Cup semifinalist Morocco recruits France U21 player Diop to start qualifying for 2026 editionZaïre-Emery has been called up for upcoming European qualifiers against Gibraltar and Greece. France is already qualified for next year’s tournament in Germany and will look to secure top spot in Group B.France hosts Gibraltar on Nov. 18 in the city of Nice and then takes on Greece in Athens three days later.Before his first call-up for the senior team, Zaïre-Emery had captained the under-21 team managed by former France and Arsenal great Thierry Henry.Former PSG coach Christophe Galtier gave Zaïre-Emery his French league debut last season when he became the youngest player in the club’s history.The teenager joined PSG’s youth academy in 2014 and won the Euros with the France under-17 team.He was included in Deschamps’ 23-man squad in the absence of injured Real Madrid midfielder Aurelien Tchouameni, but the Francem coach said he could have been on the list anyway.___France squad:Goalkeepers: Alphonse Areola (West Ham), Mike Maignan (AC Milan), Brice Samba (Lens)Defenders: Jonathan Clauss (Marseille), Lucas Hernandez (PSG), Theo Hernandez (AC Milan), Ibrahima Konate (Liverpool), Jules Kounde (Barcelona), William Saliba (Arsenal), Jean-Clair Todibo (Nice), Dayot Upamecano (Bayern Munich)Midfielders: Eduardo Camavinga (Real Madrid), Youssouf Fofana (Monaco), Boubacar Kamara (Aston Villa), Adrien Rabiot (Juventus), Warren Zaïre-Emery (PSG)Forwards: Kingsley Coman (Bayern Munich), Ousmane Dembele (PSG), Olivier Giroud (AC Milan), Antoine Griezmann (Atletico Madrid), Randal Kolo Muani (PSG), Kylian Mbappe (PSG), Marcus Thuram (Inter Milan)___More AP soccer:https://apnews.com/hub/soccerandhttps://twitter.com/AP_Sports"
    response_summary = summarize_text(sample_text)
    print(response_summary)
