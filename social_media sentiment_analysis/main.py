import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

df=pd.read_csv('resources/Tweets.csv')

print(df.iloc[5,:])

cv=CountVectorizer(stop_words='english')
ps=PorterStemmer()


df.dropna(axis=0,inplace=True)
print(df['text'].isna().sum())

df['text']=df['text'].apply(lambda x: x.lower())

def cleaned_data(x):
    st=[]
    for i in x.split(' '):
        st.append(ps.stem(i))
    return " ".join(st)


matrix=cv.fit_transform(df.text.apply(cleaned_data)).toarray()
print(cv.get_feature_names_out())
print(matrix)

MN=MultinomialNB()

MN.fit(matrix,df['sentiment'])


def clean_test(x):
    x=x.lower()
    # if x.isnull().sum()!=0:
    #     x.dropna(axis=0,inplace=True)
    print(x)
    return x


while True:
    x_test=input('ENTER THE TEXT: ')

    x_test=(clean_test(x_test))
    x_test=pd.Series(x_test)
    test_matrix=cv.transform(x_test.apply(cleaned_data)).toarray()

    print(MN.predict(test_matrix))
    
    ex=int(input("ENTER '1' TO EXIT OR '0' TO CONTINUE: "))

    if ex==1:
        break