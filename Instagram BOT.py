import os, shutil, sys, time
try:
    import instaloader
    from prettytable import PrettyTable
except:
    pathList = str(sys.executable).split("\\")
    pathList.remove("pythonw.exe"),pathList.append("Scripts")
    os.system("/".join(pathList)+"/pip.exe install instaloader")
    os.system("/".join(pathList)+"/pip.exe install prettytable")
    print("Downloaded Modules. Starting in 3 Seconds.")
    time.sleep(2)
    import instaloader
    from prettytable import PrettyTable
instagramBot = instaloader.Instaloader(quiet = True)

def auth():
    userName = input("Enter Your Instagram Username: ")
    try:
        instagramBot.load_session_from_file(userName)
    except:
        try:
            os.system("instaloader -l {0}".format(userName))
            instagramBot.load_session_from_file(userName)
        except:
            instagramBot.login(userName,input("Enter Password: "))
    print("{0} Logged In.".format(userName))

def main():
    auth()
    while True:
        myTable = PrettyTable(["Index","Task"])
        myTable.add_row(["1", "Download Profile Image from Username"])
        myTable.add_row(["2", "Download All Posts from Username"])
        myTable.add_row(["3", "Download Images from Hashtags"])
        print(myTable)
        query = input("Enter Index to Perform: ")
        if query == "1":
            currentPath = os.getcwd()
            username = input("Enter Username to Download Profile Image: ")
            instagramBot.download_profile(username, profile_pic_only = True)
            for file in os.listdir(username):
                if ".jpg" in file:
                    shutil.move("{0}/{1}".format(username,file),currentPath)
            shutil.rmtree(username)
            print("'{0}' Profile Image Downloaded.".format(username))
        elif query == "2":
            currentPath = os.getcwd()
            username = input("Enter Username to Download: ")
            try : 
                profile = instaloader.Profile.from_username(instagramBot.context, username)
            except:
                print("Username Not Found."),exit()
            if os.path.exists(username) == False:os.mkdir(username)
            os.chdir(username)
            if os.path.exists("Videos") == False:os.mkdir("Videos")
            posts = profile.get_posts()
            print("Downloading... Ctrl + C to Stop in between. Don't Open Username Folder.")
            for index, post in enumerate(posts):
                try:
                    instagramBot.download_post(post, target = index)
                except:
                    break
                    print("Downloader Exited.")
            for folder in os.listdir():
                if "." not in folder:
                    for item in os.listdir(folder):
                        if ".jpg" in item:
                            shutil.move(folder+"/"+item, "{0}/{1}".format(currentPath, username))
                        elif ".mp4" in item:
                            try:
                                shutil.move(folder+"/"+item, "{0}/{1}/Videos".format(currentPath, username))
                            except:
                                continue
                    shutil.rmtree(folder)
            print("{} Folder Created.".format(username))
        elif query == "3":
            instaloader.Instaloader(download_videos=False, save_metadata=False, post_metadata_txt_pattern='').download_hashtag(input("Enter Hashtag: "), max_count=20)
        break
main()
