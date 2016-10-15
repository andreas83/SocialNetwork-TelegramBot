#!/usr/bin/env python
#
# Simple Bot to reply Telegram messages
# Copyright (C) 2015 Leandro Toledo de Souza <leandrotoeldodesouza@gmail.com>
# Copyright (C) 2016 Andreas Beder <andreas@moving-bytes.at>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                                                                                                                
# GNU General Public License for more details.                                                                                                                                                 
#                                                                                                                                                                                              
# You should have received a copy of the GNU General Public License                                                                                                                            
# along with this program.  If not, see [http://www.gnu.org/licenses/].                                                                                                                        
                                                                                                                                                                                               
import logging                                                                                                                                                                                 
import telegram                                                                                                                                                                                
import json                                                                                                                                                                                    
import requests                                                                                                                                                                                
import pprint                                                                                                                                                                                  
import re                                                                                                                                                                                      
                                                                                                                                                                                               
                                                                                                                                                                                               
LAST_UPDATE_ID = None                                                                                                                                                                          
                                                                                                                                                                                               
                                                                                                                                                                                               
def main():                                                                                                                                                                                    
    global LAST_UPDATE_ID                                                                                                                                                                      
                                                                                                                                                                                               
    logging.basicConfig(                                                                                                                                                                       
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot('###### Authorization Token ######')

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        echo(bot)


def echo(bot):
    global LAST_UPDATE_ID
    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        message = update.message.text.encode('utf-8')
        chat_id = update.message.chat_id

        if (message):

            data = somethingnew(message);
            if (len(data) > 0):
                 data = data[0]  
            else:
                 bot.sendMessage(chat_id=chat_id, text="Sorry nothing found")
                 LAST_UPDATE_ID = update.update_id + 1
                 message = None
                 continue


            if (data['stream']['type'] == "img"):
                 bot.sendPhoto(chat_id=chat_id, photo=data['stream']['url'].encode('utf-8'))
                 LAST_UPDATE_ID = update.update_id + 1
            if (data['stream']['type'] == "video"):
                 url = re.search("(?P<url>https?://[^\s]+)", data['stream']['html']).group("url")
                 bot.sendMessage(chat_id=chat_id, text=data['stream']['text']+" " +url)
                 LAST_UPDATE_ID = update.update_id + 1

            if (data['stream']['type'] == "www"):
                 bot.sendMessage(chat_id=chat_id, text=data['stream']['url'])
                 LAST_UPDATE_ID = update.update_id + 1

            if (data['stream']['type'] == "upload"):
                 print data['stream']
                 bot.sendMessage(chat_id=chat_id, text=data['stream']['text']+" "+data['stream']['files'][0]['src'])
                 LAST_UPDATE_ID = update.update_id + 1


            if(data['stream']['type']!=""):
                 bot.sendMessage(chat_id=chat_id, text="DMDN Bot " +data['stream']['text'])
                 LAST_UPDATE_ID = update.update_id + 1


def somethingnew(hash):
        data = { "show":"1", "hash": hash}
        r = requests.get("http://www.dasmerkendienie.com/api/content/", params=data);
        return json.loads(r.text)


if __name__ == '__main__':
    main()
