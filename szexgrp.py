import requests

class Jyfwxx:
    def __init__(self,title="城市更新",size=50):
        self.url = "https://www.szexgrp.com/cms/api/v1/trade/content/page"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"}
        self.params = {"channelId":2855,
                        "fields":[],
                        "title":title,
                        "page":0,
                        "size":size,
                        "parentBusinessType":"",
                        "modelId":1378,
                        "siteId":1}
        self.totalPages = 0
        self.totalElements = 0
        self.content_list = []
        self.fields = ["title","areaName","appNoticeTypeName","noticeTypeName","releaseTime","channelId","contentId","migration"]
        
    def main(self):
        self._first_request()
        print(f"Total Pages: {self.totalPages}, Total Elements: {self.totalElements}")
        for page in range(1, self.totalPages):
            self.params["page"] = page
            res = self.get_title()
        print(f"Completed fetching all pages.{len(self.content_list)} items collected.")
                    
    def get_title(self):
        response = requests.post(self.url, json=self.params, headers=self.headers,timeout=10)
        response.raise_for_status()
        self._parse_data(response.json())
        print(f"Fetched page {self.params['page']}")
        return response.json()
    
    def _first_request(self):
        res = self.get_title()
        self.totalPages = res.get("data", {}).get("totalPages", 0)
        self.totalElements = res.get("data", {}).get("totalElements", 0)

    def _parse_data(self, data):
        content = data.get("data", {}).get("content", [])
        content_length = len(content)   
        if (self.params["page"] < self.totalPages -1 and content_length < self.params["size"]) or \
           (self.params["page"] == self.totalPages - 1 and content_length < (self.totalElements % self.params["size"])):
            print(f"Warning: Fewer items {content_length} than expected on page {self.params['page']}")

        for item in content:
            content_item = [item.get(field) for field in self.fields]
            title = item.get("title")
            area_name = item.get("areaName")
            appNoticeTypeName = item.get("appNoticeTypeName")
            noticeTypeName = item.get("noticeTypeName")
            release_time = item.get("releaseTime")
            channelId = item.get("channelId")
            contentId = item.get("contentId")
            migration = item.get("migration")
            self.content_list.append({
                "title": title,
                "area_name": area_name,
                "appNoticeTypeName": appNoticeTypeName,
                "noticeTypeName": noticeTypeName,
                "release_time": release_time,
                "channelId": channelId,
                "contentId": contentId,
                "migration": migration
            })
            # print(f"Title: {title}, Release Time: {release_time} Area Name: {area_name}, App Notice Type Name: {appNoticeTypeName}, Notice Type Name: {noticeTypeName}, Channel ID: {channelId}, Content ID: {contentId}, Migration: {migration}")
            

if __name__ == "__main__":
    jyfwxx = Jyfwxx()
    # jyfwxx.main()
    # jyfwxx.params["page"] = 1
    # res = jyfwxx.get_title()
    # print(res)