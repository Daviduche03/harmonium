import discord
import os
import requests
import json

class DiscordBot:
    def __init__(self, ai_url, ai_model, token_env_var='TOKEN', ai_token_env_var='AI_TOKEN'):
        self.intents = discord.Intents.default()
        self.client = discord.Client(intents=self.intents)
        self.ai_url = ai_url
        self.ai_model = ai_model
        self.token_env_var = token_env_var
        self.ai_token_env_var = ai_token_env_var

        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    def ai_response(self, user_message):
        auth_token = os.getenv(self.ai_token_env_var)
        response = requests.post(
            url=self.ai_url,
            headers={
                "Authorization": f'Bearer {auth_token}',
            },
            data=json.dumps({
                "model": self.ai_model,
                "messages": [{
                    "role": "user",
                    "content": user_message
                }]
            }))
        choices = response.json().get('choices', [])
        for result in choices:
            return result['message']['content']

    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content:
            response = self.ai_response(message.content)
            await message.channel.send(response)

    def run(self):
        token = os.getenv(self.token_env_var)
        self.client.run(token)

# Usage example (this should be in a separate script):
if __name__ == "__main__":
    ai_url = "https://openrouter.ai/api/v1/chat/completions"
    ai_model = "mistralai/mistral-7b-instruct"
    bot = DiscordBot(ai_url, ai_model)
    bot.run()
