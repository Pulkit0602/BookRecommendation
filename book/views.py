from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pickle

# Create your views here.

popular_df = pickle.load(open("ML\popular.pkl","rb"))
df = pickle.load(open("ML\df.pkl","rb"))
similarity_score = pickle.load(open("ML\similarityScore.pkl","rb"))
books = pickle.load(open("ML\infobooks.pkl","rb"))


def index(request):    
    list1 = list(popular_df["Book-Title"].values)
    list2 = list(popular_df["Image-URL-M"].values)
    mylist = zip(list1, list2)
    
    return render(request, "index.html",  {"mylist":mylist})

def recommend(request):    
    list1 = list(popular_df["Book-Title"].values)
    list2 = list(popular_df["Image-URL-M"].values)
    mylist = zip(list1, list2)
    user_input = str(request.GET.get("user_input")) 
    #user_input = "1984"  
    print(user_input)

    if user_input != "None":                     
        #FROM IPYNB

        index = np.where(df.index == user_input)[0][0]
        
        recommend = sorted(list(enumerate(similarity_score[index])), key= lambda x: x[1] , reverse = True)[1:5]
        
        recommend_list = list(map(lambda x : x[0], recommend))
        
        
        recommend_list = df.index[recommend_list]
        
        item_book_title=[]
        item_book_author=[]
        item_image=[]
        for i in  recommend_list:        
            temp_df = books[books["Book-Title"] == i]
            item_book_title.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
            item_book_author.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
            item_image.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values)) 

    #-----------------------------------------------------------------------

        #Recommendation List
        reco1 = item_book_title
        reco2 = item_book_author
        reco3 = item_image

        reco = zip(reco1,reco2,reco3)
        return render(request, "recommendation.html",   {                                                    
                                                        "mylist":mylist,
                                                        "recommend": reco,
                                                        "user_input":user_input})

    else:
    #print(a)   
        return render(request, "recommendation.html",   {                                                    
                                                       "mylist":mylist
                                                        })

def bookInfo(request,name): 

    info=[]
    #print(name)
    
    temp_df = books[books["Book-Title"] == name]
    info.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
    info.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
    info.extend(list(temp_df.drop_duplicates("Book-Title")["Year-Of-Publication"].values)) 
    info.extend(list(temp_df.drop_duplicates("Book-Title")["Publisher"].values)) 
    info.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))     
    #print(info) 

    list1 = list(popular_df["Book-Title"].values)
    list2 = list(popular_df["Image-URL-M"].values)
    mylist = zip(list1, list2)

    
    return render(request, "book_info.html",{"mylist":mylist , "info":info})

