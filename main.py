import modules.proxy as proxy

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

account = scratch.Account("herasium","")
project = scratch.ScratchProject(1003965733,account)

def send_user_pp(user):
    img = image.get_user_image(user)
    project.send("img_1",img[0])
    project.send("img_2",img[1])
    project.send("img_3",img[2])
    project.send("img_user",user)

while True:
    send_user_pp(input())

@project.on_event
def on_event(request: scratch.Request):
    print(f"New request on project {request.project} by {request.user}: {request.data}")

project.start() # End of code
