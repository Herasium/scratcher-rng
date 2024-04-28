import modules.proxy as proxy
import random

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

account = scratch.Account("ScratcherRng","")
project = scratch.ScratchProject(1003965733,account)

def send_user_pp(user):
    img = image.get_user_image(user)
    project.send("img_1",img[0])
    project.send("img_2",img[1])
    project.send("img_3",img[2])
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
        print("Requested user",user)
        uclass = rank.User(user)
        score = uclass.get_score()
        var="server_"+str(random.randint(1,3))
        print("Sent user",user)
        project.send(var,scratch.Encoder().encode(str(parsed[0])+"\\"+user+"\\"+str(score.score)+"\\"+score.rank+"\\"+str(score.texts)))
        send_user_pp(user)



project.start() # End of code
