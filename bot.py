import requests
import urllib.parse
import aiohttp
import typing
import discord
from discord import Client, Intents, Interaction
from discord.app_commands import (
    CommandTree,
    allowed_installs, guild_install, user_install,
    allowed_contexts, dm_only, guild_only, private_channel_only,
)
import cohere
import datetime
from discord.ext import commands
from pydub import AudioSegment
from rembg import remove
from io import BytesIO 
from selenium import webdriver
import urllib.request
import os
import io
from PIL import Image
import time
from backgroundremover.bg import remove
from dotenv import load_dotenv
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

import asyncio
# .envファイルから環境変数を読み込む
load_dotenv()


r'''
===========================================================
===========================================================
 ____                          ____        _   
| __ ) _   _  __ _  __ _  __ _| __ )  ___ | |_ 
|  _ \| | | |/ _` |/ _` |/ _` |  _ \ / _ \| __|
| |_) | |_| | (_| | (_| | (_| | |_) | (_) | |_ 
|____/ \__,_|\__,_|\__,_|\__,_|____/ \___/ \__|  v0.2a

Made By Sotaro Shimada


やること

・旧仕様のままのものを新仕様に書き換える <=多分できた
・不要なライブラリをアンロードする
・汚いクソコードを綺麗にする

===========================================================
===========================================================
'''


# ここから定義

dt_now = datetime.datetime.now()

# なんの定義か忘れた
filepath_temp = os.path.dirname(__file__)
filepath = ""
for i in range(len(filepath_temp)):
    if filepath_temp[i] == "\\":
        filepath = filepath + "/"
    else:
        filepath = filepath + filepath_temp[i]
    
# Discordのインテント指定
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='bu!', intents=intents)

# 画像検索のやつのキー(Microsoft Bing Search API)
subscription_key = os.getenv('BINGKEY')
search_url = "https://api.bing.microsoft.com/v7.0/images/search"

# dotenv読み込み
TOKEN = os.getenv('DISCORD_TOKEN')

# ＠の置き換え
def replace_at(text: str) -> str:
    return text.replace("@", "＠")

# removebgAPIKey
removebg_key = os.getenv('REMOVEBG')

# Cohere Chat API Key
co = cohere.Client(os.getenv('COHERE'))

GOOGLE_API_KEY=os.getenv('GEMINI')
genai.configure(api_key=GOOGLE_API_KEY)

# 定義ここまで

# ===========================================================
# ===========================================================


# 一応起動通知（おんれでぃー）
@bot.event
async def on_ready():
    print('きどーしたよ')
    channel = bot.get_channel(1210374862217158776) # 起動通知をするチャンネルをここに入れる
    day = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    mes = f'''以下の条件で、BuaaaBotが今起動したことをお知らせする文章で応答してください。
    ・あなたの名前はDiscordボットの「BuaaaBot」
    ・今の日時時間は{day}
    ・朝5時台に起動していれば正常に自動起動し、それ以外はBuachiが手動で起動したということを伝える
    ・語尾は「にゃん！」
    ・BuaaaBotのオーナーはぶあち(Buachi)
    '''
    response = co.chat(
        message=mes, 
        model="command-r-plus", 
        temperature=0.9,
        connectors=[{"id": "web-search"}]
    )
    await channel.send(response.text)
    await bot.tree.sync() # スラッシュコマンド更新
    
# サイトのスクショ取得
@bot.hybrid_command(name="webpageshot", aliases=['wp', 'web', "url"], brief="指定されたURLのスクリーンショットを取得します")
@allowed_installs(guilds=True, users=True)
async def webpageshot(ctx, url:str):
    if ctx.interaction:
        await ctx.interaction.response.defer()
    if not url:
        await ctx.send(("URLを指定してください"))
        return
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "https://" + url  # http(s)を入れてない場合に入れる
    message = await ctx.send(("内部ブラウザを起動中です..."))
    start_time = time.time()
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu") 
    options.add_argument("--no-sandbox")  
    options.add_argument("--window-size=1920,1080")  
    
    try:
        driver = webdriver.Chrome()
        await message.edit(content=(("読み込み中です...")))
        driver.get(url)    
        driver.execute_script("return document.body.scrollHeight") 
        body_height = driver.execute_script("return document.body.scrollHeight")
        window_height = driver.execute_script("return window.innerHeight")
        if body_height > window_height:
            driver.set_window_size(driver.get_window_size()["width"], body_height)
        driver.execute_script("return document.readyState")
        await message.edit(content=(("スクリーンショットを取得しています...")))
        screenshot = driver.get_screenshot_as_png()
        driver.quit()
        
        elapsed_time = time.time() - start_time
        await message.edit(content=(("完了しました！")))
        image_stream = io.BytesIO(screenshot)
        embed = discord.Embed(title=(("Webページのスクリーンショット")), description=f"[URL]({url})", color=discord.Color.blue())
        embed.set_image(url="attachment://screenshot.png")
        
        translated_message = _('取得にかかった時間: {time:.2f}秒').format(time=elapsed_time)
        embed.set_footer(text=(translated_message))
        await ctx.reply(embed=embed, file=discord.File(image_stream, filename="screenshot.png"))
        
    except Exception as e:
        translated_message = _(f"エラーが発生しました：{e}").format(e=e)
        await ctx.send(translated_message)



#tracemoe
@bot.hybrid_command(name="trace", aliases=['t', 'a', "anime"],brief="スクリーンショット画像からアニメを特定します")
@allowed_installs(guilds=True, users=True)
async def trace(ctx,file:discord.Attachment):
    if ctx.interaction:
        await ctx.interaction.response.defer()
    if len(ctx.message.attachments) == 0:
        await ctx.send(("画像が添付されていません。"))
        return

    image_url = ctx.message.attachments[0].url
    res = requests.get("https://api.trace.moe/search?anilistInfo&url={}".format(urllib.parse.quote_plus(image_url))).json()

    if res.get("error", ""):
        await ctx.send(("エラーが発生しました: {}".format(res["error"])))
        return

    # json抽出ライブラリをケチってしまった結果めんどいなこれ
    result = res["result"][0]
    title = result["anilist"]["title"]["native"]
    episode = result["episode"]
    start_time = result["from"]
    end_time = result["to"]
    video_url = result["video"] + "&size=l"
    image_url = result["image"]
    similarity = result["similarity"] * 100
    is_adult = result["anilist"]["isAdult"]

    start_minutes, start_seconds = divmod(start_time, 60)
    end_minutes, end_seconds = divmod(end_time, 60)


    # Embed作成
    embed = discord.Embed(title=title, color=discord.Color.blue())
    embed.add_field(name=(("エピソード")), value=episode, inline=True)
    embed.add_field(name=(("開始地点")), value="{:02d}:{:02d}".format(int(start_minutes), int(start_seconds)), inline=True)
    embed.add_field(name=(("終了地点")), value="{:02d}:{:02d}".format(int(end_minutes), int(end_seconds)), inline=True)
    embed.add_field(name=(("一致度")), value="{:.2f}%".format(similarity), inline=True) # 一致度をパーセント表記に
    embed.add_field(name=(("動画ファイル")), value=(("[見る]({})")).format(video_url), inline=False)
    if is_adult:
        embed.add_field(name=(("注意")), value=(("不適切な表現が含まれている可能性があります。")), inline=False)
    else:
        # 画像をダウンロードしてセット
        response = requests.get(image_url)
        if response.status_code == 200:
            with open("image.jpg", "wb") as file:
                file.write(response.content)
            file = discord.File("image.jpg", filename="image.jpg")
            embed.set_image(url="attachment://image.jpg")
            await ctx.send(file=file, embed=embed)
        else:
            embed.add_field(name=(("画像の取得に失敗しました")), value=(("サーバーからの応答がありませんでした。")), inline=False)
            await ctx.send(embed=embed)





# 性別判定
@bot.hybrid_command(name="nametogender", aliases=['name', 'gender'], brief="名前から性別判定（英語のみ）します")
@allowed_installs(guilds=True, users=True)
async def name(ctx, *, name:str):
    url = f"https://api.genderize.io/?name={name}"
    response = requests.get(url)
    data = response.json()
    
    gender = data.get('gender')
    if gender == 'male':
        translated_message = _(f'{name}さんは男性です！').format(name=name)
    elif gender == 'female':
        translated_message = _(f'{name}さんは女性です！').format(name=name)
    else:
        translated_message = _(f'{name}さんの性別は不明です。').format(name=name)
    await ctx.reply(replace_at(translated_message))
# RB
@bot.command(name="reineandbuachi", aliases=['rb'], brief="おっと。。。")
async def reineandbuachi(ctx):
    await ctx.reply('Reine & Buachi House!')

# 画像検索
@bot.hybrid_command(name="imagesearch", aliases=['image', 'im', "search"], brief="Bing画像検索をします")
@allowed_installs(guilds=True, users=True)
async def imagesearch(ctx, word: str):
    if ctx.interaction:
        await ctx.interaction.response.defer()
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": word, "count": 20}
    response = requests.get(search_url, headers=headers, params=params)
    search_results = response.json()
    if "value" in search_results:
        images = search_results["value"]
        current_index = 0
        image_info = images[current_index]
        embed = discord.Embed(title=image_info["name"], description=f"{current_index + 1}/20")
        embed.set_image(url=image_info["thumbnailUrl"])
        embed.add_field(name=(("リンク先")), value=image_info["hostPageUrl"])
        message = await ctx.send(embed=embed)
        await message.add_reaction("⬅️")  
        await message.add_reaction("➡️")  
        await message.add_reaction("🔪")  
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ["⬅️", "➡️", "🔪"]
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "➡️" and current_index < len(images) - 1:
                    current_index += 1
                    image_info = images[current_index]
                    embed = discord.Embed(title=image_info["name"], description=f"{current_index + 1}/20")
                    embed.set_image(url=image_info["thumbnailUrl"])
                    embed.add_field(name=(("リンク先")), value=image_info["hostPageUrl"])
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "⬅️" and current_index > 0:
                    current_index -= 1
                    image_info = images[current_index]
                    embed = discord.Embed(title=image_info["name"], description=f"{current_index + 1}/20")
                    embed.set_image(url=image_info["thumbnailUrl"])
                    embed.add_field(name=(("リンク先")), value=image_info["hostPageUrl"])
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "🔪": 
                    await message.remove_reaction(reaction, user)
                    await ctx.reply(("処理中です！"))
                    async with aiohttp.ClientSession() as session:
                        async with session.get(image_info["contentUrl"]) as resp:
                            if resp.status != 200:
                                return await ctx.send(('画像をダウンロードできませんでした。'))
                            temp_file_path = "input.png"
                            with open(temp_file_path, "wb") as temp_file:
                                temp_file.write(await resp.read())

                            model_choices = ["u2net", "u2net_human_seg", "u2netp"]
                            with open("input.png", "rb") as f:
                                data = f.read()
                                img = remove(data, model_name=model_choices[0],
                                            alpha_matting=True,
                                            alpha_matting_foreground_threshold=240,
                                            alpha_matting_background_threshold=10,
                                            alpha_matting_erode_structure_size=10,
                                            alpha_matting_base_size=1000)
                            with open("output.png", "wb") as f:
                                f.write(img)
                            await ctx.send(file=discord.File("output.png"))
                
            except TimeoutError:
                break
    else:
        await ctx.send(("画像が見つかりませんでした。"))




# ラウドネス判定
@bot.hybrid_command(name='loudness', aliases=['l', 'loud', "loudpena"] ,brief="YouTubeでラウドネスがいくつ下がるかを判定します")
@allowed_installs(guilds=True, users=True)
async def loudness(ctx,file:discord.Attachment):
    if not ctx.message.attachments:
        await ctx.reply(("音声ファイルが添付されていません。"))
        return
    audio_url = ctx.message.attachments[0].url
    response = requests.get(audio_url)
    if response.status_code != 200:
        await ctx.reply(("音声ファイルのダウンロードに失敗しました。"))
        return
    audio_data = AudioSegment.from_file(BytesIO(response.content))
    loudness = audio_data.dBFS
    loudness_penalty = loudness - (-17.5)
    await ctx.reply((f'この音声のYouTubeでのラウドネスペナルティは -{loudness_penalty:.2f}です'))


# 背景切り抜き
@bot.hybrid_command(name='background', aliases=['bg', 'back', 'haikei'], brief="添付画像の背景を削除")
@allowed_installs(guilds=True, users=True)
async def background(ctx, url: typing.Optional[discord.Attachment]):
    if ctx.interaction:
        await ctx.interaction.response.defer()
    url = url.url
    if url is None:
    # RIP チャンネル内画像切り抜き
        async for message in ctx.channel.history(limit=15):
            if message.attachments and message.attachments[0].content_type.startswith('image'):
                url = message.attachments[0].url
                break
        else:
            await ctx.send(("チャンネル内に画像が見つかりませんでした。"))
            return

    # 画像の背景を削除
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        data={'image_url': url, 'size': 'auto'},
        headers={'X-Api-Key': removebg_key},
    )

    if response.status_code == requests.codes.ok:
        with open('no-bg.png', 'wb') as out:
            out.write(response.content)
        await ctx.send(file=discord.File('no-bg.png'))
    else:
        print("Error:", response.status_code, response.text)
        await ctx.send(("エラーが発生しました。"))

    # エラー
    error_messages = {
        'gif': (("GIFには現在対応していません。将来対応する可能性があります。")),
        'multiple_sources': (("一度に2枚以上送信しないでください。")),
        'missing_source': (("ファイルが破損しているようです。")),
        'maximum file size': (("ファイルのサイズが大きすぎます。")),
        'unknown_foreground': (("背景が検出されませんでした。")),
        'insufficient_credits': (("クレジットが不足しています。"))
    }

    for error, message in error_messages.items():
        if error in response.text:
            await ctx.send(message)
            break

# removebgbeta
@bot.hybrid_command(name='backgroundv2', aliases=['bg2', 'back2', "haikei2"], brief="添付画像の背景を削除2（ベータ）", integration_types=1)
@allowed_installs(guilds=True, users=True)
async def backgroundv2(ctx, type: int, file: discord.Attachment):

    if not ctx.message.attachments:
        await ctx.reply(("ファイルが添付されていないようです。"))
        return

    attachment = ctx.message.attachments[0]
    shurui = ctx.message.attachments[0].content_type.startswith

    if not shurui('image'):
        await ctx.reply(("添付されたファイルが画像ではないようです。"))
        return
    await ctx.reply(("処理中です..."))

    # ファイルをダウンロードして保存
    input_path = attachment.filename
    file_path = os.path.join(os.getcwd(), input_path)
    await attachment.save(file_path)
    output_path = 'output.png'
    
    if type == 1: # rembg
        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                input = i.read()
                output = remove(input)
                o.write(output)
                
                await ctx.send(file=discord.File(output_path))
        pass
    elif type == 2:
        model_choices = ["u2net", "u2net_human_seg", "u2netp"]
        with open(input_path, "rb") as f:
            data = f.read()
            img = remove(data, model_name=model_choices[0],
                         alpha_matting=True,
                         alpha_matting_foreground_threshold=240,
                         alpha_matting_background_threshold=10,
                         alpha_matting_erode_structure_size=10,
                         alpha_matting_base_size=1000)
        with open(output_path, "wb") as f:
            f.write(img)
        await ctx.send(file=discord.File(output_path))
        pass
    else:
        await ctx.send(("type には 1 または 2 を指定して下さい。"))
        return
    

# SimpleAI
@bot.hybrid_command(name="ai", aliases=['aichat', 'chat'], brief="AIと対話できます（無加工）")
@allowed_installs(guilds=True, users=True)
async def ai(ctx, word: str , file: typing.Optional[discord.Attachment]):
    if ctx.interaction:
        await ctx.interaction.response.defer()
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    if file is None:
        response = model.generate_content([word])
    else:
        file_data = await file.read() 
        img = Image.open(io.BytesIO(file_data))  
        response = model.generate_content([word, img])
    await ctx.reply(replace_at(response.text))
    
# おじさん構文
@bot.hybrid_command(name="ozisan", aliases=['o', 'oz'], brief="おじさん構文に変換します")
@allowed_installs(guilds=True, users=True)
async def imagesearch(ctx, word: str):
    if ctx.interaction:
        await ctx.interaction.response.defer()

    mess = f"""
    【以下、　プロンプト】

あなたは50代男性のおじさんです。
おじさんは[特徴:]のような文章を書きます。
[おじさん構文例:]が具体例です。
特徴と具体例を参考に、最後に伝える[入力文:]を、おじさんが書いたような文に変換してください。

[特徴:]
・タメ口で話す
・すぐに自分語りをする
（例）おじさん😎はね〜今日📅お寿司🍣を食べた👄よ〜
・ことあるごとに食事やホテルに誘う
・語尾を半角カタカナにする（例）「〜ｶﾅ？」「〜ﾀﾞﾈ！」
・「冗談」+「ﾅﾝﾁｬｯﾃ」を多用する
・若者言葉を使う
・句読点を過剰に使う
・絵文字を過剰に使う。以下、一例
・😎　サングラスの絵文字。「おじさん」「ボク」などの単語の後につけがち。「🤓」でも代替可能
・🤔　悩んでいる絵文字。「ｶﾅ？」や「大丈夫？」の後につけがち
・😂　泣き笑いの絵文字。冗談を言った時などに使う
・😅　汗の絵文字。「^^;」「（汗）」「(；・∀・)」でも代用可能
・❤️　ハートの絵文字。愛を表現するため多用する
・❗　赤いビックリマーク。強調のときに多用する。連続で使うことも多い

[おじさん構文例:]
おはよー！チュッ❤
〇〇ﾁｬﾝ、可愛らしいネ٩(♡ε♡ )۶
〇〇ﾁｬﾝ、だいすき！❤(ӦｖӦ｡)
今日のお弁当が美味しくて、一緒に〇〇チャンのことも、食べちゃいたいナ〜😍💕（笑）✋ナンチャッテ😃💗
お疲れ様〜٩(ˊᗜˋ*)و🎵今日はどんな一日だっタ😘❗❓僕は、すごく心配だヨ(._.)😱💦😰そんなときは、オイシイ🍗🤤もの食べて、元気出さなきゃだネ😆
〇〇ちゃんのお目々、キラキラ(^з<)😘😃♥ してるネ❗💕ホント可愛すぎだよ〜😆マッタクもウ😃☀ 🎵😘(^o^)
オハヨー😚😘本日のランチ🍴は奮発してきんぴらごぼう付き(^_^)😆（笑）誰だ、メタボなんて言ったやツハ(^_^;😰💦
僕は、すごく心配だよ^^;(T_T)(^_^;(-_-;)そんなときは、美味しいもの食べて、元気出さなきゃダネ😚(^з<)(^_^)😘オイラは〇〇ちゃん一筋ダヨ（￣▽￣）
誰だ△△なんて言ったやつは💦
〇〇ﾁｬﾝ、今日は、□□ｶﾅ(?_?)
おぢさんは今日、☆☆を食べたよ〜👄
ﾏｯﾀｸもう😡 
おぢさんのﾊﾞｶﾊﾞｶﾊﾞｶ(´*ω*｀)
今日も一日、がんばろう🤗└( 'ω')┘ムキッ
〇〇ﾁｬﾝが風邪🍃😷💊になると、おぢさん🤓心配！😕🤔😭
女優さんかと思った😍
〇〇ﾁｬﾝにとっていい日になりますように(≧∇≦)b
ボクは〇〇ﾁｬﾝの味方だからね👫🧑‍🤝‍🧑

[入力文:{word}]

"""

    response = co.chat(
    message=mess, 
    model="command-r-plus", 
    temperature=0.9,
    connectors=[{"id": "web-search"}]
)   
    await ctx.reply(replace_at(response.text))

# QuizAI
@bot.hybrid_command(name="quiz", aliases=['q', 'qz'], brief="Quiz")
async def quiz(ctx, *, genre: str = None):
    # ジャンル指定がないときはノンジャンル
    if genre is None:
        genre = 'random'
    if ctx.interaction:
        await ctx.interaction.response.defer()
    print ('クイズAI')
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f'「{genre}」というジャンルでクイズを1問のみ出題してください。なお、問題文のみを1行目のみに、その問題の答えのみを絶対2行目のみで応答してください。'
    response = co.chat(
        message=prompt,
        model='command-r-plus',
        temperature=1,
        connectors=[{"id": "web-search"}]
    )

    quiz_text = response.text.strip().split('\n')
    if len(quiz_text) < 2:
        await ctx.send(("クイズの生成に失敗しました。もう一度試してください。"))
        return
    
    question = quiz_text[0]
    answer = "\n".join(quiz_text[1:]).strip() 
    
    # クイズ送信
    await ctx.reply(replace_at(f"クイズのジャンル: {genre}\n質問: {question}"))

    def check(m):
        return m.channel == ctx.channel and m.author != bot.user

    correct = False
    end_time = asyncio.get_event_loop().time() + 30.0

    while not correct and asyncio.get_event_loop().time() < end_time:
        try:
            user_response = await bot.wait_for('message', check=check, timeout=end_time - asyncio.get_event_loop().time())
            user_answer = user_response.content

            # 審査中
            await user_response.add_reaction('⏳')

            # 回答審査
            validation_prompt = f'「"{question}"」という問題に対する模範解答は"{answer}"ですが、次の回答は正解になりますか？：「"{user_answer}"」正解になる場合はtrue、不正解になる場合はfalse、ギブアップと言っている場合はgiveと応答してください。なお、似ている回答でも正解とします。'
            validation_response = model.generate_content(validation_prompt)
            validation_result = validation_response.text.strip().lower()

            if validation_result == 'give':
                await user_response.clear_reaction('⏳')
                await user_response.add_reaction('🏳️')
                await ctx.send(replace_at("ギブアップ！正解は "+answer+" です。"))
                return
            elif validation_result == 'true':
                correct = True
                await user_response.clear_reaction('⏳')
                await user_response.add_reaction('✅')
                await user_response.reply(replace_at("正解！\n模範解答:"+answer))
            else:
                await user_response.clear_reaction('⏳')
                await user_response.add_reaction('❌')

        except asyncio.TimeoutError:
            break

    if not correct:
        await ctx.send(replace_at(f"時間切れです。正解は {answer} です。"))
        await ctx.send()

bot.run(TOKEN)
