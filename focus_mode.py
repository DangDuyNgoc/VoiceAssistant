import time
import ctypes
import datetime
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAdmin()
    except:
        return False

if is_admin:
    current_time = datetime.datetime.now().strftime("%H:%M")
    Stop_Time = input("Enter time eg:- [10:10] :-")

    host_path = "C:\Windows\System32\drivers\etc\hosts"
    redirect = "127.0.0.1"

    print(current_time)
    time.sleep(2)
    web_list = ["facebook.com", "www.twitter.com", "www.tiktok.com", "www.instagram.com", "youtube.com", "www.youtube.com", "facebook.com"]
    if(current_time < Stop_Time):
        with open(host_path, "r+") as file: 
            content = file.read()
            for web in web_list:
                if web in content:
                    pass
                else: 
                    file.write(f"{redirect} {web}")
                    print("Done!!!")

            print("web are blocked")
    
    while True: 
        current_time = datetime.datetime.now().strftime("%H:%M")
        web_list = ["facebook.com", "www.twitter.com", "www.tiktok.com", "www.instagram.com", "youtube.com"]
        if(current_time >= Stop_Time):
            with open(host_path, "r+") as file:
                content = file.readlines()
                file.seek(0)

                for line in content:
                    if not any(web in line for web in web_list):
                        file.write(line)
                
                file.truncate()

                print("web are unblocked")
                break
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, -1)
