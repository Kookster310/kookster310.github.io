---
title: PiHole - Home DNS Server for Ad Blocking and Traffic Analysis
date: 2018-01-20
---

# PiHole - Home DNS Server for Ad Blocking and Traffic Analysis

![Pi-hole](../assets/img/pi-hole.png)

I'm an avid supporter of home automation. I enjoy making devices smarter and allowing communication across services and devices. Not only to make everyday living easier, but just because it's fun. With all the gadgets and toys around, I wanted to get more insight into what is going on within my network. I decided to grab one of my unused Raspberry Pis and get an internal recursive DNS server going. I could get the information I was looking for and block some unwanted domains in the process.

I decided to go with the open source project [Pi-Hole](https://pi-hole.net/). Once I got it up and running and had all my devices pointed to it, I noticed some interesting things going on in my network.

## 1. Your Alexas, Google Homes, and Apple HomePods are making a lot of calls… Like a lot!

One of the first things I noticed was the number of queries that were being made from my Amazon Alexa devices. You would figure that these devices are making some checkback calls to make sure that they are up and running. Makes sense, right? What's puzzling to me, is where some of these queries are going.

This image shows the top allowed domains that are being requested over a one-week period. This doesn't show the domains being blocked, only the allowed calls.

Some of these make sense to me. I have dynamic DNS set up on my router, so that would account for the checkip requests at the top. Unifi is the Ubiquiti service I use to manage my Access Points, that checks out. Cryptopanic would be the bots spamming Crypto news in some of the discord channels I'm in, okay makes sense…

Almost **4,600 queries to example.com**, another almost **4,600 to example.net**, and a final trifecta of **4,571 queries to example.org**… now that's random.

I checked and saw that all the queries are coming from my Amazon Alexa devices. Alexa is making almost a thousand calls a day to example.com, net, and org. I mean you'd think they would do these calls to a domain that they own (I double checked, example.com is on Edgecast's network. I'm pretty sure Amazon uses their own CloudFront as their main CDN). Maybe they want to offload what looks like heartbeat traffic to another network? Not sure why you'd do that as you are still incurring the payload costs regardless, but whatever.

## 2. Metrics, metrics, metrics…

So Alexa is making some weird calls. Okay, not that big a deal. It is a large number but not that bad, especially when compared to the metrics calls being made.

So again, in first place with whopping **35,393 total calls made: Alexa!**

Alexa made 35,000 DNS queries over a 7-day period. This is with a single Amazon Alexa and an Alexa Dot. What makes me think this URL is not really a true heartbeat query is that everything still works. I am actively blocking Alexa from reaching this destination, but she (yes, I have officially humanized my Alexa) is still able to function and do everything she needs to. I'm still able to control my other devices like my Nest thermostat and my Hue smart bulbs. This leads me to believe that this is more in tune with data gathering.

The next 4 culprits on my list all belong to one OS: **Microsoft Windows**. The IP address would be my home desktop. My Windows desktop seems to like analytics as much as the next guy, it did make over 32,000 calls over the last week.

## 3. No more ads, tracking, and other nonsense

**Over 40%.** That's how much of my internet traffic is being blocked locally. Sitting at **44.3%** at the time of writing.

With the built-in filter list, we get just over **120k domains** on the block list. There are some other lists that people have developed to lock it down even further, but right now I'm running stock.

It's pretty gnarly to think of the amount of traffic that is destined for crap I not only don't need, but really don't want. This is the first time I've had a data cap with my ISP, 1TB a month iirc. With all the IoT devices there are, you would imagine all this chatter would start to add up.

## 4. If you have IPv6 in your network and can't adjust DNS for IPv6, you're going to have a bad time

Before I got my current equipment, I used a Netgear C6300 all-in-one Wireless Router/Modem device. It was an okay device, got what I needed to get done for the most part. When I got the Pi-Hole in place, I noticed some devices were still seeing ads. I checked my Netgear and saw that the DNS was pointed to Pi-Hole properly, but the Pi-Hole logs were not showing the massive number of requests I was anticipating. Digging a little deeper I found out why, our good friend **IPv6**.

Apparently this $160 router/modem did not have the ability to change your IPv6 DNS server. Ugh…

I reached out to Cox, my ISP. After shifting around a few different representatives, I finally got some info. Believe it or not, they were unable to help me. They wouldn't stop sending their IPv6 DNS server info over to me. I need Business Class to be able to do cool stuff like that. Fun…

I decided that was just enough annoyance to get me to go out and buy proper equipment. I drove to my nearby Microcenter and bought me a fancy new Ubiquiti Edge Router, Arris Surfboard, and Ubiquiti Unifi AP. With the new router I'm able to utilize IPv4 and IPv6 if I want (I don't) while keeping my Pi-Hole intact. This new equipment is so much better… I should've bought it a while ago.

**Little side note on the IPv6 debacle:** The Pi-Hole also has a DHCP service that you can set up. In the interim from having my new equipment and still rolling with the C6300, I offloaded DHCP duties to my Pi-Hole. This took care of the IPv6 issues but meant that my Pi-Hole was now my DHCP server.

## Conclusion

I'm glad the DNS server is up and running. I have more insight into what's going on within my local network. Though it was initially set up for blocking ads, it exposed a lot of things happening under the hood of my network.
