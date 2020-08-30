#!/usr/bin/python

import discord
import json
import requests
import datetime
import asyncio

from discord.ext import commands

# Token
TOKEN = "Discord token of your bot"

bot = commands.Bot(command_prefix='$', description='Price Bot')


@bot.event
async def on_ready():
	print("Teloscoin Price Bot Started")
	print("Bot username: ", bot.user.name)
	print("Bot id: ", bot.user.id)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="TELOS Price"))


@bot.command(pass_context=True)
async def price(ctx):
	if ctx.message.guild == None:
		return

	async with ctx.channel.typing():


		crex_link = "https://crex24.com/exchange/TELOS-BTC"
		grav_link = "https://graviex.net/markets/telosbtc"
		south_link = "https://www.southxchange.com/Market/Book/TELOS/BTC"
		biki_link = "https://www.biki.com/trade/TELOS_USDT"
		birake_link = "https://dex.bitdorado.exchange/market/BIRAKE.TELOS_BIRAKE.BTC"
		xbtx_link = "https://dex.bitdorado.exchange/market/BIRAKE.XBTX_BIRAKE.TELOS"

		# Southxchange
		try:
			southxchange = "https://www.southxchange.com/api/price/TELOS/BTC"
			south_get = requests.get(southxchange)

			south_last = str("{:.8f}".format(south_get.json()["Last"]))
			south_bid = str("{:.8f}".format(south_get.json()["Bid"]))
			south_ask = str("{:.8f}".format(south_get.json()["Ask"]))
			south_dif = str(south_get.json()["Variation24Hr"])
			south_v = float("{:.1f}".format(south_get.json()["Volume24Hr"]))
			south_vol = round(south_v)
		except (KeyError, ValueError, ConnectionError, requests.exceptions.RequestException, ConnectionResetError):
			south_last = "Error"
			south_bid = "Error"
			south_ask = "Error"
			south_dif = "Error"
			south_vol = "Error"

		# Graviex
		try:
			graviex = "https://graviex.net:443//api/v2/tickers/telosbtc.json"
			grav_get = requests.get(graviex)

			grav_last = grav_get.json()["ticker"]["last"]
			grav_bid = grav_get.json()["ticker"]["buy"]
			grav_ask = grav_get.json()["ticker"]["sell"]
			grav_dif = str("{:.1f}".format(grav_get.json()["ticker"]["change"]))
			grav_v = float(grav_get.json()["ticker"]["vol"])
			grav_vol = round(grav_v)
		except (KeyError, ValueError, ConnectionError, requests.exceptions.RequestException, ConnectionResetError):
			grav_last = "Error"
			grav_bid = "Error"
			grav_ask = "Error"
			grav_dif = "Error"
			grav_vol = "Error"

		# Crex24
		try:
			crex = "https://api.crex24.com/v2/public/tickers?instrument=TELOS-BTC"
			crex_get = requests.get(crex)

			crex_last = str("{:.8f}".format(crex_get.json()[0]["last"]))
			crex_bid = str("{:.8f}".format(crex_get.json()[0]["bid"]))
			crex_ask = str("{:.8f}".format(crex_get.json()[0]["ask"]))
			crex_dif = str("{:.2f}".format(crex_get.json()[0]["percentChange"]))
			crex_v = float("{:.1f}".format(crex_get.json()[0]["baseVolume"]))
			crex_vol = round(crex_v)
		except (KeyError, ValueError, ConnectionError, requests.exceptions.RequestException, ConnectionResetError):
			crex_last = "Error"
			crex_bid = "Error"
			crex_ask = "Error"
			crex_dif = "Error"
			crex_vol = "Error"

		# Biki
		try:
			biki = "https://openapi.biki.com/open/api/get_ticker?symbol=telosusdt"
			biki_get = requests.get(biki)

			biki_last = biki_get.json()["data"]["last"]
			biki_bid = biki_get.json()["data"]["buy"]
			biki_ask = biki_get.json()["data"]["sell"]
			biki_v = float(biki_get.json()["data"]["vol"])
			biki_vol = round(biki_v)
		except (KeyError, ValueError, ConnectionError, requests.exceptions.RequestException, ConnectionResetError):
			biki_last = "Error"
			biki_bid = "Error"
			biki_ask = "Error"
			biki_vol = "Error"

		# Bitdoradodex
		try:
			birake = "https://api.birake.com/public/v3/ticker"
			bir = requests.get(birake).json()

			for k in bir:
				for x, y in k.items():

					if y == "TELOS_BTC":
						bir_last = k["lastPrice"]
						bir_bid = k["highestBid"]
						bir_ask = k["lowestAsk"]
						bir_v = float(k["quoteVolume24h"])
						bir_vol = round(bir_v)
		except (KeyError, ValueError, ConnectionError, requests.exceptions.RequestException, ConnectionResetError):
			bir_last = "Error"
			bir_bid = "Error"
			bir_ask = "Error"
			bir_vol = "Error"

		# Bitdoradodex-xbtx
		try:
			bir_xbtx = "https://api.birake.com/public/v3/ticker"
			xbtx_get = requests.get(bir_xbtx).json()

			for m in xbtx_get:
				for a, b in m.items():

					if b == "XBTX_TELOS":
						xbtx_last = m["lastPrice"]
						xbtx_bid = m["highestBid"]
						xbtx_ask = m["lowestAsk"]
						xbtx_v = float(m["quoteVolume24h"])
						xbtx_vol = round(xbtx_v)
		except (KeyError, ValueError, ConnectionError, requests.exceptions.RequestException, ConnectionResetError):
			xbtx_last = "Error"
			xbtx_bid = "Error"
			xbtx_ask = "Error"
			xbtx_vol = "Error"



		embed=discord.Embed(title="Teloscoin Price Ticker", color=0x131338)


		embed.add_field(name="Crex24 (BTC)", value="**|Price: **{}\n**|Vol: **{} **TELOS**\n**|Bid: **{}\n**|Ask: **{}\n**|Chg: **{}%\n[Link]({})".format(crex_last, crex_vol, crex_bid, crex_ask, crex_dif, crex_link), inline=True)

		embed.add_field(name="Graviex (BTC)", value="**|Price: **{}\n**|Vol: **{} **TELOS**\n**|Bid: **{}\n**|Ask: **{}\n**|Chg: **{}%\n[Link]({})".format(grav_last, grav_vol, grav_bid, grav_ask, grav_dif, grav_link), inline=True)

		embed.add_field(name="Southxchange (BTC)", value="**|Price: **{}\n**|Vol: **{} **TELOS**\n**|Bid: **{}\n**|Ask: **{}\n**|Chg: **{}%\n[Link]({})".format(south_last, south_vol, south_bid, south_ask, south_dif, south_link), inline=True)

		embed.add_field(name="Biki (USDT)", value="**|Price: **{}\n**|Vol: **{} **TELOS**\n**|Bid: **{}\n**|Ask: **{}\n**|Chg: **Not Supported\n[Link]({})".format(biki_last, biki_vol, biki_bid, biki_ask, biki_link), inline=True)

		embed.add_field(name="BitdoradoDEX (BTC)", value="**|Price: **{}\n**|Vol: **{} **TELOS**\n**|Bid: **{}\n**|Ask: **{}\n**|Chg: **Not Supported\n[Link]({})".format(bir_last, bir_vol, bir_bid, bir_ask, birake_link), inline=True)

		embed.add_field(name="Bitdorado (XBTX)", value="**|Price: **{}\n**|Vol: **{} **XBTX**\n**|Bid: **{}\n**|Ask: **{}\n**|Chg: **Not Supported\n[Link]({})".format(xbtx_last, xbtx_vol, xbtx_bid, xbtx_ask, xbtx_link), inline=True)

		embed.set_footer(text=datetime.datetime.now().strftime("Time | %d/%m/%Y %H:%M"))
		
		await asyncio.sleep(10)
		await ctx.send(embed=embed)



bot.run(TOKEN)
