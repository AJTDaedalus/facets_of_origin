# B2. Folk

People, mostly.

This is the chapter you will use most, and it is the one where the ladder matters least — a harbour tough and a mercenary captain are not the same creature at two sizes, they are two different jobs. What they share is that every one of them can be talked to, every one of them wants something specific, and none of them is having the best night of their life either.

A note before the entries, because it changes how the whole chapter runs: **people surrender.** Not as a mercy the Mirror Master extends, but as the ordinary behaviour of ordinary people who have discovered that this fight is going worse than expected. Every morale line in this chapter is written to fire early and mean it. If the fights in your game routinely end with everyone on one side dead, something has gone wrong upstream of the dice.

---

## The Ordinary Dangerous

*The three of them have stopped talking. One is still holding a cup. The one in the middle — older, with a look of having done this before and not enjoyed it then either — steps forward half a pace and puts a hand out, palm down, in the universal gesture for* let's all slow down.

These are the people who fight for a living without being soldiers about it: dock muscle, watch officers, veterans who took the pension and found the pension insufficient. They are the commonest antagonist in any campaign, and they are almost never the antagonist for very long, because their reasons for being in the fight are usually somebody else's reasons.

**None of them is fighting for a cause.** A harbour tough is fighting because a job pays. A watch sergeant is fighting because a report has to say something. A veteran soldier is fighting because they know how, and because the alternative was the pension. Every one of those is a negotiable position, and a party that identifies which one they are facing has already found the exit.

<!-- statblock: harbor_thug -->

**Harbor Thug** · *Mook* · **TR 2**

**When they act on it:** Resolve — · armor none · defense +0

**When it acts:** attack +0 · incoming Tier 1

**Disposition:** Muscle for hire, and unenthusiastic about it.

**Morale:** Alone, a harbour thug is atmosphere, not a threat, and behaves like it.

**Appears:** Effective in groups of four or more; below that they posture and wait for numbers.

*`enemies/harbor_thug.fof`*

<!-- /statblock -->

<!-- statblock: city_watch_sergeant -->

**City Watch Sergeant** · *Named* · **TR 8**

**When they act on it:** Resolve 3 · armor light (+1 Resolve) · defense +2

**When it acts:** attack +2 · incoming Tier 2

**Disposition:** Methodical, uninspired, and very hard to rattle.

**In play:**

- Opens Measured; shifts to Defensive if Staggered.
- Goes Aggressive only if the party is clearly losing.
- Calls for backup if the fight runs more than two exchanges.

**Morale:** Fights to arrest, not to kill. Surrender ends the fight immediately and starts the paperwork.

**Appears:** One sergeant per four to six watch on a shift.

*`enemies/city_watch_sergeant.fof`*

<!-- /statblock -->

<!-- statblock: veteran_soldier -->

**Veteran Soldier** · *Named* · **TR 10**

**When they act on it:** Resolve 4 · armor light (+1 Resolve) · defense +3

**When it acts:** attack +3 · incoming Tier 2

**Disposition:** Trained, unhurried, and entirely without anything to prove.

**Morale:** Withdraws in good order when a fight stops being worth the wound. Does not rout.

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

- **Four toughs and a doorway** *(4 Mooks — Skirmish)*. A tutorial fight, and the right place to teach postures and reactions. Two down and the other two disengage.
- **The watch turns up** *(3 Named + 1 Mook — Standard)*. Three sergeants and a runner, and the party is on the wrong side of something procedural. The fight is winnable. The arrest is survivable. The report is the actual problem.
- **Old company, bad contract** *(3 Named + 2 Mooks — Hard)*. Three veteran soldiers who served together, now working for somebody the party would rather they were not. Every one of them will withdraw in good order the moment the fight stops being worth the wound, and they know each other well enough to go at the same time.
- **The favour** *(no fight)*. A watch sergeant is standing between the party and where they need to be, and has been ordered to. Ask what the order was. Somebody wrote it, and that somebody is reachable.

**Ecology.** A city's supply of the ordinary dangerous is roughly proportional to its supply of people who need something moved, guarded, or discouraged. They know each other. That is the fact worth remembering: the tough on the dock and the sergeant on the wall drink in the same three places, and a party that makes an enemy of one has made a mildly inconvenienced acquaintance of the other forty. Word travels at the speed of a shift change.

**Adaptation.** These need no adaptation; they are wherever people are. What varies is the institution behind them, and the entry improves the more specific you make it. "A watch sergeant" is a stat block. "A watch sergeant whose brother-in-law owns the warehouse" is an encounter.

---

## The Bought

*Five of them, in matched coats, and the coats are the tell — nobody outfits five people identically for cheap. They have taken up positions rather than walked into a room. One of them, at the back, is unhurriedly opening a leather case at their hip and taking out a folded document.*

The Bought are a mercenary company, and the joke the company makes about itself is that its most dangerous asset is the paperwork. It is not a joke. A Bought contract runs to several pages, specifies objectives and boundaries and permitted force with the precision of a shipping manifest, and is produced and read aloud at the start of engagements more often than weapons are drawn.

**This is not decoration. It is the entire creature.** A company that fights strictly to written terms is a company you can defeat by changing the terms, and the Bought know that better than anyone, which is why the contract case is chained to the belt and why the captain is the only person who has read the second clause.

They have existed in some form in every settled region for as long as anyone has been able to write down what they wanted done. The name changes. The case does not.

<!-- statblock: bought_blade -->

**Blade of the Bought** · *Mook* · **TR 4**

**When they act on it:** Resolve — · armor light (+1 Resolve) · defense +1

**When it acts:** attack +1 · incoming Tier 1

**Disposition:** Professional. Not cruel, not enthusiastic, and paying close attention to the terms.

**Goes for:** Whoever the contract names. Everyone else is an obstacle to be moved.

**In play:**

- Will not pursue past the boundary the contract specifies, and knows exactly where that is.
- Fights to the terms — a contract to detain produces no killing blows, and everyone on both sides can tell the difference.

**Morale:** Down two of four and the rest disengage in order. Nobody in the Bought has ever been paid enough to die for a clause.

**Appears:** Fours under a sergeant; four fours under a captain.

*`enemies/bought_blade.fof`*

<!-- /statblock -->

<!-- statblock: bought_sergeant -->

**Sergeant-at-Arms** · *Named* · **TR 9**

**When they act on it:** Resolve 3 · armor light (+1 Resolve) · defense +2

**When it acts:** attack +2 · incoming Tier 2

**Special:** HOLD THE TERMS — once per scene, the sergeant states the contract's boundary aloud. Every Blade in earshot immediately behaves as though the boundary is where the sergeant just said it is, whatever they believed a moment ago.

**Disposition:** Reads first, fights second, and would genuinely rather not.

**Goes for:** Whoever is closest to breaking the contract's boundary.

**In play:**

- Opens by naming the contract's terms aloud. This is not a bluff; it is how the company works.
- Spends Hold the Terms when the party splits, to keep the Blades from following anyone past the line.

**Morale:** Surrenders the field the moment the contract is void — payment withdrawn, terms broken by the employer, or the named target gone. Will say so out loud and expect to be believed.

**Negotiation:** Wants the contract satisfied or voided; either ends the fight. Shifts for proof the employer has broken terms. Honours any deal that lets the company withdraw with its fee and its reputation.

**Appears:** One per four Blades.

*`enemies/bought_sergeant.fof`*

<!-- /statblock -->

<!-- statblock: bought_captain -->

**Captain-under-Contract** · *Boss* · **TR 15**

**When they act on it:** Resolve 6 · armor heavy (+2 Resolve) · defense +2

**When it acts:** attack +3 · incoming Tier 2

**Special:** THE SECOND CLAUSE — every contract the Bought sign has one, and only the captain has read it. Once per fight the captain invokes it and the company's objective changes mid-scene, in a direction the party did not plan for.

**Special:** REFORM THE LINE — once per scene, every Blade that disengaged this scene returns to the field in good order.

**At Resolve 3:** The captain stops fighting and starts negotiating, out loud, mid-exchange. Attacks continue; so does the offer. Any party member who answers is talking to someone who is genuinely listening.

**Disposition:** Runs the fight the way a foreman runs a site: no heroics, no waste, and a very clear idea of when to stop.

**Goes for:** Nobody, at first. The captain spends the opening exchange placing Blades and watching who the party protects.

**In play:**

- Invokes the Second Clause the exchange after the party looks like winning.
- Reforms the line once, and only once, and only if the company still has somewhere to withdraw to.
- Never goes Aggressive. Ever. It is not that kind of company.

**Morale:** Calls the withdrawal at Resolve 2 and means it. A captain who has called a withdrawal will not resume the fight tonight for any inducement, including a better offer.

**Negotiation:** Wants the fee, the company intact, and the reputation that gets the next contract. Shifts for a better-paying, better-terms offer made in front of the sergeants. Honours a bought-out contract absolutely — it is the only asset the Bought actually sell.

**Appears:** One per company of sixteen Blades and four sergeants.

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

- **A four and a sergeant** *(1 Named + 4 Mooks — a soft Standard)*. The company's basic unit, doing a basic job. Ask what the job is.
- **Three sergeants holding a line** *(3 Named + 1 Mook — Standard)*. Different fours, same contract, and the Hold the Terms ability means the boundary is wherever the sergeants have agreed it is. The party can move the boundary by moving the sergeants' understanding of it.
- **The captain's engagement** *(1 Boss + 2 Named + 4 Mooks — Deadly, and written to be resolved rather than won)*. The Second Clause fires the exchange after the party looks like winning, and the phase change at Resolve 3 has the captain negotiating out loud, mid-fight, while attacks continue. A party that answers is talking to somebody who is genuinely listening.
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

**A Kindly One** · *Named* · **TR 8**

**When they act on it:** Resolve 4 · armor none · defense +3

**When it acts:** attack +0 · incoming Tier 2

**Special:** FAIR OFFER — a Kindly One cannot decline a genuinely fair trade, and knows fair from unfair without being told. No roll. The MM does not get to refuse on its behalf.

**Special:** THE UNFORGIVEN SLIGHT — a Kindly One cheated once never trades with that person again, nor does any other. There is no roll for this either, and no apology that works.

**Disposition:** Does not fight. Has never fought. Will absolutely stand there while you decide whether you are going to.

**Goes for:** None. If struck, a Kindly One defends itself by being extremely difficult to hit and by leaving.

**In play:**

- Opens every encounter with an offer, and the offer is always real.
- Never lies, never haggles twice, and never mentions the slight again — to you.

**Morale:** Leaves at the first Condition, and does not come back. Neither does any other Kindly One, anywhere, for the rest of the campaign.

**Negotiation:** Wants a fair trade, and defines fair generously. Shifts for anything genuinely valued by its owner rather than anything expensive. Honours every bargain to the letter, including the ones you would rather it read loosely.

**Appears:** Alone, at a crossing, a threshold, or a place where something was lost.

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
- **If the party attacks it** *(1 Named — nominally Standard, and a catastrophe by any measure that matters)*. It has a Threat Rating because a table that starts a fight needs one to finish. It leaves at the first Condition. Nothing in this book costs a campaign more.

**Ecology.** In regions where the Kindly are known, the local etiquette is intricate and universally observed, and outsiders find it baffling. People carry a token valuable specifically for crossings. Parents drill children on what to say. There is usually a rhyme. The rhyme is usually wrong about several details and right about the important one, which is *do not be clever at the bridge*.

**Adaptation.** They can be small folk, spirits, masked children, a very old animal — anything that can hold something out and wait. Keep the threshold, keep the two absolutes, and keep the fact that the fair trade is genuinely good for the party. A Kindly One who offers junk is a riddle. A Kindly One who offers something wonderful is a temptation, and temptation is what this entry is for.
