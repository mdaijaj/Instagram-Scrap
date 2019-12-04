import requests, json, pprint, os, path
import urllib.request
# from bs4 import BeautifulSoup

# url="http://form.hktdc.com/UI_VisitorIntranet/Public/VisitorListPublic.aspx?EVENTID=588916b5-631b-4d63-a828-26d727e8011f&LANGID?__a=1"

# # def get_data(url):
# data=requests.get(url)
# soup=BeautifulSoup(data.text, "html.parser")
# data_item=soup.find_all("tr", class_="datagrid_item")
# for i in data_item:
#     a=i.find("a")
#     print(a)
# print(get_data(url))







# url=("https://www.instagram.com/explore/tags/sarees/?__a=1")
# def get_data(url):

#     data=requests.get(url)
#     response=(data.text)
#     json_data=json.loads(response)
#     all_data=json_data["graphql"]["hashtag"]
#     # pprint.pprint(all_data)
#     ID=all_data["id"]
#     name=all_data["name"]
#     profileUrl=all_data["profile_pic_url"]

#     taken_at_timestamp=all_data["edge_hashtag_to_media"]["edges"][0]["node"]
#     # pprint.pprint(taken_at_timestamp)
#     timestamp=taken_at_timestamp["taken_at_timestamp"]
#     hashtag=taken_at_timestamp["edge_media_to_caption"]["edges"][0]["node"]["text"].split("\n")
#     shortcode=taken_at_timestamp["shortcode"]
#     # pprint.pprint(hashtag)
#     # length=len(hashtag)
#     # for i in range(0,length+1):
#     #     pprint.pprint(hashtag[length])

#     dic={
#         "id": ID,
#         "name": name,
#         "timestamp": timestamp,
#         "profileUrl": profileUrl,
#         "hashtag": hashtag,
#         "shortcode": shortcode
#     }
#     return dic
# pprint.pprint(get_data(url))





#home url fetch data
hashtag_list=[]
if os.path.exists("instagramAllData.json"):
    with open("instagramAllData.json", "r") as file:
        read=file.read()
        data=json.loads(read)
        pprint.pprint(data)
        print("file allready exists")
else:
    home_url="https://www.instagram.com/explore/tags/sarees/?__a=1"            
    data=requests.get(home_url)
    response=(data.text)
    json_data=json.loads(response)
    all_data=json_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
    # p(all_data)

    id_list=[]
    user_id=[]
    for index in all_data:
        owner=index["node"]["owner"]["id"]
        user=index["node"]["shortcode"]

        id_list.append(owner)
        user_id.append(user)

        #user url fetch data
        obj="/?__a=1"
        user_url="https://www.instagram.com/p/"+ user + obj                    
        data=requests.get(user_url)
        response=(data.text)
        json_data=json.loads(response)
        
        profile_data=json_data["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"]
        comment=json_data["graphql"]["shortcode_media"]["edge_media_preview_comment"]["count"]
        like=json_data["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]
        # pprint.pprint(json_data)
        owner=json_data["graphql"]["shortcode_media"]["owner"]

        id=json_data["graphql"]["shortcode_media"]["id"]
        hashtag=profile_data[0]["node"]["text"].split("\n")
        hashtag= hashtag[-1].split(" ")
        for x in hashtag:                      #duplicate value remove from array
            if x not in hashtag_list:
                hashtag_list.append(x)
        owner_id=owner["id"]
        timestamp=json_data["graphql"]["shortcode_media"]["taken_at_timestamp"]
        owner_username=owner["username"]

        
        #profile user url fetch data
        user_url_name= "https://www.instagram.com/" + owner_username + obj          
        data=requests.get(user_url_name)
        response=(data.text)
        jsonData=json.loads(response)
        # pprint.pprint(jsonData)
        
        biography=jsonData["graphql"]["user"]["biography"].split("\n")
        business_category=jsonData["graphql"]["user"]["business_category_name"]
        business_account=jsonData["graphql"]["user"]["is_business_account"]
        post=jsonData["graphql"]["user"]["edge_owner_to_timeline_media"]
        following=jsonData["graphql"]["user"]["edge_follow"]["count"]
        followers=jsonData["graphql"]["user"]["edge_followed_by"]["count"]

        data_detail={
            "id": id,
            "hashtag": hashtag,
            "owner_id": owner_id,
            "timestamps": timestamp,
            "owner_username": owner_username,
            "post": post["count"],
            "content": biography,
            "business_category": business_category,
            "business_account": business_account,
            "following": following,
            "followers": followers,
            "like": like,
            "comment": comment
        }
        pprint.pprint(data_detail)
        with open("instagramAllData.json","w")as file:
            data=json.dump(data_detail, file, indent=4)
            pprint.pprint(data)
            print("data create successfully")
            break
    print(hashtag_list)
        


