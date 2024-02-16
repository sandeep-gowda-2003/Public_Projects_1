import pandas as pd
import numpy as np
import ast
from pyscript import document


def recommender():
    # print("HII")
    seac=document.querySelector('#box')
    search_movie=seac.value
    df_movies=pd.read_csv('../resources/tmdb_5000_credits.csv')
    df_credits=pd.read_csv('../resources/tmdb_5000_movies.csv')

    df_movies=df_movies.merge(df_credits)

    # print(df_movies.shape)
    # print(df_movies.tagline)


    df_movies.drop(['budget','homepage','original_title','popularity','original_language','production_countries','production_companies','runtime','release_date','revenue','spoken_languages','status','tagline','vote_average','vote_count','movie_id'],axis=1,inplace=True)

    print(df_movies.columns)

    # for i in df_movies.columns:
    #     print(df_movies.loc[:,i].isnull().sum())

    df_movies.dropna(inplace=True)

    print(df_movies.duplicated().sum())

    def convert(obj):
        l=[]
        for i in ast.literal_eval(obj):
            l.append(i['name'])
        return l



    def fetch_director(obj):
        l=[]
        for i in ast.literal_eval(obj):
            if i['job']=='Director':
                l.append(i['name'])
                break
        return l


    def cast_convert(obj):
        l=[]
        c=0
        for i in ast.literal_eval(obj):
            c+=1
            if c==4:
                break
            l.append(i['name'])
        return l



    # convert(df_movies.genres[0])
    df_movies['genres']=df_movies['genres'].apply(convert)


    df_movies['keywords']=df_movies['keywords'].apply(convert)

    df_movies.cast=(df_movies.cast.apply(cast_convert))

    df_movies.crew=(df_movies.crew.apply(fetch_director))

    df_movies.overview=(df_movies.overview.apply(lambda x:x.split()))

    df_movies.genres=df_movies.genres.apply(lambda x: [i.replace(' ','') for i in x])
    df_movies.keywords=df_movies.keywords.apply(lambda x: [i.replace(' ','') for i in x])
    df_movies.cast=df_movies.cast.apply(lambda x: [i.replace(' ','') for i in x])
    df_movies.crew=df_movies.crew.apply(lambda x: [i.replace(' ','') for i in x])


    df_movies['tags']=df_movies.overview+df_movies.genres+df_movies.keywords+df_movies.cast+df_movies.crew

    df_movies['tags']=df_movies['tags'].apply(lambda x:' '.join(x))

    df_movies['tags']=df_movies['tags'].apply(lambda x:x.lower())

    df_movies['title']=df_movies['title'].apply(lambda x:x.upper())

    # print(df_movies.tags[0])


    from nltk.stem.porter import PorterStemmer
    ps=PorterStemmer()

    def stem(text):
        l=[]
        # print(type(text))
        for i in text.split():
            l.append(ps.stem(i))
        return ' '.join(l)

    from sklearn.feature_extraction.text import CountVectorizer

    cv=CountVectorizer(max_features=5000,stop_words='english')

    print(df_movies['tags'])

    vector=cv.fit_transform(df_movies['tags'].apply(stem)).toarray()

    # print(cv.get_feature_names_out())
    # print(vector)

    from sklearn.metrics.pairwise import cosine_similarity

    similarity=cosine_similarity(vector)
    print(similarity[0])
    # print(sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1]))

    def recommend(movie_name):
        movie_list=[]
        index=df_movies[df_movies.title==movie_name].index[0]
        movie_suggested=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])[0:7]
        # print(movie_suggested)
        for i in movie_suggested:
            # print((df_movies.title.iloc[i[0]]))
            movie_list.append((df_movies.title.iloc[i[0]]))
        return movie_list

    return recommend(search_movie.upper())

if __name__=='__main__':
    recommender()


