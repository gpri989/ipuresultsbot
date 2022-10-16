import asyncio
from multiprocessing.connection import Client
from typing import final
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
import requests
app = Client(
    "my_bot",
    api_id=API_ID, api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
@app.on_message(filters.command("start"))
async def start_command(_, message):
    await message.reply_text("**Hey! Enter Your University Roll Number**")

@app.on_message(filters.text)
async def search(client, message):
    rn = message.text
    url = f"https://api.ipuresults.xyz/v1/results/{rn}"
    res = requests.get(url)
    if res.status_code == 200:
        res1 = res.json()
        rus = res1['data']['results']
        str1 = f"**□ Name :** ```{res1['data']['name']}``` \n**□ Roll Number :** ```{res1['data']['rollNumber']}``` \n**□ Institue :** ```{res1['data']['institution']['name']}``` \n**□ Course :** ```{res1['data']['programme']['name']}``` \n**□ Total Semesters :** ```{res1['data']['results'][0]['semYear']['num']}``` \n**□ Aggregate Percentage :** ```{res1['data']['aggregatePercentage']}``` \n**□ Aggregate Credit Percentage :** ```{res1['data']['aggregateCreditPercentage']}``` \n**□ Credits :** ```{res1['data']['totalCreditsEarned']}/{res1['data']['maxCredits']}``` \n"
        await message.reply(str1,disable_web_page_preview=True)
        #await message.reply("Semester Wise Result Below")
        for i in range(0, len(rus)):
            str2 = f"**🔹 Semester {rus[i]['semYear']['num']}** \n**Total Marks :** ```{rus[i]['totalMarks']}/{rus[i]['maxMarks']}``` \n**Credit Percentage :** ```{rus[i]['creditPercentage']}``` \n**College Rank :** ```{rus[i]['collegeRank']}``` \n**University Rank :** ```{rus[i]['universityRank']}``` \n**Subject Wise 👇🏻**"
            await message.reply(str2,disable_web_page_preview=True)
            str3 = ""
            for sub in rus[i]['subjects']:
                str3 = str3 + f"✱ **{sub['name']}**\nMarks : ```{sub['total']['earned']}/{sub['total']['max']}```"
                str3 = str3 + "\n"
            await message.reply(str3,disable_web_page_preview=True)
    else:
        await message.reply("**❌ Enter Correct Roll Number ❌**")
print("Bot Alive")
app.run()
