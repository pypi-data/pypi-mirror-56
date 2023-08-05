import requests
import json

def main():
    """Entry point for the application script"""
    print("Call your main application code here")

def getData(boname,headers,data):
    print("called")
    url = "http://10.134.192.116:8081/dspdm/rest/common/"
    response = requests.request("POST", url,headers= headers, json=data)
    return json.loads(response.text)[data][boname]["list"]