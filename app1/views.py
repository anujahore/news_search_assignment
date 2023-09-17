import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from app1.models import Article_Source, Articles_db

# Create your views here.

API_KEY = "a5d4e2b329c24a14a4b8f30a67b7ff80"


# GIVEN_URL = r"https://newsapi.org/v2/everything?q=tesla&from=2023-08-13&sortBy=publishedAt&apiKey=a5d4e2b329c24a14a4b8f30a67b7ff80"
# GIVEN_URL = f"https://newsapi.org/v2/top-headlines/sources?apiKey={API_KEY}"
# GIVEN_URL = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}"

def storing_data_fun(all_articles, key_word, user):
    '''
    this function is to store the results in back-end
    '''

    for article in all_articles:
        # print(article['author'], "="*10)
        author = article['author']
        title = article['title']
        description = article['description']
        url = article['url']
        urlToImage = article['urlToImage']
        publishedAt = article['publishedAt']
        content = article['content']
        article_sourse = article['source']
        source_name = article_sourse['name']
        source_id = article_sourse['id']
        
        # creating Article_Source object
        article_source = Article_Source.objects.create(new_id=source_id, name=source_name)

        # creating articles_db object
        article_db = Articles_db.objects.create(author=author,title=title,description=description,
                                   url=url, urlToImage=urlToImage,publishedAt=publishedAt,
                                   content=content, key_word=key_word, source=article_source,  users=user)
        
        
def sorting_by_publishedAt(all_articles):
    """
    This function is to sort articles by published-date and in desending ording
    """
    lst = all_articles #list of dict
    sorted_articles_publishedat = sorted(lst, 
                                         key=lambda x: x['publishedAt'], reverse=True)
    return sorted_articles_publishedat

def get_last_publishedat(all_articles):
    """
    This function is to get the lattest article searched by user
    sorting articles on the basis of published date and in desending order
    """
    sorted_article_first = Articles_db.objects.first()
    lattest_published_date = sorted_article_first.publishedAt
    return lattest_published_date
    
    
def find_time_difference(all_articles):
    """
    This function is to get the time diff between time when user refresh the query and the time stored in database
    user_search_time -- time stored in databse when user 1st search the query
        -- its in UST timezone
        -- this is auto_now_add=True 
    current_time_django -- current time (utc) 
        -- its provided by django 
        -- imported from django.utils import timezone
    """
    for article in all_articles:
        article_search_time_utc = article.user_search_time
        # print(article_search_time_utc, '----', article.publishedAt)
        
    current_time_django = timezone.now()
    print(article_search_time_utc, "db------------- time ")
    print(current_time_django, "currenttime--- django")
    # print("django_timezon-----", timezone.now())
    time_difference = current_time_django - article_search_time_utc
    return time_difference
   

def get_user_search_keywords(user_search_articles):
    """
    This Function is to get all the keywords search by th perticular user
    In this function we are passing all the list of articles seached by the user
    and thif function will eliminat duplicate keywords pass by user and
    return the unique list of keywords search by perticular user
    """
    keywords_lst = []
    for article in user_search_articles:
        if article.key_word not in keywords_lst:
            keywords_lst.append(article.key_word)
        else:
            continue
    return keywords_lst


        
def home(req):
    '''
    This function is to see all posts in given api
    if user is authenticated then only he is able to access home page
    
    user can search on basis of country, category and keyword=news_title
    
    while refreshing the page the api will not be called, the result which are stored in databse table
    for perticular user will be fetch and showed in frond-end
    '''
    if req.user.is_authenticated:
        country = req.GET.get('country')
        category = req.GET.get('category')
        news_title = req.GET.get('q')
        all_articles = None
        result_count = 0
        user = User.objects.get(id=req.user.id)
        # print(user)
        user_search_articles = user.articles_db_set.all()
        user_keywords = get_user_search_keywords(user_search_articles)
        print(user_keywords)
        
        if country:
            query_sets = user_search_articles #to check whether data exists in database or not
            if query_sets:
                all_articles = query_sets
                get_last_published_date = get_last_publishedat(all_articles=all_articles)
                # print("in querysets ----")
                time_difference = find_time_difference(all_articles=all_articles)
                # print(time_difference, time_difference.total_seconds()//60, "total_seconds:=",time_difference.total_seconds())
                if (time_difference.total_seconds() // 60) <= 15:
                    all_data = query_sets
                    result_count = len(list(all_data))
                    print("in time diff  source  -----------")
                    return render(req, "home.html", context={"all_articals": all_data, "result_count": result_count, "user_keywords":user_keywords})
                else:
                    print("in else -- contry ---- ")
                    GIVEN_URL = f"https://newsapi.org/v2/top-headlines?country={country}&from={get_last_published_date}&sort_by=publishedAt&apiKey={API_KEY}"
            
            else:
                # GIVEN_URL = f"https://newsapi.org/v2/everything?country={country}&sort_by=publishedAt&apiKey={API_KEY}"
                GIVEN_URL = f"https://newsapi.org/v2/top-headlines?country={country}&sort_by=publishedAt&apiKey={API_KEY}"
            response = requests.get(GIVEN_URL)
            data = response.json()
            try:
                all_articles = data['articles']
                result_count = len(all_articles)
            except Exception as error:
                return JsonResponse({"error": "not having any articles"})
            
            # sorting of articles on publishedAt
            all_articles = sorting_by_publishedAt(all_articles=all_articles)
            storing_data_fun(all_articles=all_articles, key_word=country, user=user)
            
        elif category:
            # query_sets = Articles_db.objects.exists() #to check whether data exists in database or not
            query_sets = user_search_articles
            if query_sets:
                all_articles = query_sets
                # time_diff = find_time_difference(all_articles=all_articles)
                # print(time_diff,"======================================")
                get_last_published_date = get_last_publishedat(all_articles=all_articles)
                time_difference = find_time_difference(all_articles=all_articles)
                print(time_difference, time_difference.total_seconds()//60, "total_seconds:=",time_difference.total_seconds())
                if (time_difference.total_seconds() // 60) <= 15:
                    # all_data = Articles_db.objects.all()
                    all_data = query_sets
                    result_count = len(list(all_data))
                    print("in time diff categpory -- -----------")
                    return render(req, "home.html", context={"all_articals": all_data, "result_count": result_count, "user_keywords":user_keywords})
                
                else:
                    print("in else -- category ---- ")
                    GIVEN_URL = f"https://newsapi.org/v2/top-headlines?category={category}&from={get_last_published_date}&sort_by=desc(publishedAt)&apiKey={API_KEY}"
            
            else:
                GIVEN_URL = f"https://newsapi.org/v2/top-headlines?category={category}&sort_by=desc(publishedAt)&apiKey={API_KEY}"
                # GIVEN_URL = f"https://newsapi.org/v2/everything?category={category}&sort_by=publishedAt&apiKey={API_KEY}"
                # {"status":"error","code":"parameterInvalid","message":"The category param is not currently supported on the /everything endpoint."}
            
            response = requests.get(GIVEN_URL)
            data = response.json()
            all_articles = data['articles']
            result_count = len(all_articles)
            all_articles = sorting_by_publishedAt(all_articles=all_articles)
            storing_data_fun(all_articles=all_articles, key_word=category, user=user)
            
        elif news_title:
            # query_sets = Articles_db.objects.exists() #to check whether data exists in database or not
            query_sets = user_search_articles.filter(key_word=news_title, users=user)
            query_source_name = req.GET
            print(query_source_name, "=/"*101)
            if query_sets:
                all_articles = query_sets
                get_last_published_date = get_last_publishedat(all_articles=all_articles)
                print("in querysets ----")
                time_difference = find_time_difference(all_articles=all_articles)
                print(time_difference, time_difference.total_seconds()//60, "total_seconds:=",time_difference.total_seconds())
                if (time_difference.total_seconds() // 60) <= 15:
                    all_data = query_sets.filter(key_word=news_title, users=user)
                    result_count = len(list(all_data))
                    print("in time diff News Tile --- q -----------")
                    return render(req, "home.html", context={"all_articals": all_data, "result_count": result_count, "query": news_title,  "user_keywords":user_keywords})
                
                else:
                    print("in else ----- news title -----")
                    GIVEN_URL = f"https://newsapi.org/v2/everything?q={news_title}&from={get_last_published_date}&sort_by=desc(publishedAt)&apiKey={API_KEY}"
            
            else:
                # url for all top-headlines
                # GIVEN_URL = f"https://newsapi.org/v2/top-headlines?q={news_title}&sort_by=publishedAt&apiKey={API_KEY}"
                # url for getting everything but only applicable for query and not for contry or category
                GIVEN_URL = f"https://newsapi.org/v2/everything?q={news_title}&sort_by=desc(publishedAt)&apiKey={API_KEY}"
            
            response = requests.get(GIVEN_URL)
            data = response.json()
            all_articles = data['articles']
            result_count = len(all_articles)
            all_articles = sorting_by_publishedAt(all_articles=all_articles)
            storing_data_fun(all_articles=all_articles, key_word=news_title, user=user)
            
        return render(req, "home.html", context={"all_articals": all_articles, "query": news_title, "result_count": result_count,  "user_keywords":user_keywords})
    
    else:
        return redirect("login")


def signup_view(request):
    """
    This function is for signup page
    here user is created
    """
    if request.method == 'POST':
        print(request.POST,'+'*101)
        signup_form = UserCreationForm(request.POST)
        print(signup_form.error_messages)
        if signup_form.is_valid():
            print("validddd")
            signup_form.save()
            messages.success(request=request, message="User Created Sucessfully...!")
            return redirect("login")
    signup_form = UserCreationForm()
    return render(request, "signup.html", context={"signup_form": signup_form})

    
def login_page(request):
    """
    This function is for user login
    after user sign-up he has username and password
    user needs to enter his/her username and password
    then they are able to access hime page
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)            
            messages.success(request, "user loggedIn Successfully...!")
            if request.user.is_superuser == True:
                return redirect("admin")
            
            return redirect("home")
            
    login_form = AuthenticationForm()
    return render(request, "login.html",context={"login_form": login_form})

def admin_view(request):
    """
    This function is created for admin only
    only admins can access this page
    """
    if request.user.is_superuser:
        return render(request, "admin_page.html")
    else:
        messages.warning(request, "You can't login to this page as Only admins can login to this page")
        return redirect("login")
            
def user_edit(request, id):
    """
    This function is to edit the users
    Only admins can access this view
    """
    if request.user.is_superuser:
        pk = id
        required_user = User.objects.get(id=pk)
        if request.method == 'POST':
            user_edit_form = UserChangeForm(data=request.POST, instance=required_user)
            if user_edit_form.is_valid():
                user_edit_form.save()
                return redirect("all_users")
        
        user_edit_form = UserChangeForm(instance=required_user)
        return render(request, "user_edit.html", context={"user_edit_form": user_edit_form})
        
    return redirect("login")

def logout_page(request):
    """
    This is normal logout function
    here user will be logout from the session
    """
    logout(request)
    return redirect("login")

def get_all_users(request):
    """
    This function is to get all users
    Only admin can access this
    """
    if request.user.is_superuser:
        all_users = User.objects.all()
        return render(request, "all_users.html", context={"all_users": all_users})
    return redirect("login")


# def test_sort(req):
#     data = Articles_db.objects.all()
#     sorted_data = sorted(data, key=lambda x: x.publishedAt)
#     print(sorted_data)
    


def filter_results(req):
    """
    This function is designed for filtering the search results
    """
    if req.user.is_authenticated:
        author_name_query = req.GET.get('author')
        print(author_name_query, "===================")
        user = User.objects.get(id=req.user.id)
        # print(user)
        user_search_articles = user.articles_db_set.all()
        articles_publishedAt_query = req.GET.get("publishedAt")
        query_sets = user_search_articles.filter(key_word=req.GET.get('q'), users=user)
        print(query_sets, "===")
        if articles_publishedAt_query:
            articles_publishedAt = query_sets.filter(publishedAt=articles_publishedAt_query)
            all_articles = articles_publishedAt
            print(all_articles)
            return render(req, "filter_results.html", context={"all_articles": all_articles, "query": req.GET.get('q')})
        else:
            
            articles_author_name = query_sets.filter(source__icontains=author_name_query)
            print(articles_author_name,"====article ====")
            all_articles = articles_author_name
            return render(req, "filter_results.html", context={"all_articles": all_articles, "query": req.GET.get('q')})
    
    else:
        return redirect("login")
