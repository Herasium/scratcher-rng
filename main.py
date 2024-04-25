import modules.proxy as proxy
import random
import time

logo = '''
╔═╗┌─┐┬─┐┌─┐┌┬┐┌─┐┬ ┬┌─┐┬─┐  ╦═╗┌┐┌┌─┐
╚═╗│  ├┬┘├─┤ │ │  ├─┤├┤ ├┬┘  ╠╦╝││││ ┬
╚═╝└─┘┴└─┴ ┴ ┴ └─┘┴ ┴└─┘┴└─  ╩╚═┘└┘└─┘ v1.0, made by Herasium
'''

print(logo)

proxy_class = proxy.ProxyScraper()
proxies = proxy_class.Scraper()

import modules.scratch as scratch
import modules.image as image
import modules.rank as rank
import modules.user as users

account = scratch.Account("herasium","")
project = scratch.ScratchProject(1003965733,account)

def send_user_pp(user):
    img = image.get_user_image(user)
    project.send("img_1",img[0])
    time.sleep(0.1)
    project.send("img_2",img[1])
    time.sleep(0.1)
    project.send("img_3",img[2])
    time.sleep(0.1)
    project.send("img_user",scratch.Encoder().encode(user))

var_list = [
    " client_1"," client_2"," client_3"
]

#project.send("server_2",scratch.Encoder().encode("1\\herasium\\123456"))

@project.on_event
def on_event(request: scratch.Request):
    if not request.var in var_list: return False
    parsed = scratch.Encoder().decode(request.data)
    if parsed[1] == "open":
        user = users.random_user()
        uclass = rank.User(user)
        score = uclass.get_score()
        var="server_"+str(random.randint(1,3))
        print(user,var,len(scratch.Encoder().encode(str(parsed[0])+"\\"+user+"\\"+str(score.score)+"\\"+score.rank+"\\"+str(score.texts))))
        time.sleep(0.3)
        project.send(var,scratch.Encoder().encode(str(parsed[0])+"\\"+user+"\\"+str(score.score)+"\\"+score.rank+"\\"+str(score.texts)))
        time.sleep(0.1)
        send_user_pp(user)



project.start() # End of code
