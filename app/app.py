import streamlit as st
import preprocess ,helper
import matplotlib.pyplot as plt
import seaborn as sns




st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocess.preprocessor(data)

    



# fetching user dropdown
    user_list = df['user'].unique().tolist()
    remove_set = {
    "group_notification",
    "Follow this link to join my WhatsApp group",
    "POLL",
    "Meta AI",
    "Fill out the Google form below to register and secure your spot"
}

    user_list = [u for u in user_list if u not in remove_set]

    user_list.sort()
    user_list.insert(0,"overall")
    selected_users = st.sidebar.selectbox('show analysis wrt' , user_list)
    

    if st.sidebar.button("show analysis"):
        st.title('General stats')
        col1, col2, col3, col4 = st.columns(4)
        num_messages , words , media , links= helper.fetch_stats(selected_users,df)

        with col1:
            st.header('Total messages')
            st.title(num_messages)
        with col2:
            st.header('number of words')
            st.title(words)
        with col3:
            st.header('media shared')
            st.title(media)
        with col3:
            st.header('links shared')
            st.title(links)
        pass

    # monthly timeline
        st.title('monthly timeline')
        timeline = helper.monthly_timeline(selected_users , df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'] , timeline['message'],color='purple')
        plt.xticks(rotation = "vertical" )
        st.pyplot(fig)

    # daily timeline
        st.title('daily timeline')
        daily_timeline = helper.daily_timeline(selected_users,df)
        
        fig ,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'] , daily_timeline['message'],color='green')
        plt.xticks(rotation = "vertical" )
        st.pyplot(fig)

    
    # activity map
        st.title('Activity map')

        col1 , col2 = st.columns(2)

        with col1: # daily activity
           st.header('Most busy day')
           busy_day = helper.week_activity_map(selected_users,df)

           fig ,ax = plt.subplots()
           ax.bar(busy_day.index,busy_day.values,color='orange')
           plt.xticks(rotation = "vertical" )
           st.pyplot(fig)
        
        with col2:# monthly activity 
           st.header('Most busy month')
           busy_month = helper.month_activity_map(selected_users,df)

           fig ,ax = plt.subplots()
           ax.bar(busy_month.index,busy_month.values,color='yellow')
           plt.xticks(rotation = "vertical" )
           st.pyplot(fig)
        
        # activity heatmap
        st.header('users activity heatmap')
        user_heatmap = helper.activity_heatmap(selected_users,df)
        
        fig, ax = plt.subplots(figsize=(20, 6))
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



    # most busy users
       
        if selected_users == 'overall':
          x  ,new_df = helper.most_busy_users(df)
          fig , ax = plt.subplots()
       
          col1 , col2 = st.columns(2)

          with col1 :
            st.title('Most busy users')
            ax.bar(x.index , x.values , color = 'red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
          with col2 :
            st.dataframe(new_df)

    
    

    # wordcloud
        st.title("wordcloud")
        df_wc = helper.create_wordcloud(selected_users , df)
        fig , ax = plt.subplots()   
        ax.axis("off")
        ax.imshow(df_wc)
        st.pyplot(fig)


    # most commmon words
        st.title("most common words")
        most_common_df = helper.most_common_words(selected_users , df)
        fig , ax = plt.subplots()
        ax.barh(most_common_df[0] , most_common_df[1])
        
        st.pyplot(fig)
       


    # emoji analysis
        emoji_df = helper.emoji_analyzer(selected_users,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
        
