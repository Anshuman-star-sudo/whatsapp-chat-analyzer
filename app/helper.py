from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns



extractor = URLExtract()
def fetch_stats(selected_users  , df):
    if selected_users != 'overall':
       df = df[df['user'] == selected_users]


    # fetching no of messages
    num_messages = df.shape[0]


     # fetching no of words
    words = []
    for i in df['message']:
         words.extend(i.split())


    # fetching no of media sent
    num_media = df[df['message'] == "<Media omitted>\n"].shape[0]


    # fetching links sent 
    links = []
    for i in df['message']:
     links.extend(extractor.find_urls(i))
    links_sent = len(links)
    
    return  num_messages ,len(words) , num_media , links_sent

# most busy users on group
def most_busy_users(df):
   x = df['user'].value_counts().head()
   new_df = round((df['user'].value_counts() / df['user'].shape[0])*100 , 2).reset_index().rename(columns={'count':'percent'})
   return x , new_df 


#wordcloud
def create_wordcloud(selected_users , df):
    f = open('stop_hinglish.txt' , 'r')
    stop_words  = f.read()
    if selected_users != 'overall':
       df = df[df['user'] == selected_users]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]

    def remove_stop_words(message):
       y = []
       for word in message.lower().split():
          if word not in stop_words:
             y.append(word)
       return " ".join(y)

   
    wc = WordCloud(width = 400 ,
                   height=400 ,
                   max_font_size=100 ,
                  background_color = 'white')
    
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep =" "))
    return df_wc

# most commmon words
def most_common_words(selected_users,df):
   if selected_users != 'overall':
       df = df[df['user'] == selected_users]
   temp = df[df['user'] != 'group_notification']
   temp = temp[temp['message'] != "<Media omitted>\n"]

   f = open('stop_hinglish.txt' , 'r')
   stop_words  = f.read()
   words = [] 

   for message in temp['message']:
     for word in message.lower().split():
         if word  not in stop_words:
            words.append(word) 

   most_common_df = pd.DataFrame(Counter(words).most_common(20))
   return most_common_df


# emoji analysis 
def emoji_analyzer(selected_users , df):
   if selected_users != 'overall':
       df = df[df['user'] == selected_users]
   
   emojis =[]

   for message in df['message']:
      emojis.extend([e['emoji'] for e in emoji.emoji_list(message)])
   

   emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
   return emoji_df
    
# monthly timeline
def monthly_timeline(selected_users,df ):
   if selected_users != 'overall':
       df = df[df['user'] == selected_users]
   
   timeline = df.groupby(['year' , 'month' , 'month_num' ]).count()['message'].reset_index()
   time=[]
   for i in range(timeline.shape[0]):
    time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
   timeline['time'] = time

   return timeline


# daily timeline
def daily_timeline(selected_users , df):
   if selected_users != 'overall':
       df = df[df['user'] == selected_users]

   daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
   
   return daily_timeline


def week_activity_map(selected_users , df):
    if selected_users != 'overall':
       df = df[df['user'] == selected_users]
    
    return df['day_name'].value_counts() 


def month_activity_map(selected_users , df):
   if selected_users != 'overall':
       df = df[df['user'] == selected_users]
    
   return df['month'].value_counts()

def activity_heatmap(selected_users ,df):
   if selected_users != 'overall':
       df = df[df['user'] == selected_users]
   
   day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
             'Friday', 'Saturday', 'Sunday']

   period_order = sorted(df['period'].unique(),
                      key=lambda x: int(x.split('-')[0]))
   
   pivot = df.pivot_table(
    index='day_name',
    columns='period',
    values='message',
    aggfunc='count'
    ).fillna(0)

   user_heatmap = pivot.reindex(day_order).reindex(columns=period_order)
   return user_heatmap
   
