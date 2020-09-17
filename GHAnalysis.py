import json
import os
import argparse


class Data:
    def __init__(self, dict_address: int = None, reload: int = 0):
        if reload == 1:
            self.__init(dict_address)
        if dict_address is None and not os.path.exists('user_event.json') and not os.path.exists('repo_event.json') and not os.path.exists('user_repo_event.json'):
            raise RuntimeError('error: init failed')

    def __init(self, Address):
        user_event = {}
        repo_event = {}
        user_repo_event = {}
        for root, dic, files in os.walk(Address):
            # 遍历文件夹
            for f in files:
                if f[-5:] == '.json':
                    event = ["PushEvent", "IssueCommentEvent", "IssuesEvent", "PullRequestEvent"]
                    json_path = f
                    x = open(Address + '\\' + json_path , 'r' , encoding='utf-8').readlines()
                    for i in x :
                        i = json.loads(i)
                        if  i["type"] in event:
                            self.add_user_event(i, user_event)
                            self.add_repo_event(i, repo_event)
                            self.add_user_repo_event(i, user_repo_event)
        with open("user_event.json", "a") as f:
            json.dump(user_event, f)
        with open("repo_event.json", "a") as f:
            json.dump(repo_event, f)
        with open("user_repo_event.json", "a") as f:
            json.dump(user_repo_event, f)

    def add_user_event(self, i, user_event):
        id = i["actor"]["login"]
        event = i["type"]
        if id not in user_event:
            #如果此ID未出现过，就建立新数据
            user_event[id] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        user_event[id][event] +=1

    def add_repo_event(self, i, repo_event):
        repo = i["repo"]["name"]
        event = i["type"]
        if repo not in repo_event:
            repo_event[repo] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        repo_event[repo][event] += 1

    def add_user_repo_event(self, i, user_repo_event):
        id = i["actor"]["login"]
        event = i["type"]
        repo = i["repo"]["name"]
        if id not in user_repo_event:
            user_repo_event[id] = {}
            user_repo_event[id][repo] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        if repo not in user_repo_event:
            user_repo_event[id][repo] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        user_repo_event[id][repo][event] +=1

    def get_user_event(self, user, event):
        x = open("user_event.json", "r", encoding="utf-8").read()
        data = json.loads(x)
        return data[user][event]
    
    def get_repo_event(self, repo, event):
        x = open("repo_event.json", "r", encoding="utf-8").read()
        data = json.loads(x)
        return data[repo][event]
    
    def get_user_repo_event(self,user, repo, event):
        x = open("user_repo_event.json", "r", encoding="utf-8").read()
        data =json.loads(x)
        return data[user][repo][event]


class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.data = None
        self.argInit()

    def argInit(self):
        self.parser.add_argument('-i', '--init')
        self.parser.add_argument('-u', '--user')
        self.parser.add_argument('-r', '--repo')
        self.parser.add_argument('-e', '--event')
        
    def analyse(self):
    if self.parser.parse_args().init:
        self.data = Data(self.parser.parse_args().init, 1)
    elif args.user and args.event and not args.repo:
        data = Data()
        print(data.get_user_event(args.user, args.event))
    elif args.repo and args.event and not args.user:
        data = Data()
        print(data.get_repo_event(args.repo, args.event))
    elif args.user and args.repo and args.event:
        data = Data()
        print(data.get_user_repo_event(args.user, args.repo, args.event))

if __name__ == '__main__':
    a = Run()
