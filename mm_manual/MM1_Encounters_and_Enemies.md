# Mirror Master's Manual: Encounters and Enemies

A fight is a question with teeth. *Can they hold the bridge? Will the ogre take the toll or the traveler? Who breaks first?* Everything in this chapter is there to make that question sharper and the answer quicker to reach.

The work comes in five parts. **Reading a monster card**, so you can run anything in the Bestiary without studying it. **Choosing a level and a role**, which gives you every number a foe needs. **Deciding how many**, which decides whether your table has a good evening. **Running the exchange**: telegraphing, rolling in the open, morale and the Bloodied moment. And **converting**, for the night you want a creature from some other book.

There's less arithmetic here than you might expect. A foe has one dial, its level, and one choice, its role. Everything else on the card is behavior, because behavior is what your players will actually remember.

When you would rather not build anything, the **Bestiary** is a catalog of creatures that arrive finished, each already carrying the fields this chapter would otherwise have you write.

---

## The Monster Card

Every foe in these books, from a chicken to a city's last defender, is written on the same card. The numbers sit on two lines at the top. The rest is a handful of short fields that tell you what the thing does when the party is in front of it.

> **Reading the Entries — the monster card**
>
> **Name line:** the creature's name, then its **level** (1–10) and its **role** (Mook, Standard, Elite or Boss).
>
> **Numbers line:** **HP**, **armor** (0–2), **attack** (the bonus on its 2d6), **damage** (a flat number per hit), **attacks** per exchange, and **morale** (2–12). HP, attack, damage and attacks come from the level and role (Tables MM1–1 and MM1–2); armor and morale are chosen to fit the creature. A number flagged with **†** has been set by hand rather than read off the tables.
>
> **WANTS:** what it's doing when the party meets it, in one line. This is what you play when nobody has drawn a weapon yet.
>
> **SPECIAL:** the one thing that makes it more than a generic brute, stated so you can run it without asking anyone.
>
> **WHEN BLOODIED:** what changes when it drops to half its HP. For a Boss, this is its second phase.
>
> **TELLS:** what the party can see, hear or learn before the SPECIAL bites. Information before impact.
>
> **BREAKS:** what it does when its morale fails: flees, surrenders, bargains, or something stranger.
>
> **TWISTS (d6):** six one-line variations. Roll one, or pick one, and the same card gives you a different fight.
>
> **NASTIER:** optional. One extra line for a harder version, used when the party has outgrown the plain one.
>
> A missing NASTIER means the card offers no harder version; use a higher level instead. Every other field is always present.

The order is the order you need them in. WANTS matters when the party first sees it. TELLS matters while they're deciding what to do. SPECIAL and WHEN BLOODIED matter once the fight is running, and BREAKS matters at the end. TWISTS you use at the prep table, before any of that.

Here's a card built from scratch, so you can see every field doing its job. It's an example, not a creature from any setting.

```
TOLL OGRE                                   Level 3 Elite
HP 28   Armor 1   Attack +2   Damage 6   Attacks 2   Morale 8

WANTS          A toll from everyone who crosses its bridge, and it
               decides the price by looking at you.
SPECIAL        Grab and hurl: on a hard hit it can throw its target
               off the bridge instead of dealing damage.
WHEN BLOODIED  It drops the club, grabs the rail with both hands and
               shakes the whole span. Everyone on the bridge must
               avoid it with Body or go over the side.
TELLS          Coins nailed to the rail. Torn cloaks snagged on the rocks
               below. It licks its lips at anyone light enough to throw.
BREAKS         It jumps into the river and swims for its cave, cursing.
TWISTS (d6)    1 Two of them, and they argue about the toll.
               2 It has a toll collector: a frightened child it stole.
               3 The bridge is rotten; the ogre knows exactly which
                 planks are safe.
               4 It's lonely, and the toll is an hour of conversation.
               5 A rival is paying it to let nobody cross today.
               6 It is guarding the bridge for a family that
                 stopped paying it years ago.
NASTIER        It throws people at other people.
```

Read the card top to bottom and the whole fight is already there. WANTS says the party can pay and walk on. TELLS says what happens to people who don't. SPECIAL says what a hard hit looks like, and WHEN BLOODIED gives the fight a second act without a single new number. BREAKS says it won't fight to the death, and the TWISTS say there are at least six other ways this bridge could go.

---

## Level and Role

### The Level Table

A foe's level sets three numbers: how much HP it has, how hard it hits, and the bonus it adds to its attack roll. Read the row and you're done.

**Table MM1–1: Monster Levels**

| Level | HP | Damage | Attack |
|---|---|---|---|
| 1 | 8 | 4 | +1 |
| 2 | 11 | 5 | +1 |
| 3 | 14 | 6 | +2 |
| 4 | 17 | 7 | +2 |
| 5 | 20 | 8 | +2 |
| 6 | 23 | 9 | +3 |
| 7 | 26 | 10 | +3 |
| 8 | 29 | 11 | +3 |
| 9 | 32 | 12 | +4 |
| 10 | 35 | 13 | +4 |

Damage is a flat number, not a roll: a level 3 foe that hits deals 4, before the target's armor comes off. A hard hit adds 2 (see *Rolling in the Open*, MM1). Monster levels use the same 1–10 scale as the characters', which is the point: a level 5 foe is a fair match for one level 5 character.

### Roles

The role says how the foe fights and how much of the scene it owns. It changes the numbers from Table MM1–1 in fixed ways.

**Table MM1–2: Roles**

| Role | HP | Damage | Attack | Attacks | Also |
|---|---|---|---|---|---|
| Mook | drops to any hit (7+) | −1 | −1 | 1 | Attacks as one mob: +1 damage per extra Mook, up to +4 |
| Standard | as the level | +0 | +0 | 1 | — |
| Elite | ×2 | +0 | +0 | 2 | — |
| Boss | ×5 | +2 | +1 | 2 | Has a Bloodied phase |

**Mooks** are the crowd: thugs, rats, cultists in matching robes. They have no HP to track. Any attack that hits, a 7–9 as much as a 10+, drops one. They don't attack one by one. A group of Mooks makes a single attack roll as a mob, and each Mook beyond the first adds 1 to its damage, to a maximum of +4. Five Mooks at level 2 roll once at +0 and deal 2 + 4 = 6 on a hit. When three of them are down, the survivors deal 2 + 1 = 3. The mob gets weaker as it gets smaller, which is exactly how a crowd should feel.

**Standard** foes are the default: a sergeant, a wolf, a hired sword. One attack, the level's HP.

**Elites** are the foes a scene is built around: the ogre on the bridge, the captain of the guard. Double HP and two attacks per exchange, which means an Elite can threaten two characters at once or hit one of them twice.

**Bosses** are the reason the session happened. Five times the HP, two attacks, +2 damage and +1 to attack, and a WHEN BLOODIED line that changes the fight halfway through. A Boss with no second phase is just a large Standard foe, and your players will feel the difference.

### Armor and Overrides

Armor runs from 0 to 2 and comes off each hit the party lands, to a minimum of 1 damage. Hide and scale are 1, plate or stone is 2. Most foes are 0 or 1.

A card may override any number by hand, with a † on the card to show it. Use this sparingly: the bog creature whose HP is half again what its level says, the construct with armor 3 because that is the entire point of it. If you find yourself overriding three numbers, you've picked the wrong level.

### Choosing a Level

Start at the party's level. Go up a level or two for a foe that should feel dangerous, down a level or two for one that should feel like a warm-up. Stay inside a two-level band either side and the fight will behave the way Table MM1–4 predicts.

The rules put a hard edge on the far side. A foe three or more levels above an attacker makes that character's attacks Hard; six or more makes them Very Hard (see Chapter III.3). A level 1 party that walks into a level 5 anything isn't in a fight. It's in trouble, and the right move is to make that visible early (in the TELLS, in the ruin the thing left behind) so running away is a choice rather than a punchline.

> **Example — numbers from level and role**
>
> The Toll Ogre is level 3 and an Elite. Table MM1–1's level 3 row reads HP 14, damage 6, attack +2. Elite doubles the HP and gives two attacks. Its card reads HP 28, damage 6, attack +2, two attacks. Hide over muscle is armor 1. It's greedy, but it doesn't want to die for a bridge, so morale 8, just above the default. That's every number it will ever need, and none of it took longer than reading two rows.

---

## Morale

Nothing in these books fights to the death by default. Every foe has a **morale** number from 2 to 12. The default is 7; a foe that will never break is 12.

At certain moments you roll 2d6 for the foe. If the roll is **over** its morale, its nerve goes and it does whatever its BREAKS line says. If the roll is equal to its morale or under it, it fights on.

**The triggers.** Roll morale when:

- **the first of them falls**, dropped or fled;
- **half of them are down**;
- **their leader is down**;
- **one is left alone and hurt**, the last of its group or a lone foe at half HP or less.

Roll once per trigger, for the whole group. Mooks don't check one at a time; they break as a crowd. A character who forces a check with a talent (*Dread Presence*, Chapter II.4a) is making one of these moments happen early, and that's what the talent is for.

**Table MM1–3: Choosing Morale**

| Morale | It breaks on | How often | Who |
|---|---|---|---|
| 3 | 4 or more | Almost always | Conscripts, bullies, anything that was promised this would be easy |
| 5 | 6 or more | Usually | Hired muscle, hungry animals, looters |
| 7 | 8 or more | Often (the default) | Soldiers, ordinary beasts, most people |
| 9 | 10 or more | Sometimes | Veterans, anything defending its young or its home |
| 11 | 12 only | Rarely | Zealots, the cornered, the truly desperate |
| 12 | never | Never | Constructs, the mindless, the bound |

A broken foe is out of the fight but not out of the story. BREAKS says how. The ogre swims for home and remembers faces. The hired sword drops her blade and asks what the party pays. The pack scatters into the trees, and the party will hear them again tonight. Play it the way the card says, and then let the players decide what to do with a beaten enemy, because that's one of the more interesting choices the game offers.

> **Through the Mirror — why morale does so much work**
>
> We count morale as the single largest lever on how long a fight lasts. Without it, every fight runs to the last HP, which is slow, samey, and teaches the party that every enemy is a sack of numbers to be emptied. With it, most fights end somewhere around their middle, and the end is a story beat (a surrender, a rout, a parley) instead of bookkeeping. If you house-rule it away, expect fights to run half again as long and feel less alive.

---

## Meeting Someone: The Reaction Roll

Most encounters don't begin as fights. When the party meets a creature or person whose attitude the fiction hasn't already settled, roll 2d6 before anyone says a word. Low is hostile. The middle is wary or uncertain, and high is open or friendly. The full table, with a d66 list of what they want right now, is in MM6.

Because 2d6 bunches in the middle, the result you'll see most often is *uncertain*: they'll talk, but they want something first. That's deliberate. It puts the next move in the players' hands and turns a random meeting into a conversation instead of a brawl. Roll it for the ogre on the bridge, the patrol on the road and the thing in the cellar, and your campaign will have far fewer fights nobody wanted.

Don't roll when the fiction has already answered. The assassin sent after the party is hostile; the grandmother who raised one of them is friendly. The roll is for when you honestly don't know.

---

## Building a Fight

### Count the Threats

Whether a fight is easy or deadly depends mostly on how many real threats are in it compared with how many characters are facing them. Levels matter at the edges; headcount matters everywhere. So count.

**Table MM1–4: Reading a Fight**

| Foe | Counts as |
|---|---|
| Every four Mooks (round up) | 1 threat |
| A Standard foe | 1 threat |
| An Elite | 2 threats |
| A Boss | 4 threats |
| Any foe 3+ levels above the party | double its count |
| Any foe 3+ levels below the party | half its count |

Add them up and hold the total against the number of characters:

- **Fewer threats than two-thirds of the party** is a **skirmish**. The party wins. It costs a little HP and establishes that the danger is real.
- **Up to one threat per character** is a **real fight**. Someone gets hurt, Sparks get spent, and it takes two to four exchanges.
- **Up to one and a half per character** is **hard**. Someone may drop to 0 HP. Morale and terrain will decide it as much as the dice do.
- **More than that** is **deadly**. It exists to be avoided, bargained with, or fought only after the party has found an edge.

Three level 1 characters against the Toll Ogre face 2 threats: a real fight. Put a Boss in front of the same three and it's 4 threats against 3, which is hard, and that is correct: a level 1 Boss should frighten a level 1 party.

> **Through the Mirror — these bands are a starting read**
>
> The bands in Table MM1–4 follow from the roles themselves: an Elite has twice a Standard foe's HP and attacks, a Boss has five times the HP. The shape we're aiming for is four Mooks being trivial, a mixed fight of Standard foes lasting two to four exchanges, and a lone Boss at the party's level being dangerous at every level from 1 to 10. The app's encounter read uses the same counts. What no count can tell you is how clever your players are, so treat the band as a forecast and your own table as the weather.

### Dials Other Than Headcount

**Morale** turns a hard fight into a real one: a crowd with morale 5 will scatter after the first two fall. Raise it for the fight that's supposed to be grim; lower it for one that should end in a chase.

**Terrain** gives both sides something to do besides trade blows. A bridge, a burning barn, a rope over a pit, a hallway only one foe wide. Terrain is where the players' stunts come from (on a 10+ they can trip, disarm, push or pin instead of dealing more damage), so give them things worth pushing someone into.

**Arrivals** are the sharpest dial you own. One more Mook at the door, a second wolf on the ridge. Add them when a fight is going too easily; hold them back when it's going badly. Nobody at the table knows how many were supposed to come.

**A way out** is a dial too. Every real fight or harder should have at least one route to winning that isn't emptying the foe's HP: a leader who can be talked to, a weakness the TELLS point at, a door that can be barred. That isn't a consolation prize.

> **MM Note — a lateral solution is the encounter working**
>
> When a player finds a way around most of the fight (the ogre is paid off, the bridge is cut, the Boss is locked in its own vault), they haven't broken your encounter. That is the encounter doing its job. The default is to let it work. The dial is how much it costs: a Spark, a 7–9, something left behind. The guardrail is that the clever route should never be cheaper than it looks from the outside.

---

## Running the Exchange

Combat runs in **exchanges**, and each exchange goes the same way (see Chapter III.3). You telegraph, the players act, the foes attack in the open, you narrate, and anything that lasts an exchange ends. What follows is the MM's half of that.

### Telegraph Intent

Start every exchange by saying what each foe is about to do, and to whom. *"The ogre winds up to swing at Mordai. The two thugs are edging round behind Zahna."* This is the most important thing you'll say all fight. It turns combat from a slugging match into a set of problems. Mordai can step in, Zahna can move, Zulnut can do something unwise with the rope. The players make their choices knowing what's coming, which is the only way their choices mean anything.

Telegraphing isn't a promise. If the party does something that changes the situation (the thugs' target leaves, the ogre is pinned), the foes adapt. But what you said is what they were going to do, and if nobody stops it, it happens.

The TELLS line is the long-range version of the same thing. A telegraph is what happens in the next few seconds; a tell is what the party could have noticed before the fight started. Use both.

### Players Act, In Any Order

There is no turn order. After you've telegraphed, ask the table what they do, take the answers in whatever order they come, and have them roll. Everyone acts every exchange. If two players both want to go first, let the one who spoke first go first and move on. It matters much less than it feels like it does.

### Rolling in the Open

Foes roll their own attacks: 2d6 plus their attack bonus, in front of everyone. The app rolls it for you and shows it to the table. Say who's being attacked, roll, and read the result:

- **10+:** a hard hit, damage +2.
- **7–9:** a hit, the card's damage.
- **6−:** a miss.

A natural 12 is a hard hit and something more, which you name: the target is thrown, disarmed, knocked through a door. A natural 2 is a miss that gives the target an opening, and that character's next attack on this foe is Easy. Armor comes off every hit, to a minimum of 1.

Three things change the roll. A character who took a 7–9 on their own attack this exchange is **exposed**: a foe that can reach them rolls an extra die on its next attack at them this exchange and keeps the best two. A character who **defends** makes attacks on them Hard (−1). A character who **intercepts** defends and takes the attacks aimed at an ally within reach.

Rolling in the open does something your players will feel before they can name it. When the ogre's dice come up 11 in front of the whole table, the damage isn't your choice, and nobody at the table thinks it is. You stop being the person hurting their characters and become the person narrating what the dice did.

> **Through the Mirror — why the foes roll**
>
> Earlier versions of this game kept every die in the players' hands, and foes never rolled. We changed it because the players we watched wanted to see the danger arrive. A roll everyone can see is a moment everyone shares: the table groans at the 11 and cheers at the 2. The players still roll far more often than you do, since every one of them acts every exchange. Outside combat, NPCs still never roll against the characters. The players roll, and the NPC sets the difficulty.

### When a Player Rolls 6−

On a missed attack, the foe gets a move. Look at the fiction first, then the card, then the Fight Complications table in MM6 if nothing comes. The foe might push its advantage, grab the thing it wants, pull back into cover or hurt someone. Whatever you choose, it should change the situation, not merely subtract HP. A miss that only means "nothing happens" is a wasted roll.

### Bloodied

When a foe drops to half its HP or lower, it's **Bloodied**, and its WHEN BLOODIED line happens at once, in the middle of whatever was going on. For a Boss this is its second phase: new behavior, new threat, sometimes a new goal. Say it out loud as it happens. The table should feel the fight change.

Build a Boss's second phase so the party can meet it early. If the Bloodied line only protects something the party would never otherwise see (a hostage, a collapsing roof, a secret the Boss shouts), put that thing into the fight from the start. A party that burns a Boss down in two exchanges should get the whole story, not skip half of it.

### Ending the Fight

A fight is over when its question is answered, not when the last HP is gone. If the foes are broken and the party is standing, say so and move on. *"The last two drop their clubs and run."* Nobody needs to roll their way through a result the whole table can already see.

> **Example — one exchange on the bridge**
>
> The party has refused the toll. The ogre is at full HP, 28.
>
> MM: "The ogre swings at Mordai with the club. And it's looking at Zahna like he's the right size to throw. What do you do?"
>
> **Mordai** attacks. The MM agrees his knack, *Soldiering*, applies: 2d6 + Body (+2) + knack (+1). He rolls 4 and 5, plus 3, for 12: a full success. His longsword deals 1d8, showing 5, and he picks +1d6 damage from the three options, rolling 3, for 8. Armor 1 comes off, so 7. The ogre is on 21.
>
> **Zulnut** goes for the ogre's ankle to trip it: 2d6 + Body (+2), rolling 1 and 3, plus 2, for 6. A miss.
>
> MM: "It's like trying to trip a tree. The ogre doesn't even look down. It just puts a foot on your chest, and you're pinned flat on the planks."
>
> (The MM took that from the fiction, not a table. Zulnut is now on his back under an ogre, which is a much better problem than "you miss.")
>
> **Zahna** backs away, casting nothing yet.
>
> The ogre attacks twice. At Mordai: 2d6 + 2, showing 6 and 3, for 11: a hard hit, 4 + 2 = 6 damage. Mordai's heavy armor and shield stop 3, so he takes 3. At Zahna, and the ogre wants to throw him: 2d6 + 2, showing 2 and 3, for 7: a hit. That's no hard hit, so no throw. It deals 4, and Zahna's light armor stops 1. Zahna takes 3 and is on 3 of his 6 HP.
>
> MM: "It grabs for you and gets a fistful of your coat instead of you. You're bruised, and you're very aware of the river."
>
> (Two rolls, both public, one of them close. Nobody at the table blames the MM for either.)

---

## Converting Creatures from Other Games

Sooner or later you'll want a creature from another game's book. You can have it, but bring the idea across, not the text or the numbers. Our cards are written in our own words, and a stat block copied from someone else's book is both a copyright problem and a bad fit.

Read the original for four things and translate each one:

1. **How tough is it, where it comes from?** Something that game treats as a fair fight for a starting party is level 1 or 2 here. Something it treats as a campaign's final enemy is level 9 or 10. Put everything else between by feel.
2. **How does it fight alongside others?** Things that come in swarms and die in one blow are Mooks. Ordinary foes are Standard. The creature a scene is built around is an Elite. The creature an adventure is built around is a Boss.
3. **How well protected is it?** Nothing special is armor 0, a thick hide or mail is 1, plate or stone is 2.
4. **How brave is it?** Pick a morale from Table MM1–3.

That's the numbers. Then write the card fields yourself, and that's where the creature really lives. What does it want? What's the one thing it does that nothing else does? How would the party know? What does it do when it loses its nerve? Six twists. If the original has a dozen special abilities, pick the one that makes the best scene and let the rest go. A creature with one SPECIAL that the table remembers beats a creature with six that you forget to use.

---

## Building Your Own in Five Minutes

When you need a foe and don't have one, work through these in order.

**1. The question.** What is this fight about? *Can they get past it? Will they save the prisoner? Who gets the map?* If you can't say, the scene may not need a fight.

**2. Level and role.** Start at the party's level. Pick the role from the scene's shape: a crowd, a foe, a centerpiece or a finale. Read the numbers off Tables MM1–1 and MM1–2.

**3. WANTS and SPECIAL.** One line each. The want should be something the party could give it, deny it or trick it out of. The special should be something you can describe in a sentence and run without looking anything up.

**4. TELLS and BREAKS.** How the party could learn about the special before it lands, and what it does when its nerve goes.

**5. Twists.** Six, if you have time. One, if you don't. The first twist you think of is usually the best one.

Then count the threats (Table MM1–4) and add a way out.

> **MM Note — when in doubt, the easier fight**
>
> If you're torn between two sizes of fight, pick the smaller one. A party that feels competent takes risks, tries stunts and does something interesting. A party that feels outmatched hunkers down and plays safe, and safe is dull. You can always add an arrival at the door. Taking one away is much harder to do gracefully.

### The Three-Fight Session

Most sessions that have fights have one to three of them. When there are three, give them a shape:

1. **Opening:** a skirmish. Establish the threat and let the players feel good at this.
2. **Middle:** a real fight. The stakes rise, HP runs down, Sparks come out.
3. **Climax:** hard, with a way out. The payoff.

Never hard, hard, hard: by the third one the party is spent and the fight feels unfair rather than dramatic. And never open with the deadly one. Players need to feel competent before you test them.
