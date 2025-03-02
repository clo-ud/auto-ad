# Imports
import requests, json, time, os, websocket, threading, ssl, sys, select, datetime, subprocess, random
from colorama import Fore, Back, Style
if os.name == 'nt':
    import msvcrt

# Check Config
with open('config.json') as f:
    data = json.load(f)
token = data.get('token') or input("Enter your token: ").replace('"', '').replace("'","")
while requests.get('https://discord.com/api/v10/users/@me', headers={'Authorization': token}).status_code != 200:
    token = input("Invalid token, enter your token: ").replace('"', '').replace("'","")
data['token'] = token
data['message'] = data.get('message') or input("Enter message: ").replace('\\n','\n')
data['delay'] = data.get('delay') or input("Enter your delay (in seconds): ")
data['channels'] = data.get('channels') or input("Enter channel ID/s (separated by a space): ").split(" ")
data['webhook'] = data.get('webhook') or input("Enter webhook URL for logging (leave blank if you don't want webhook notifications): ") 
data['repeatBypass'] = data.get('repeatBypass') or input("Enable message repeat bypass? (y/n): ").strip().lower()
while data['repeatBypass'] not in ("y", "n"):data['repeatBypass'] = input("Invalid choice, enable message repeat bypass? (y/n): ").strip().lower()
with open('config.json', 'w') as f:
    json.dump(data, f)
    f.close()

# Message Sender
def sendMessage():
    global x
    last_action_time = time.time()
    start_time = time.time()
    stop_msg = Fore.RED + ("Press your 'escape' key to stop advertising!" if os.name == 'nt' else "Enter 'escape' to stop advertising!")
    print(stop_msg)
    while True:
        elapsed_time = time.time() - last_action_time

        if (os.name == 'nt' and 'msvcrt' in sys.modules and msvcrt.kbhit() and msvcrt.getch() == b'\x1b') or (os.name != 'nt' and select.select([sys.stdin,],[],[],0.0)[0] and sys.stdin.readline().strip() == 'escape'):
                break

        if elapsed_time >= float(data.get('delay')):
            last_action_time = time.time()
            if (os.name == 'nt' and 'msvcrt' in sys.modules and msvcrt.kbhit() and msvcrt.getch() == b'\x1b') or (os.name != 'nt' and select.select([sys.stdin,],[],[],0.0)[0] and sys.stdin.readline().strip() == 'escape'):
                break
            channels = data.get('channels')
            for channel in channels:
                if data.get('repeatBypass') == 'y':
                    repeatBypass = str(random.randint(752491546761342621526, 7834345876325483756245232875362457316274977135724691581387))
                    requests.post(f'https://discord.com/api/v10/channels/{channel}/messages', headers={'Authorization': token}, json={'content': data.get('message')+'\n\n'+repeatBypass})
                else:
                    requests.post(f'https://discord.com/api/v10/channels/{channel}/messages', headers={'Authorization': token}, json={'content': data.get('message')})
                elapsed_time = time.time() - start_time
                elapsed_time_str = f"[{datetime.timedelta(seconds=elapsed_time)}s]"
                if data.get('webhook'):requests.post(data.get('webhook'), json={'content': f'{elapsed_time_str} Sent message to channel <#{channel}>'})
                x+=1;subprocess.call('title="Discord Advertiser | Messages Sent: {}"'.format(x), shell=True)
            if data.get('webhook'):requests.post(data.get('webhook'), json={'content': f'Cooldown has been reached. Sleeping for {data.get("delay")} seconds.'})

        time.sleep(1.5)

# Channels Changer
def modifyChannels(operation):
    channel = input("Enter channel ID: ")
    if operation == 'add':
        data['channels'].append(channel)
        update_config(data, 'channels')
    elif operation == 'remove':
        data['channels'].remove(channel)
        update_config(data, 'channels')

# Delay Changer
def changeMessage():
    data['message'] = input("Enter your message: ")
    update_config(data, 'message')

# Delay Changer
def changeDelay():
    data['delay'] = input("Enter your delay (in seconds): ")
    update_config(data, 'delay')

# Config Updater
def update_config(data, parameter):
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Changed {parameter} to {data[parameter]}")
        time.sleep(3)

# Clear console
def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

# Advertiser menu
def advertiser():
    while 1:
        clearConsole()
        choice=input(Fore.RED+"Advertiser:\n"+Fore.YELLOW+"1. Start advertiser\n2. Add channel\n3. Remove channel\n4. Change message\n5. Change delay\n6. Leave\n")
        {'1':lambda:sendMessage(),'2':lambda:modifyChannels('add'),'3':lambda:modifyChannels('remove'),'4':lambda:changeMessage(),'5':lambda:changeDelay(),'6':lambda:main()}.get(choice,lambda:print('Invalid choice'))()
        time.sleep(0.5)

# Main menu
def main():
    while 1:
        clearConsole()
        choice=input(Fore.RED+"Home:\n"+Fore.YELLOW+"1. Advertiser\n2. Leave\n")
        {'1':advertiser,'2':lambda:exit()}.get(choice,lambda:print('Invalid choice'))()
        time.sleep(0.5)

x=0;subprocess.call('title="Discord Advertiser | Messages Sent: {}"'.format(x), shell=True)
main()
