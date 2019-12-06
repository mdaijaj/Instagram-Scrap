import requests, json, pprint, os, path, datetime
import urllib.request
# import pandas as pd
# import pandas


current_time=datetime.datetime.now()
hr=current_time.hour
minute=current_time.min
sec=current_time.second
# if (current_time-last_time)>=frequency:
#     if enable==true:

# home url fetch data
# df_ht = pd.read_csv("ht.csv")
hashtags_list=["#sarees", "#saree"]
users_list=[]
main_data_list=[]

#if you want to find only one user scrap all hashtags information then take instagram function under loop 
# otherwise which is written below the last hashtag scrap all users scrape data and store.

for ht in hashtags_list:  
    ht=ht[1:len(ht)]
    # print(ht)

def instagram_data(ht):         
    i=0
    obj="/?__a=1"
    if os.path.exists("instagramAllData.json"):
        with open("instagramAllData.json") as file:
            read=file.read()
            data=json.loads(read)
        return (data)
    
    home_url="https://www.instagram.com/explore/tags/"+ ht + obj            
    data=requests.get(home_url)
    response=(data.text)
    json_data=json.loads(response)
    all_data=json_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
    # pprint.pprint(json_data)

    all_data_list=[]
    for index in all_data:
        user=index["node"]["shortcode"]
        if user not in users_list:                  #unique    
            users_list.append(user)

            #user url fetch data
            user_url="https://www.instagram.com/p/"+ user + obj                    
            data=requests.get(user_url)
            response=(data.text)
            json_data=json.loads(response)
            
            profile_data=json_data["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"]
            comment=json_data["graphql"]["shortcode_media"]["edge_media_preview_comment"]["count"]
            like=json_data["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]
            timestamp=json_data["graphql"]["shortcode_media"]["taken_at_timestamp"]
            owner=json_data["graphql"]["shortcode_media"]["owner"]
            owner_id=owner["id"]
            owner_username=owner["username"]
            hash_tag_id=json_data["graphql"]["shortcode_media"]["id"]
            hashtag=profile_data[0]["node"]["text"].split("\n")
            hashtag= hashtag[-1].split(" ")
            
            # print(hashtag)

            for x in hashtag:                      #duplicate value remove from array
                if x not in hashtags_list:
                    hashtags_list.append(x)
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

            main_data={
                "hashtag": hashtags_list,
                "last_update": "last_update",
                "frequency(hrs)": "6 hours",
                "status": "enable"
            }

            data_detail={
                "user_id": user,
                "hash_tag_id": hash_tag_id,
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
            main_data_list.append(main_data)
            all_data_list.append(data_detail)
            pprint.pprint(data_detail)
            # if i >= 1 :
            #     break
            # i= i +1
            # print(hashtags_list)                     ## show hashtag not duplicate value

    # # pandas.read_json(json.dumps(all_data_list)).to_csv("source.csv")     
    # return (data_detail)

    with open("instagramAllData.json","w")as file:              #json file format
        json.dump(all_data_list, file, indent=4) 
    return (data_detail)
pprint.pprint(instagram_data(ht))

        