# RisingWarBot

Small discord bot script for the mobile game Clash of Clans, allows you to search up player as well as clan info.

Before doing anything you need a Clash of Clans API account, from which you can create a token permitting you to use their API from some ip address.
https://developer.clashofclans.com/#/

Best way to make this bot run is to run it on AWS. You need to assign your AWS EC2 an elastic (aka static) IP address, which you will use when creating a valid CoC API Token.

The bot also needs a discord token (don't remember) if you decide to run this script yourself.
You can set up the discord bot permissions here: https://discord.com/developers/applications

Paste the token (x) into this command, where x is a string
client.run(x)
