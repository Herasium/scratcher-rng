import scratchattach as scratch
import requests
import time

user_list = []

with open("accounts.txt","r") as txt:
    user_list = txt.read().split(";")


acc = scratch.login("followeveryoneaaaaaa",",f4Vz(BzKrx_9=M")

acc._get_csrftoken()

headers = acc._headers
headers["cookie"] = "scratchcsrftoken="+headers["x-csrftoken"]+";scratchsessionsid="+acc.session_id

for user in user_list:
            start_time = time.time()
            resp = requests.put("https://scratch.mit.edu/site-api/users/followers/"+user+"/add/?usernames=followeveryoneaaaaaa",headers=headers)
            end_time = time.time()
            print(resp.status_code,user)
            if (end_time-start_time) < 1:
                time.sleep(1-(end_time-start_time))
    