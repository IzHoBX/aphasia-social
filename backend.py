import http.server
import socketserver
import KeywordExtract.ExtractKeyword
import EmojiText.EmojiVec
import requests
import urllib
import json
import socket
import os
import ssl

from http.server import BaseHTTPRequestHandler, HTTPServer

PREFIX = "/agent?sentence="
RETURN_LIMIT = 5

def takeScore(x):
    return x[1]

class MyHandler(BaseHTTPRequestHandler):

    emoji2Vec = EmojiText.EmojiVec.EmojiVec()

    def do_GET(self):
        sentence = self.getSentence(self.path)

        ans = []
        for word in KeywordExtract.ExtractKeyword.extractKeyword(sentence):
            link, score =self.emoji2Vec.getEmoji(word)
            ans.append((link, score))
        if len(ans) > RETURN_LIMIT:
            ans.sort(reverse=True, key=takeScore)
            ans = ans[:RETURN_LIMIT]
        x = json.dumps({"emojis":ans})

        self.send_response(200)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(bytes(x,"utf-8"))
        self.wfile.close()

        return

    def getSentence(self, inx):
        inx = inx[len(PREFIX):]
        for i in range(0, len(inx)):
            if inx[i] == "+":
                inx = inx[:i]+ " "+inx[i+1:]
        return inx

print('starting server on port 7777...')

server_address = ('localhost', 7777)
httpd = HTTPServer(server_address, MyHandler)
httpd.serve_forever()
