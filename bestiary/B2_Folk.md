# B2. Folk

People, mostly.

This is the chapter you will use most, and it is the one where the ladder matters least — a harbour tough and a mercenary captain are not the same creature at two sizes, they are two different jobs. What they share is that every one of them can be talked to, every one of them wants something specific, and none of them is having the best night of their life either.

A note before the entries, because it changes how the whole chapter runs: **people surrender.** Not as a mercy the Mirror Master extends, but as the ordinary behaviour of ordinary people who have discovered that this fight is going worse than expected. Every morale number in this chapter is low enough to fire early, and every Breaks line means it. If the fights in your game routinely end with everyone on one side dead, something has gone wrong upstream of the dice.

---

## The Ordinary Dangerous

*The three of them have stopped talking. One is still holding a cup. The one in the middle — older, with a look of having done this before and not enjoyed it then either — steps forward half a pace and puts a hand out, palm down, in the universal gesture for* let's all slow down.

These are the people who fight for a living without being soldiers about it: dock muscle, watch officers, veterans who took the pension and found the pension insufficient. They are the commonest antagonist in any campaign, and they are almost never the antagonist for very long, because their reasons for being in the fight are usually somebody else's reasons.

**None of them is fighting for a cause.** A harbour tough is fighting because a job pays. A watch sergeant is fighting because a report has to say something. A veteran soldier is fighting because they know how, and because the alternative was the pension. Every one of those is a negotiable position, and a party that identifies which one they are facing has already found the exit.

<!-- statblock: harbor_thug -->

**Harbor Thug** · *Level 1 Mook* · Club, boat hook, or the nearest piece of cargo

**HP** — (drops to any hit) · **Armor** 0 · **Attack** +0 · **Damage** 3 · **Attacks** 1 · **Morale** 5

*Attacks as a mob: +1 damage per extra Mook (max +4).*

**Wants:** Paid, and home before anything goes badly.

**Special:** NUMBERS FIRST — fewer than four thugs will not start a fight: they posture, shout, and wait for more to arrive. From four up they attack as one mob.

**Tells:** They keep counting each other, and the loudest one keeps looking back at whoever hired them.

**Breaks:** Runs, loudly, the moment whoever they are working for goes down or leaves, and takes the nearest portable cargo along.

**Twists (d6):**

1. They are owed a week's wages and have just worked out they are not getting it.
2. One of them is somebody a party member knows, and would much rather not have been recognised.
3. The fight is on a pier: anyone who goes in the water is out of it until someone fishes them out.
4. They were hired to frighten, not to hurt, and nobody told them what to do if someone got hurt.
5. A second crew, hired by somebody else for the same job, arrives in the middle of it.
6. Their employer is watching from a window and will not come down.

**Nastier:** A crew boss is with them: a level 2 standard, and the thugs do not check morale while the boss is standing.

*`enemies/harbor_thug.fof`*

<!-- /statblock -->

<!-- statblock: city_watch_sergeant -->

**City Watch Sergeant** · *Level 3 Standard* · Cudgel

**HP** 14 · **Armor** 1 · **Attack** +2 · **Damage** 6 · **Attacks** 1 · **Morale** 8

**Wants:** An arrest, a clean report, and nobody dead on this shift.

**Special:** BACKUP — if the fight runs past its second exchange, the sergeant has already whistled: at the end of the third exchange, two watch arrive (level 1 Mooks).

**When bloodied:** Guard comes down low. It Defends every exchange (no attack; attacks on it are Hard) until help arrives or the party is clearly losing.

**Tells:** It keeps glancing up the street, and the whistle is already on its lanyard.

**Breaks:** Surrenders, or accepts a surrender, at once, and starts the paperwork.

**Twists (d6):**

1. The sergeant has the wrong people, knows it, and still has to arrest somebody.
2. The sergeant's brother-in-law owns the warehouse the party is standing in.
3. It is the end of a double shift, and the sergeant will take any excuse to go home.
4. The backup is already here, out of sight, and heard everything the party just said.
5. The order came from someone the sergeant does not trust, and the sergeant would like to be talked out of it.
6. A crowd has gathered, and it is on the party's side.

**Nastier:** A watch captain: level 5, and the backup arrives at the end of the second exchange.

*`enemies/city_watch_sergeant.fof`*

<!-- /statblock -->

<!-- statblock: veteran_soldier -->

**Veteran Soldier** · *Level 4 Elite* · Soldier's sword

**HP** 34 · **Armor** 1 · **Attack** +2 · **Damage** 7 · **Attacks** 2 · **Morale** 9

**Wants:** To be paid, to go home, and to finish this without a new scar.

**Special:** TELEGRAPHED FINISHER — once per scene, against a character already below half HP, it names the blow a full exchange early: the measured step, the blade drawn back. Next exchange it makes that one attack, and only that one, and a hit deals double damage.

**When bloodied:** It stops committing and Defends (no attack; attacks on it are Hard) until someone in the party is below half HP; then it comes back for them.

**Tells:** It watches weight, not weapons, and it has not wasted a movement since the fight started.

**Breaks:** Withdraws in good order when the fight stops being worth the wound. It never routs: it walks backwards, blade up.

**Twists (d6):**

1. Three of them served together, and all three will leave at the same moment.
2. It recognises a party member's training, and says out loud where they learned it.
3. It is guarding someone it despises, for money it needs.
4. It carries an old wound: on a natural 12 against it, the wound opens and it withdraws.
5. Its pension was stopped last month, and whoever stopped it is the party's real opponent.
6. It offers single combat, to spare the people it came with.

**Nastier:** Level 6, and it can name the Finisher twice a scene.

*`enemies/veteran_soldier.fof`*

<!-- /statblock -->

> **What Characters Can Know — the ordinary dangerous**
>
> **6−** — *"They've done this before. Not the fighting — the standing there deciding whether to fight."*
>
> **7–9** — *"Nobody here is being paid enough to die. The one in the middle is the one who decides, and the other two are watching them, not us."*
>
> **10+** — *"You can name their price out loud. Every one of these people has a specific reason to be in this doorway tonight, and none of the reasons is you — figure out whose problem you actually are, and you can hand it back to them."*

**Encounters.**

- **Four toughs and a doorway** *(four level 1 Mooks — easy)*. A tutorial fight, and the right place to teach the exchange: you say what the mob is about to do, the players answer it, and the mob's one attack is rolled where everyone can see it. Two down and the other two usually break.
- **The watch turns up** *(three sergeants and a runner: three level 3 standards and a Mook — hard for a new party)*. Three sergeants and a runner, and the party is on the wrong side of something procedural. The fight is winnable. The arrest is survivable. The report is the actual problem.
- **Old company, bad contract** *(three level 4 elites — deadly for a new party; save it for later)*. Three veteran soldiers who served together, now working for somebody the party would rather they were not. Every one of them will withdraw in good order the moment the fight stops being worth the wound, and they know each other well enough to go at the same time.
- **The favour** *(no fight)*. A watch sergeant is standing between the party and where they need to be, and has been ordered to. Ask what the order was. Somebody wrote it, and that somebody is reachable.

**Ecology.** A city's supply of the ordinary dangerous is roughly proportional to its supply of people who need something moved, guarded, or discouraged. They know each other. That is the fact worth remembering: the tough on the dock and the sergeant on the wall drink in the same three places, and a party that makes an enemy of one has made a mildly inconvenienced acquaintance of the other forty. Word travels at the speed of a shift change.

**Adaptation.** These need no adaptation; they are wherever people are. What varies is the institution behind them, and the entry improves the more specific you make it. "A watch sergeant" is a card. "A watch sergeant whose brother-in-law owns the warehouse" is an encounter.

---

## The Bought

*Five of them, in matched coats, and the coats are the tell — nobody outfits five people identically for cheap. They have taken up positions rather than walked into a room. One of them, at the back, is unhurriedly opening a leather case at their hip and taking out a folded document.*

The Bought are a mercenary company, and the joke the company makes about itself is that its most dangerous asset is the paperwork. It is not a joke. A Bought contract runs to several pages, specifies objectives and boundaries and permitted force with the precision of a shipping manifest, and is produced and read aloud at the start of engagements more often than weapons are drawn.

**This is not decoration. It is the entire creature.** A company that fights strictly to written terms is a company you can defeat by changing the terms, and the Bought know that better than anyone, which is why the contract case is chained to the belt and why the captain is the only person who has read the second clause.

They have existed in some form in every settled region for as long as anyone has been able to write down what they wanted done. The name changes. The case does not.

<!-- statblock: bought_blade -->

**Blade of the Bought** · *Level 2 Mook* · Company blade, or a cudgel on a contract to detain

**HP** — (drops to any hit) · **Armor** 1 · **Attack** +0 · **Damage** 4 · **Attacks** 1 · **Morale** 6

*Attacks as a mob: +1 damage per extra Mook (max +4).*

**Wants:** The contract's terms met and the fee paid.

**Special:** TO THE TERMS — Blades fight only as the contract allows and never cross its boundary. On a contract to detain, a character their hits would drop to 0 HP is left at 1 HP and held instead.

**Tells:** Matched coats, positions taken rather than a room walked into, and someone at the back opening a document case.

**Breaks:** Disengages in good order and walks back to the boundary. Nobody in the Bought has ever been paid enough to die for a clause.

**Twists (d6):**

1. The contract is to delay, not to stop: they only need to hold for three exchanges.
2. The contract names one party member, and the Blades step politely around everyone else.
3. The boundary is a painted line on the floor of this room, and the party is standing on it.
4. One Blade is new and does not yet know exactly where the boundary is.
5. The fee was paid in bad coin, and the Blades have just been told.
6. They are escorting a prisoner who very much wants the party to win.

**Nastier:** Their sergeant is in earshot, and has already said where the boundary is.

*`enemies/bought_blade.fof`*

<!-- /statblock -->

<!-- statblock: bought_sergeant -->

**Sergeant-at-Arms** · *Level 3 Standard* · Company blade, drawn second; the contract case, drawn first

**HP** 14 · **Armor** 1 · **Attack** +2 · **Damage** 6 · **Attacks** 1 · **Morale** 8

**Wants:** The contract satisfied or voided. Either one ends the fight.

**Special:** HOLD THE TERMS — once per scene, the sergeant states the contract's boundary aloud, and every Blade in earshot at once behaves as though the boundary is where the sergeant just said it is.

**When bloodied:** Calls the Blades back to the boundary and starts offering terms out loud, still fighting.

**Tells:** It opens by reading the contract's terms aloud. This is not a bluff; it is how the company works.

**Breaks:** Surrenders the field the moment the contract is void (payment withdrawn, terms broken by the employer, or the named target gone), says so, and expects to be believed.

**Twists (d6):**

1. The employer broke the terms an hour ago, and the sergeant does not know yet.
2. The sergeant has read the contract twice and privately thinks the party is right.
3. Two sergeants, two fours, and the fours have been told two different boundaries.
4. The named target is standing behind the sergeant, and is a friend of the party.
5. The contract case is gone from its belt, stolen, and the sergeant is improvising.
6. The party splits up, and the sergeant spends Hold the Terms to keep every Blade on one side of the line.

**Nastier:** Level 5, and Hold the Terms can be used again each time a Blade falls.

*`enemies/bought_sergeant.fof`*

<!-- /statblock -->

<!-- statblock: bought_captain -->

**Captain-under-Contract** · *Level 4 Boss* · A very good sword it would rather not draw

**HP** 85 · **Armor** 2 · **Attack** +3 · **Damage** 9 · **Attacks** 2 · **Morale** 9

*Changes phase when Bloodied (half HP).*

**Wants:** The fee, the company intact, and the reputation that gets the next contract.

**Special:** THE SECOND CLAUSE — once per fight, in the exchange after the party looks like winning, the captain invokes the clause only it has read, and the company's objective changes mid-scene in a direction the party did not plan for.

**When bloodied:** It starts negotiating out loud, mid-exchange, while the attacks continue. Anyone who answers is talking to someone genuinely listening. If the fight is going long, do this on its second exchange on the field instead of waiting.

**Tells:** It spends the opening exchange placing Blades and watching who the party protects. The contract case is chained to its belt.

**Breaks:** Calls the withdrawal and means it. A captain who has called a withdrawal will not resume the fight tonight for any inducement, including a better offer.

**Twists (d6):**

1. The Second Clause is to take the party alive and deliver them to the employer.
2. The Second Clause voids the contract if the employer lied, and the employer lied.
3. A better offer, made in front of the sergeants, ends this before it starts.
4. Half the company are Blades the party has already beaten once, and they remember.
5. The captain is still hurt from the last engagement and wants this to be short.
6. The employer has come onto the field, and the captain would very much prefer otherwise.

**Nastier:** REFORM THE LINE — once per scene, and only if the company still has somewhere to withdraw to, every Blade that disengaged this scene returns to the field in good order.

*`enemies/bought_captain.fof`*

<!-- /statblock -->

> **What Characters Can Know — the Bought**
>
> **6−** — *"Matched coats, and they took positions instead of walking in. That's a company, not a mob."*
>
> **7–9** — *"They fight to a contract, and they'll tell you what's in it if you ask — they'd rather you knew, because most people leave once they hear. There's a boundary written down somewhere and they will not cross it."*
>
> **10+** — *"Buy the contract. It's for sale, it has always been for sale, and it is the only thing the Bought actually sell. And there's a second clause the sergeants haven't read — if the fight turns and the captain suddenly changes what they're doing, that's what happened."*

**Encounters.**

- **A four and a sergeant** *(one sergeant and four Blades — a fair fight)*. The company's basic unit, doing a basic job. Ask what the job is.
- **Three sergeants holding a line** *(three sergeants and a Blade — hard)*. Different fours, same contract, and Hold the Terms means the boundary is wherever the sergeants have agreed it is. The party can move the boundary by moving the sergeants' understanding of it.
- **The captain's engagement** *(the captain, two sergeants and four Blades — deadly, and written to be resolved rather than won)*. The Second Clause fires the exchange after the party looks like winning, and once the captain is bloodied (or on its second exchange, if the fight is running long) it starts negotiating out loud, mid-fight, while the attacks continue. A party that answers is talking to somebody who is genuinely listening.
- **The counter-offer** *(no fight)*. The party has money, or leverage, or a better employer. Making the offer in front of the sergeants is the difference between a negotiation and an insult, and the entry is explicit about that because players will not guess it.

**Ecology.** A region with an active company in it has a strange kind of peace: violence becomes contractual, predictable, and bounded, which is much better than the alternative and much worse than it sounds. Disputes that would have been settled by feud get settled by competing engagements instead, and everybody involved goes home. The Bought are widely disliked and universally hired.

**Adaptation.** The contract can be a writ, a geas, a debt of service, or a religious commission — anything binding, written down, and transferable. Keep three things: the boundary the company will not cross, the fact that the terms are read aloud, and the buy-out. A mercenary company that cannot be bought out is not this entry; it is a war.

---

## The Kindly

*Something waist-high is standing at the crossing, holding a thing out to you in both hands. It has been holding it out for a while, and it does not seem tired. It is dressed in what somebody gave it — several somebodies, over what must be a long time, in styles that have not been fashionable together within living memory. It says good evening, in your language, and waits.*

The Kindly are the reason travellers in some regions carry one useless valuable thing.

They appear singly, at thresholds — crossings, bridges, doorways, the place where a road becomes a different road, the spot where something was lost. They are always holding something out. They always speak first, always politely, always in whatever language they were addressed in or, absent that, the language of the person they most recently traded with. They want to trade, and the trade is always genuinely offered.

**A Kindly One cannot decline a fair offer and cannot forgive an unfair one.** Both halves of that are absolute and neither is a metaphor. They know fair from unfair without being told, they define fair generously — what a thing is *worth to its owner*, not what it would fetch — and they have never once been argued out of either judgement.

Nobody knows what they do with what they are given. The Kindly do not say, and the several people who have followed one have all reported the same thing, which is that they did not manage it.

<!-- statblock: kindly_one -->

**A Kindly One** · *Level 2 Standard* · None. It is holding something out.

**HP** 11 · **Armor** 0 · **Attack** +1 · **Damage** 5 · **Attacks** 1 · **Morale** 2

**Wants:** A fair trade, where fair means what a thing is worth to its owner.

**Special:** FAIR DEALING — it cannot decline a genuinely fair offer, and knows fair from unfair without being told: no roll, and the MM does not get to refuse on its behalf. Cheat it once and neither it nor any other Kindly One ever trades with that person again: no roll, and no apology that works.

**When bloodied:** It leaves, whatever the morale roll said.

**Tells:** It spoke first, politely, in your language, and it has been holding the thing out for longer than anyone should be able to.

**Breaks:** It never strikes back. If struck it Defends (attacks on it are Hard) and leaves at the end of the exchange, and does not come back. Neither does any other Kindly One, anywhere, for the rest of the campaign.

**Twists (d6):**

1. What it holds out is something the party will need later and cannot yet know they want.
2. It is holding out something a party member lost years ago.
3. Someone at the crossing already cheated one, and is trying to get the party to trade on their behalf.
4. It wants something nobody in the party thinks is worth anything, and it is right.
5. A local has taught the party the rhyme. The rhyme is wrong about two details and right about the important one.
6. It has been given so many coats that it can barely lift its arms, and it would like to trade one away.

*`enemies/kindly_one.fof`*

<!-- /statblock -->

> **What Characters Can Know — the Kindly**
>
> **6−** — *"It spoke first, and it's waiting. Whatever this is, it isn't an ambush."*
>
> **7–9** — *"A Kindly One. It'll trade, honestly, and it can't turn down a fair offer — but 'fair' means what the thing is worth to you, not what it's worth. Don't try to be clever."*
>
> **10+** — *"Cheat one and you have cheated all of them, permanently. Not this one — all of them, everywhere, for the rest of your life. There is no apology, no restitution, and no known exception. There are people alive today who cannot buy bread at a crossing because of something they did as an apprentice."*

**Encounters.**

- **The crossing** *(no fight, and there is no version of this that is a fight)*. It is holding something out. That is the encounter. What it is holding should be something the party will want later and cannot yet know they want.
- **The unfair trade** *(no fight)*. A party member gets greedy or gets clever. Nothing happens. Nothing at all happens, and then for the rest of the campaign nothing continues to happen, at every crossing, forever, and the entry is explicit that the Mirror Master should not soften this.
- **If the party attacks it** *(one level 2 standard — no fight at all, and a catastrophe by any measure that matters)*. It has numbers because a table that starts a fight needs some to finish. It never strikes back, and it leaves at the first hurt. Nothing in this book costs a campaign more.

**Ecology.** In regions where the Kindly are known, the local etiquette is intricate and universally observed, and outsiders find it baffling. People carry a token valuable specifically for crossings. Parents drill children on what to say. There is usually a rhyme. The rhyme is usually wrong about several details and right about the important one, which is *do not be clever at the bridge*.

**Adaptation.** They can be small folk, spirits, masked children, a very old animal — anything that can hold something out and wait. Keep the threshold, keep the two absolutes, and keep the fact that the fair trade is genuinely good for the party. A Kindly One who offers junk is a riddle. A Kindly One who offers something wonderful is a temptation, and temptation is what this entry is for.
