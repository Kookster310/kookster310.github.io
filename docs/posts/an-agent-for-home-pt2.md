---
title: "An Agent for Home Part 2: Electic Boogaloo"
date: 2026-02-12
---

# Mail Time

Part 1 here: [Part 1](an-agent-for-home.md)

Time to extend the workflow to outside of the agent TUI.
I wanted my agent to start becoming a little more autonomous. Setting up the daemon was a good start, but actually getting it to do things without me sending commands in the terminal is really the next step in all of this. Probably setting up some sort of queue in Redis and having it listen to events is probably the correct way to do things, but that doesn't really feel "human" enough for me. The whole idea behind agents was to have it interact with outside services and such on your behalf, like a human. 
Any shmuck can use Redis, but my agent deserves better. 

It deserves a gmail account.

Now obviously I can't just have any ol' Dick or Harry send my agent an email and obliterate my home server. I needed to add some safeguards, and not just some instructions in a .md file someone could tell the agent to ignore. I decided the best way to do this would be an email inbox checker SKILL.md + Gmail labels. 

Normally in a business google workspace account, you can set up a blacklist to just delete emails that don't come from a specific person. But I was too cheap to spend the extra money on creating a user for this agent. So after setting up it's free gmail account, I created a filter in Gmail that applied the tag "Allowed" to any email that was received from my personal daniel.ryan@310networks.com email address. After adding the specific instructions to search only for that label in the SKILL.md, I set up an hourly cronjob to ask the agent to check it's inbox for any new tasks and complete them accordingly.

<img src="../assets/img/agent-inbox.png" alt="Agent inbox" width="800">

I ran some test emails trying to get the agent to run a command from an email other than the ones marked allowed. Each time the email was properly left unread, while the emails labeled "Allowed" were properly processed. So far so good. 

Much like the Epstein files, here is a heavily redacted image of an email:

![Redacted email task completed](../assets/img/agent-email-task-completed.png)

I have some friends and family that use some of the services I self-host.
The idea behind this was to give them [REDACTED]. I could add a select few users to the "Allowed" list to have them interact with the agent directly. Allowing them to [REDACTED] without needing to reach out to me to [REDACTED] for them.