import requests
import os
from datetime import datetime
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import mysql.connector

# connect to the "watchtower" database
def connect_to_mysql():
    try:
        # connect to the database
        db = mysql.connector.connect(
            host="localhost",
            user="database username",
            password="database password",
            database="watchscope"
        )

        # return the database connection object
        return db

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

discord_webhook_url = "your webhook link"
discord_webhook_url_error = "your webhook link for error messages"
webhook = DiscordWebhook(url=discord_webhook_url)

hackerone_url = 'https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/hackerone.json'
bugcrowd_url = 'https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/bugcrowd.json'
yeswehack_url = 'https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/yeswehack.json'


# Function to handle errors
def handle_error(error):
    message = f"Error at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {error}"
    send_discord_message(discord_webhook_url_error, message)

# Function to send a message to a Discord webhook
def send_discord_message(url, message):
    data = {"content": message}
    response = requests.post(url, json=data)
    if response.status_code != 204:
        raise ValueError(f"Failed to send message to {url}: {response.content}")



def main():
    function_hackerone()
    function_bugcrowd()
    function_yeswehack()

def function_hackerone():
    try:
        # Get the new data from the URL
        response = requests.get(hackerone_url)
        response.raise_for_status()
        data = response.json()

        db = connect_to_mysql()
        cursor = db.cursor()



        # loop over data items
        for item in data:
            structured_scopes = item['relationships']['structured_scopes']['data']
            for scope in structured_scopes:
                Asset_Identifier = scope['attributes']['asset_identifier']
                name = item['attributes']['name']
                profile_picture = item['attributes']['profile_picture']
                offers_bounties = item['attributes']['offers_bounties']
                handle = item['attributes']['handle']
                platform = 'Hackerone'
                print(Asset_Identifier)
                if offers_bounties == True:
                    type_target = 'Bug Bounty'
                else:
                    type_target = 'VDP'


                query = "SELECT * FROM programs WHERE name=%s AND Asset_Identifier=%s AND type=%s AND platform=%s"
                values = (name, Asset_Identifier, type_target, platform)
                cursor.execute(query, values)
                result = cursor.fetchone()
                #print(result)
                if result is None:
                    # if record does not exist in table, insert it
                    insert_query = "INSERT INTO programs (name, Asset_Identifier, type, platform) VALUES (%s, %s, %s, %s)"
                    insert_values = (name, Asset_Identifier, type_target, platform)
                    cursor.execute(insert_query, insert_values)

                    # create embed object
                    embed = DiscordEmbed(title=platform, color='03b2f8')
                    embed.set_thumbnail(url=profile_picture)
                    embed.add_embed_field(name="Name: ", value=name, inline=False)
                    embed.add_embed_field(name="Asset Identifier: ", value=Asset_Identifier, inline=False)
                    embed.add_embed_field(name="Website: ", value=f"https://hackerone.com/{handle}", inline=False)
                    embed.add_embed_field(name="Offers Bounties: ", value=type_target, inline=False)
                    embed.set_footer(text=f"New data detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    # add embed object to webhook
                    webhook.add_embed(embed)
                    # send webhook
                    response = webhook.execute(remove_embeds=True)
                    time.sleep(10)
                    # clear all fields from the embed
                    #embed.fields = []
        db.commit()
        db.close()
    except Exception as e:
        handle_error(e)    
    pass

def function_bugcrowd():
    try:
        # Get the new data from the URL
        response = requests.get(bugcrowd_url)
        response.raise_for_status()
        data = response.json()

        db = connect_to_mysql()
        cursor = db.cursor()



        # loop over data items
        for item in data:
            if not item['target_groups']:
                Asset_Identifier = 'seyed'
                name = item['name']
                profile_picture = item['logo']
                type_target = item['license_key']
                handle = item['program_url']
                platform = 'BugCrowd'
                print(Asset_Identifier)
            else:
                structured_scopes = item['target_groups'][0]['targets']
                for scope in structured_scopes:
                    if item['target_groups'][0]['in_scope'] == True:
                        Asset_Identifier = scope['name']
                        name = item['name']
                        profile_picture = item['logo']
                        type_target = item['license_key']
                        handle = item['program_url']
                        platform = 'BugCrowd'
                        print(Asset_Identifier)
                    


                    query = "SELECT * FROM programs WHERE name=%s AND Asset_Identifier=%s AND type=%s AND platform=%s"
                    values = (name, Asset_Identifier, type_target, platform)
                    cursor.execute(query, values)
                    result = cursor.fetchone()
                    #print(result)
                    if result is None:
                        # if record does not exist in table, insert it
                        insert_query = "INSERT INTO programs (name, Asset_Identifier, type, platform) VALUES (%s, %s, %s, %s)"
                        insert_values = (name, Asset_Identifier, type_target, platform)
                        cursor.execute(insert_query, insert_values)

                        # create embed object
                        embed = DiscordEmbed(title=platform, color='03b2f8')
                        embed.set_thumbnail(url=profile_picture)
                        embed.add_embed_field(name="Name: ", value=name, inline=False)
                        embed.add_embed_field(name="Asset Identifier: ", value=Asset_Identifier, inline=False)
                        embed.add_embed_field(name="Website: ", value=f"https://www.bugcrowd.com{handle}", inline=False)
                        embed.add_embed_field(name="Offers Bounties: ", value=type_target, inline=False)
                        embed.set_footer(text=f"New data detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        # add embed object to webhook
                        webhook.add_embed(embed)
                        # send webhook
                        response = webhook.execute(remove_embeds=True)
                        time.sleep(10)
                        # clear all fields from the embed
                        #embed.fields = []
        db.commit()
        db.close()
    except Exception as e:
        handle_error(e)
    pass

def function_yeswehack():
    try:
        # Get the new data from the URL
        response = requests.get(yeswehack_url)
        response.raise_for_status()
        data = response.json()

        db = connect_to_mysql()
        cursor = db.cursor()



        # loop over data items
        for item in data:
            structured_scopes = item['scopes']
            for scope in structured_scopes:
                Asset_Identifier = scope['scope']
                name = item['title']
                profile_picture = item['thumbnail']['url']
                offers_bounties = item['bounty']
                handle = item['slug']
                platform = 'YesWeHack'
                print(Asset_Identifier)
                if offers_bounties == True:
                    type_target = 'Bug Bounty'
                else:
                    type_target = 'VDP'


                query = "SELECT * FROM programs WHERE name=%s AND Asset_Identifier=%s AND type=%s AND platform=%s"
                values = (name, Asset_Identifier, type_target, platform)
                cursor.execute(query, values)
                result = cursor.fetchone()
                #print(result)
                if result is None:
                    # if record does not exist in table, insert it
                    insert_query = "INSERT INTO programs (name, Asset_Identifier, type, platform) VALUES (%s, %s, %s, %s)"
                    insert_values = (name, Asset_Identifier, type_target, platform)
                    cursor.execute(insert_query, insert_values)

                    # create embed object
                    embed = DiscordEmbed(title=platform, color='03b2f8')
                    embed.set_thumbnail(url=profile_picture)
                    embed.add_embed_field(name="Name: ", value=name, inline=False)
                    embed.add_embed_field(name="Asset Identifier: ", value=Asset_Identifier, inline=False)
                    embed.add_embed_field(name="Website: ", value=f"https://yeswehack.com/programs/{handle}", inline=False)
                    embed.add_embed_field(name="Offers Bounties: ", value=type_target, inline=False)
                    embed.set_footer(text=f"New data detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    # add embed object to webhook
                    webhook.add_embed(embed)
                    # send webhook
                    response = webhook.execute(remove_embeds=True)
                    time.sleep(10)
        db.commit()
        db.close()
    except Exception as e:
        handle_error(e)   
    pass

if __name__ == '__main__':
    main()
