from lxml import html
import requests
import json

url = "https://www.vpngate.net/en/"
page = requests.get(url)

tree = html.fromstring(page.content)

SSTP_List = list()


def download_flag(flag_url):
    with open('flags.txt','r') as file:
        flag_list = file.read().split('\n')
        file.close()
        
    file_name = flag_url.split("/")[-1]
    
    
    if file_name not in flag_list:
        flag_list.append(str(file_name))
        with open("./flags/"+file_name, "wb") as f:
            r = requests.get(flag_url, stream=True)
            f.write(r.content)
        
        with open('flags.txt', 'w') as fff:
            for i in flag_list:
                if i.strip() != '':
                    fff.write(i.strip() + '\n')
            fff.close()

    else:
        pass
    
    return (
        "https://raw.githubusercontent.com/FreeSSTP/server-list/main/flags/"
        + flag_url.split("/")[-1]
    )


def work():
    SSTP_List.clear()
    rows = tree.xpath('//*[@id="vg_hosts_table_id"]')[2].xpath("./tr")
    for tr in rows:
        td = tr.xpath("./td")
        if "SSTP Hostname" in td[7].text_content():
            temp_host = td[7].xpath("./p/span/b/span/text()")[0]
            host = temp_host if ":" not in temp_host else temp_host.split(":")[0]
            location = td[0].text_content()

            flag = download_flag(td[0].xpath("./img/@src")[0].replace('../', 'https://www.vpngate.net/'))
            
            ping = td[3].xpath("./b[2]/text()")[0]
            port = 443 if ":" not in temp_host else int(temp_host.split(":")[1])
            uptime = td[2].xpath("./span/text()")[0]
            sessions = int(td[2].xpath("./b/span/text()")[0].replace(" sessions", ""))
            line_quality = td[3].xpath("./b[1]/span/text()")[0]
            score = int(td[9].xpath("./b/span/text()")[0].replace(",", ""))

            data = {
                "HOSTNAME": host,
                "LOCATION": location,
                "FLAG": flag,
                "PING": ping,
                "PORT": port,
                "UPTIME": uptime,
                "SESSIONS": sessions,
                "LINE_QUALITY": line_quality,
                "SCORE": score,
            }
            SSTP_List.append(data)

    with open("Records.json", "w") as final:
        json.dump(SSTP_List, final)

    with open("details.json", "w") as fff:
        fff.write("Server count: {}".format(len(SSTP_List)))


work()