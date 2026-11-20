"""Generates the TRAPWORKS (TW) and STARFALL ARMADA (SFA) card sets: 300 cards each,
with full card info and a professional art prompt per card.  Re-run safely: seeded."""
import random, json, csv, os, re
OUT = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUT, exist_ok=True)

RARITY_PLAN = {'L': 30, 'R': 60, 'U': 90, 'C': 120}

def stats_for(r, cost, nab, lean):
    budget = cost * 2 + 1 - max(0, nab - 1) + (1 if r in 'RL' else 0)
    budget = max(2, budget)
    a = max(1, round(budget * lean + r_.uniform(-1, 1)))
    a = min(a, budget - 1)
    return a, max(1, budget - a)

def nval(cost, k, cap=9):
    return max(1, min(cap, round(cost * k)))

def fill(t, cost):
    """t = (kw, body, reminder, k) ; replaces {n}"""
    kw, body, rem, k = t
    n = nval(cost, k, 3 if 'draw' in body.lower() or 'card' in body.lower() else 9)
    f = lambda s: s.replace('{n}', str(n)).replace('{s}', '' if n == 1 else 's')
    return {'kw': f(kw), 'body': f(body), 'rem': f(rem)}

def uniq(gen, used, tries=400):
    for _ in range(tries):
        v = gen()
        if v not in used:
            used.add(v); return v
    raise RuntimeError('ran out of names')

def assign_rarities(cards, fixed_r):
    """cards: list with optional preset 'r'. Fill to RARITY_PLAN."""
    left = dict(RARITY_PLAN)
    for c in cards:
        if c.get('r'): left[c['r']] -= 1
    pool = [k for k, v in left.items() for _ in range(v)]
    r_.shuffle(pool)
    for c in cards:
        if not c.get('r'): c['r'] = pool.pop()

# =====================================================================
#                              TRAPWORKS
# =====================================================================
r_ = random.Random(2026)
TW_STYLE = ('dark cinematic horror concept art for a premium trading card game, dramatic chiaroscuro lighting, '
            'volumetric fog, grime and rust textures, painterly digital painting, ultra detailed, '
            '4:3 landscape composition, no text, no letters, no watermark, no gore')
TW_WINGS = {
 'Crimson': ('aggression and Bleed', 'inside a derelict slaughterhouse factory lit by red emergency lights'),
 'Brass':   ('Devices and Countdowns', 'inside a clocktower machine room full of giant brass gears and candlelight'),
 'Drowned': ('Rooms and control', 'in flooded tiled sewer cells with cold green shafts of light'),
 'Ash':     ('Minion swarms', 'in abandoned asylum corridors under flickering fluorescent lights'),
 'Lantern': ('Survivors and Escape', 'in hidden servant passages lit by a single warm lantern'),
}
TW_TYPE_WING = {  # weights per wing for each type
 'Minion':   {'Crimson': 3, 'Brass': 1, 'Drowned': 1, 'Ash': 5, 'Lantern': 0},
 'Survivor': {'Crimson': 1, 'Brass': 1, 'Drowned': 1, 'Ash': 0, 'Lantern': 6},
 'Trap':     {'Crimson': 3, 'Brass': 3, 'Drowned': 2, 'Ash': 1, 'Lantern': 0},
 'Device':   {'Crimson': 1, 'Brass': 6, 'Drowned': 1, 'Ash': 1, 'Lantern': 1},
 'Room':     {'Crimson': 1, 'Brass': 1, 'Drowned': 5, 'Ash': 2, 'Lantern': 1},
 'Trial':    {'Crimson': 2, 'Brass': 1, 'Drowned': 1, 'Ash': 1, 'Lantern': 1},
 'Event':    {'Crimson': 1, 'Brass': 1, 'Drowned': 1, 'Ash': 1, 'Lantern': 2},
}
def pick_wing(t):
    w = TW_TYPE_WING[t]; return r_.choices(list(w), weights=list(w.values()))[0]

FIRST = 'Ada Silas Marlowe June Ezra Clara Dorian Hollis Mabel Rook Tess Abel Vera Calvin Nell Otto Ivy Jasper Lena Morgan Pike Rosa Felix Greta Hugo Iris Jonah Kit Lucan Maeve Noah Opal Quinn Ruth Saul Thea Uriah Willa Zeke Della Amos Cora Desmond Elsie Gideon Hattie Ira Josie Leland Minnie'.split()
LAST = 'Crane Vance Ashby Morrow Blackwood Harrow Sallow Quill Thorne Grimsby Ledger Fenwick Marsh Stroud Calloway Pruitt Wexley Doyle Kessler Abernathy Birch Cobb Dunmore Ellery Frost Gale Hale Ingram Jessup Kane Lyle Mercer Nash Oakes Penrose Redd Sutter Tate Underhill Voss'.split()
ROLES = ['Locksmith','Night Nurse','Electrician','Firefighter','Detective','Mechanic','Schoolteacher','Chemist','Paramedic',
         'Plumber','Night Guard','Surgeon','Journalist','Rock Climber','Coal Miner','Cave Diver','Priest','Runaway','Engineer',
         'Field Medic','Courier','Carpenter','Veterinarian','Radio Operator','Boxer','Welder','Librarian','Ex-Cop','HVAC Technician',
         'Stage Magician','Cryptographer','Lineman','Pharmacist','Trucker','Sous Chef']
POSES = ['crouching behind cover with a flashlight', 'prying open a rusted hatch', 'bandaging a wounded arm, looking over a shoulder',
         'running down a corridor, breath fogging', 'studying a cryptic clue scratched on a wall', 'gripping a crowbar, ready to fight',
         'climbing through a ventilation duct', 'holding a lantern up to the darkness', 'working a lock with picks by candlelight',
         'wading through dark water, holding a key aloft']
SURV_EPI = ['the Unbroken','Who Walked Out','Last of the Night Shift','the Lockbreaker','the Quiet Survivor','Who Remembers Every Door',
            'the Iron Will','Who Never Ran','the Final Witness','Keeper of the Lantern','the One Who Stayed','Mender of the Lost',
            'the Escape Artist','Breaker of Clocks','the Unforgotten']
MASTERMINDS = [
 ('The Puppeteer of Hollow Mill','a gaunt figure in a ragged tailcoat working puppet strings that lead into the dark'),
 ('Mother Hush','a towering veiled matron holding a finger to stitched lips'),
 ('The Clockmaker','a hunched tinkerer with brass goggles and dozens of ticking pocket watches on chains'),
 ('The Surgeon in White','a spotless figure in a white coat and porcelain mask under a surgical lamp'),
 ('Sister Tallow','a nun-like figure of melted candle wax with a crown of lit candles'),
 ('The Ferryman Below','a cloaked boatman poling a skiff through a flooded tunnel, lantern on the prow'),
 ('The Choirmaster','a conductor with a raised baton before rows of silent masked figures'),
 ('The Gamesmaster','a figure in a pinstripe suit and grinning mask shuffling oversized cards'),
 ('Dr. Lisle Ambrose','an elegant doctor in an old-fashioned plague mask beside glass specimen jars'),
 ('The Hourglass King','a robed monarch whose crown is a cracked hourglass spilling red sand'),
 ('The Lamplighter','a tall figure in a stovepipe hat carrying a long brass lamplighter pole'),
 ('The Tinker','a scrawny figure in a leather apron covered in tools and tiny mechanical spiders'),
 ('The Auditor','a bureaucrat in a grey suit with a ledger and a face hidden by a blank paper mask'),
 ('The Quiet Man','a silhouette in a long coat and hat, face lost in shadow, standing perfectly still'),
]
MIN_ADJ = ['Rust-Masked','Porcelain','Hooded','Stitched','Grinning','Silent','Wax-Faced','Chain-Bound','Ragged','Pale','Lantern-Eyed',
           'Cracked','Faceless','Burlap','Tallow','Iron-Jawed','Whispering','Limping','Night-Shift','Hollow Mill','Gasmask','Bell-Collared']
MIN_NOUN = ['Orderly','Butcher','Stitcher','Doll','Hound','Porter','Janitor','Watchman','Pig-Mask','Mourner','Collector','Tallyman',
            'Rat Swarm','Crow Keeper','Scarecrow','Mannequin','Gravedigger','Lamb-Mask','Gasman','Chainman','Stalker','Bellringer','Weeper','Warden-Hound']
TRAP_A = ['Pendulum','Razorwire','Collapsing','Gas-Filled','Spring-Loaded','Barbed','Dropping','Sealed','Bear-Jaw','Tripwire','Mirrored',
          'Shock','Glass','Spiked','Flooding','Crushing','Snapping','Rigged']
TRAP_N = ['Floor','Corridor','Door','Stairwell','Ceiling','Vent','Lift','Snare','Cage','Net','Trapdoor','Lockbox','Chair','Bridge','Hallway','Locker']
DEV_A = ['Clockwork','Brass','Iron','Copper','Rusted','Ticking','Glass','Bone-Handled','Wired','Gilded','Grinding','Humming']
DEV_N = ['Collar','Hourglass','Metronome','Music Box','Mask','Gauntlet','Key','Gramophone','Lantern','Manacles','Harness','Bellows',
         'Valve','Compass','Puppet Strings','Timer','Spool','Crank','Detonator','Pocket Watch']
ROOM_A = ['Flooding','Mirrored','Freezing','Shrinking','Silent','Spinning','Upside-Down','Ticking','Velvet','Glass','Echoing','Furnace',
          'Sinking','Starving','Endless','Dark']
ROOM_N = ['Cell','Ballroom','Chapel','Library','Kitchen','Boiler Room','Morgue','Theater','Greenhouse','Archive','Bathhouse','Elevator',
          'Laundry','Waiting Room','Observatory','Cold Storage','Clock Room','Parlor','Pump Station','Records Office']
TRIALS = ['Countdown','Last Breath','Cut the Wire','Red or Green','Trust Fall','Lights Out','The Key Inside','Play or Pay','One Must Stay',
          'The Tape Plays','Running Out','The Bell Tolls','The Coin Toss','The Final Door','The Confession','Hold Your Breath','Weigh Your Heart',
          'The Scales','Pick a Card','Blind Man\'s Bluff','Sand Through Fingers','Ring the Bell','The Long Count','Ante Up','Two Keys, One Lock']
EVENTS = ['Barricade the Door','Second Wind','Found a Map','Patch Them Up','Run!','Hide in the Lockers','Smash the Camera','Lights Back On',
          'Strength in Numbers','Desperate Swing','Read the Riddle','The Floor Gives Way','Slam the Hatch','Make a Torch','Follow the Draft',
          'Scream for Help','Bad Wiring','Steady Hands','Shared Rations','Out of the Dark','False Exit','A Familiar Voice','Kick It Down',
          'Rally the Others','Burn the Ledger','Silence the Bell','Sprung Early','Night Terrors','Cold Sweat','One More Door']
TRIAL_SCENES = ['two glowing doors and a ticking timer above them','a tape recorder on a metal table under a bare bulb',
                'an antique scale holding a key on one side','a red phone ringing in an empty room','a countdown clock wired to a heavy door',
                'a single chair facing a wall of television screens','a hand of oversized playing cards on green felt',
                'an hourglass draining beside a padlocked box','a church bell hanging over a pit','a coin spinning on a rusted table']
EVENT_SCENES = ['survivors pushing a heavy cabinet against a shaking door','a hand striking a match in total darkness',
                'a torn map with a route marked in blood-red ink','a flashlight beam revealing scratch marks','an open hatch with fresh air pouring in',
                'two survivors back to back holding improvised weapons','a sparking fuse box in a corridor','a smashed security camera dangling from wires']

TW_UNIT_ABIL = [
 ('Guard.','','(Enemies must attack units with Guard first.)',0),
 ('Last Count.','When this is defeated, your opponent loses {n} life.','',0.4),
 ('Stalk.','','(Can only be blocked by units with Guard or Stalk.)',0),
 ('Bleed {n}.','','(Units this damages lose {n} more HP at end of turn.)',0.3),
 ('Panic.','When this enters, your opponent discards a random card.','',0),
 ('Disarm.','When this enters, destroy an enemy Trap or Device.','',0),
 ('Barricade.','Tap: Your other units get +0/+{n} until end of turn.','',0.4),
 ('Swarm.','Gets +1 ATK for each other Minion you control.','',0),
 ('Ambush.','You may play this on your opponent\'s turn.','',0),
 ('Sacrifice.','Destroy another unit you control: Deal {n} damage to any target.','',0.6),
 ('Watchful.','Whenever your opponent sets a Trap, draw a card.','',0),
 ('Fearless.','','(Trials can\'t make you sacrifice this.)',0),
 ('Night Shift.','At the end of your turn, if you played no cards, create a 1/1 Orderly token.','',0),
 ('Tough {n}.','','(Reduce the first damage this takes each turn by {n}.)',0.3),
 ('Quick.','','(Can attack the turn it enters.)',0),
 ('Scavenge.','When this enters, return a Device from your discard pile to your hand.','',0),
 ('Lantern.','You may look at face-down Traps at any time.','',0),
 ('Hunt.','When this defeats a Survivor, draw {n} card{s}.','',0.3),
]
TW_SURV_ABIL = [
 ('Escape —','Draw {n} card{s}.','(Escape triggers when this survives a Trial.)',0.35),
 ('Escape —','Restore {n} HP to each of your units.','(Escape triggers when this survives a Trial.)',0.5),
 ('First Aid.','Tap: Restore {n} HP to a unit.','',0.6),
 ('Lockpick.','Tap: Disarm a face-down Trap that costs {n} or less.','',0.6),
 ('Teamwork.','Your other Survivors get +1 ATK.','',0),
 ('Resourceful.','When this enters, draw a card.','',0),
 ('Distraction.','Tap: An enemy unit can\'t attack this turn.','',0),
 ('Brave.','Gets +2 ATK while you have less life than your opponent.','',0),
 ('Rescue.','When this enters, return a Survivor from your discard pile to your hand.','',0),
 ('Tinkerer.','Your Devices cost 1 less.','',0),
]
TW_TRIG = ['an enemy unit attacks','an enemy unit enters play','your opponent plays an Event','an enemy unit is healed',
           'your opponent\'s turn begins','an enemy Survivor uses a Tap ability']
TW_TRAP_FX = [('deal {n} damage to that unit','',0.7),('that unit can\'t attack or block next turn','',0),
              ('return that unit to its owner\'s hand','',0),('destroy that unit if it has {n} or less HP','',0.6),
              ('your opponent discards two cards','',0),('create two 1/1 Orderly tokens','',0),
              ('your opponent loses {n} life and you draw a card','',0.4),('put a Clockwork Collar on that unit','',0)]
TW_DEV = [
 ('Countdown.','Attach to an enemy unit. At the end of each turn, it takes {n} damage.','',0.3),
 ('Armed.','Attach to a unit you control. It gets +{n} ATK.','',0.6),
 ('Reinforced.','Attach to a unit you control. It gets +0/+{n} and Guard.','',0.7),
 ('Shackled.','Attach to an enemy unit. It can\'t block.','',0),
 ('Wired.','Tap: Deal 1 damage to any target.','',0),
 ('Engineered.','Your Traps cost 1 less.','',0),
 ('Deadman Switch.','Attach to an enemy unit. When it is defeated, its controller loses {n} life.','',0.6),
 ('Wind-Up.','At the start of your turn, add a Tick counter. Remove 3 Tick counters: Draw {n} card{s}.','',0.5),
 ('Muzzle.','Attach to an enemy unit. It loses all abilities.','',0),
 ('Rewind.','Destroy this: Return a unit to its owner\'s hand.','',0),
]
TW_ROOM = [
 ('Room.','At the start of each turn, each unit takes 1 damage.','',0),
 ('Room.','Units with {n} or less HP can\'t attack.','',0.5),
 ('Room.','Survivors get +0/+{n}.','',0.4),
 ('Room.','Minions get +1 ATK.','',0),
 ('Room.','Whenever a unit is defeated, its controller draws a card.','',0),
 ('Room.','Players can\'t gain life.','',0),
 ('Room.','Traps cost 1 less for each player.','',0),
 ('Room.','At the end of your turn, if you control three or more Minions, your opponent loses {n} life.','',0.5),
 ('Room.','Each player can attack with at most two units each turn.','',0),
 ('Room.','Whenever a Trap springs, its owner draws a card.','',0),
]
TW_TRIAL = [
 ('Trial.','Your opponent chooses one: they sacrifice a unit, or they lose {n} life.','',0.9),
 ('Trial.','Your opponent chooses one: they discard two cards, or you draw {n} cards.','',0.5),
 ('Trial.','Your opponent chooses one: their units can\'t attack next turn, or you gain {n} life.','',1),
 ('Trial.','Your opponent chooses one: they destroy one of their Devices or Rooms, or you deal {n} damage to a unit.','',1),
 ('Trial.','Your opponent chooses one: they sacrifice their strongest unit, or you create {n} 1/1 Orderly tokens.','',0.6),
]
TW_EVENT = [
 ('Strike.','Deal {n} damage to a unit.','',0.9),('Heal.','Restore {n} HP to each Survivor you control.','',0.7),
 ('Search.','Draw {n} cards.','',0.5),('Shove.','Return a unit to its owner\'s hand.','',0),
 ('Sabotage.','Destroy a Trap or Device. Draw a card.','',0),('Rally.','Your units get +{n} ATK until end of turn.','',0.4),
 ('Scout.','Look at the top {n} cards of your deck. Put one in your hand.','',0.8),
 ('Hold Out.','Your units can\'t be defeated this turn. Each takes 1 damage at end of turn.','',0),
]
TW_FLAVOR = ['Every room is a question. Every answer costs blood.','It never speaks. It only counts.','There is no lock she has not met before.',
 'Tick. Tick. Tick.','The drain was never meant to drain.','"Door one, or door two? The tape is already running."',
 'The exits are painted on.','Somewhere above, a gramophone skips on the same note.','Hollow Mill closed in 1961. Someone kept the lights on.',
 'The clocks all agree. That is the worst part.','Count the doors. Then count them again.','He smiled. The mask did not.',
 'She learned the floor plan by the screams.','The water rises one tile at a time.','Not every key opens a door. Some open you.',
 'Rule one: don\'t run. Rule two: run.','The bell rings once for each of you.','The ledger keeps score. The ledger is never wrong.',
 '"We were six when we woke up."','Rust remembers everything.','Hope is the cruelest trap of all.','The lantern was the only honest thing down there.',
 'It wore the night nurse\'s badge. It was not the night nurse.','A survivor is just a prisoner who hasn\'t stopped.',
 'Three turns of the crank. Always three.','He fixed boilers for twenty years. This one fought back.','The music box plays slower every night.',
 'Behind every wall, another wall.','The Warden built rooms the way spiders build webs.','Listen. The pipes are counting too.',
 '"The tape said trust no one. So I trusted the tape."','You can smell the next room before you see it.','The floor is a lie told in tile.',
 'Nobody wins the game. Some people finish it.','Its footsteps were always one door behind.','The chalk marks led in circles.',
 'Somebody wrote HELP on the ceiling.','The whisper came from the vent, and it knew her name.','Lights on. Lights off. Lights on.',
 '"Keep the lantern lit and keep moving."','The gears never stop. Neither should you.','Freedom is a door that opens outward.',
 'The masks are all the same face.','Hollow Mill pays its workers in silence.','The puppet strings went up into the dark forever.',
 'There was a map. The map was the trap.','Courage is just fear with a crowbar.','One of them is lying. The tape knows which.',
 'The hourglass ran red.','You hear the tally marks being scratched.','The Mill eats the brave first.','Breathe slow. The air is rationed.',
 'He welded the door shut from the inside.','"I fix things," he said, and reached for the wires.','The last room has no door at all.',
 'Every survivor leaves something behind.','Downstairs is always worse.','The gramophone started playing on its own.',
 'Iron, rust and the memory of hands.','The Lower Floors don\'t appear on any blueprint.']

def tw_cards():
    cards, used = [], set()
    def add(**c):
        c.setdefault('set', 'TW'); cards.append(c); used.add(c['name']); return c
    # ---- hand-made showcase cards (from the concept boards) ----
    add(name='The Warden, Architect of Rooms', cost=6, type='Mastermind', sub='Human Overseer', wing='Crimson', r='L', foil=True,
        ab=[{'kw':'Trial.','body':'At the start of your turn, hold a Trial.','rem':'(Your opponent chooses: sacrifice a Survivor, or lose 3 life.)'},
            {'kw':'Architect.','body':'Your Rooms cost 1 less. Whenever a Room enters, draw a card.','rem':''}],
        flavor='Every room is a question. Every answer costs blood.', atk=3, hp=7, svg='tw-warden',
        prompt='a towering masked overseer in a long dark coat and pale cracked porcelain mask holding a brass key ring, standing on a catwalk under a single hanging bulb, rows of glowing red doors behind him')
    add(name='Hollow Mill Orderly', cost=2, type='Minion', sub='Masked Henchman', wing='Ash', r='C',
        ab=[{'kw':'Guard.','body':'','rem':'(Enemies must attack units with Guard first.)'},{'kw':'Last Count.','body':'When this is defeated, your opponent loses 1 life.','rem':''}],
        flavor='It never speaks. It only counts.', atk=2, hp=2, svg='tw-orderly',
        prompt='a hulking orderly in a stained uniform and riveted porcelain mask raising a lantern in a dim corridor')
    add(name='Wren Holloway, Locksmith', cost=3, type='Survivor', sub='Human Locksmith', wing='Lantern', r='R',
        ab=[{'kw':'Escape —','body':'Disarm a Trap of your choice.','rem':'(Escape triggers when this survives a Trial.)'},{'kw':'Pick the Lock.','body':'Tap: Look at one face-down Trap your opponent controls.','rem':''}],
        flavor='There is no lock she has not met before.', atk=1, hp=3, svg='tw-wren',
        prompt='a young woman locksmith kneeling at a massive wooden door covered in a dozen padlocks, working lock picks by lantern light, warm rim light')
    add(name='Clockwork Collar', cost=3, type='Trap', sub='Device', wing='Brass', r='U',
        ab=[{'kw':'Attach.','body':'Put this on an enemy unit.','rem':'(It stays until removed.)'},{'kw':'Countdown.','body':'At the end of each turn, the wearer takes 1 damage. If it attacked this turn, it takes 2 instead.','rem':''}],
        flavor='Tick. Tick. Tick.', badge='DEVICE', svg='tw-collar',
        prompt='an ornate spiked steel collar with a brass clock face and exposed gears resting on a dark workbench, macro still life')
    add(name='Room 13: The Flooding Cell', cost=4, type='Room', sub='Location', wing='Drowned', r='R',
        ab=[{'kw':'Rising Water.','body':'At the start of each turn, add a Water counter here. Units with HP equal to or less than the Water counters can\'t attack.','rem':''},{'kw':'Escape Hatch.','body':'Pay 3: Remove all Water counters.','rem':''}],
        flavor='The drain was never meant to drain.', badge='ROOM', svg='tw-flood',
        prompt='a white-tiled prison cell filling with murky water under a barred window, a hand reaching up from the water, number 13 painted on the wall')
    add(name='The Choice', cost=1, type='Trial', sub='Event', wing='Crimson', r='U',
        ab=[{'kw':'Trial.','body':'Your opponent chooses one: they sacrifice a unit, or you draw two cards.','rem':''}],
        flavor='"Door one, or door two? The tape is already running."', badge='TRIAL', svg='tw-choice',
        prompt='two glowing doors, one red and one green, above a table holding an old reel-to-reel tape recorder and two brass keys')
    flav = [f for f in TW_FLAVOR if f not in {c['flavor'] for c in cards}]
    r_.shuffle(flav)

    # ---- masterminds (legendary) ----
    for nm, look in MASTERMINDS:
        cost = r_.randint(5, 8); w = pick_wing('Trial') if r_.random() < .5 else r_.choice(list(TW_WINGS))
        t = r_.choice(TW_TRIAL); second = fill(r_.choice(TW_UNIT_ABIL), cost)
        ab = [{'kw':'Trial.','body':'At the start of your turn, hold a Trial: ' + fill(t, cost)['body'].replace('Your opponent','your opponent'),'rem':''}, second]
        a, h = stats_for('L', cost, 2, .4)
        add(name=nm, cost=cost, type='Mastermind', sub='Overseer', wing=w, r='L', foil=True, ab=ab, atk=a, hp=h,
            prompt=f'{look}, the sinister mastermind of a deadly escape game, imposing full figure {TW_WINGS[w][1]}')
    # ---- legendary survivors ----
    for epi in SURV_EPI:
        nm = uniq(lambda: f'{r_.choice(FIRST)} {r_.choice(LAST)}', used)
        role = r_.choice(ROLES); cost = r_.randint(3, 6); w = 'Lantern' if r_.random() < .6 else r_.choice(list(TW_WINGS))
        ab = [fill(r_.choice(TW_SURV_ABIL), cost), fill(r_.choice(TW_SURV_ABIL[2:]), cost)]
        if ab[0]['kw'] == ab[1]['kw']: ab = ab[:1]
        a, h = stats_for('L', cost, len(ab), .4)
        add(name=f'{nm}, {epi}', cost=cost, type='Survivor', sub=f'Human {role}', wing=w, r='L', foil=True, ab=ab, atk=a, hp=h,
            prompt=f'{nm}, a heroic battle-worn {role.lower()}, {r_.choice(POSES)}, {TW_WINGS[w][1]}, heroic lighting')

    def unit(t, n_total):
        for _ in range(n_total):
            cost = r_.choices(range(1, 8), weights=[3, 6, 6, 5, 3, 2, 1])[0]
            w = pick_wing(t)
            if t == 'Minion':
                adj, noun = r_.choice(MIN_ADJ), r_.choice(MIN_NOUN)
                nm = uniq(lambda: f'{r_.choice(MIN_ADJ)} {r_.choice(MIN_NOUN)}', used)
                nab = r_.choice([1, 1, 2]); pool = TW_UNIT_ABIL
                ab = []
                for t2 in r_.sample(pool, nab): ab.append(fill(t2, cost))
                a, h = stats_for('C', cost, nab, .58)
                add(name=nm, cost=cost, type='Minion', sub=r_.choice(['Masked Henchman','Construct','Hound','Orderly','Butcher','Thing']),
                    wing=w, ab=ab, atk=a, hp=h,
                    prompt=f'a menacing {nm.lower()}, a masked henchman of a deadly escape game, threatening pose, {TW_WINGS[w][1]}')
            else:
                fn = uniq(lambda: f'{r_.choice(FIRST)} {r_.choice(LAST)}', used)
                role = r_.choice(ROLES)
                nab = r_.choice([1, 1, 2]); ab = [fill(t2, cost) for t2 in r_.sample(TW_SURV_ABIL + TW_UNIT_ABIL[:1] + TW_UNIT_ABIL[13:15], nab)]
                a, h = stats_for('C', cost, nab, .4)
                add(name=f'{fn}, {role}', cost=cost, type='Survivor', sub=f'Human {role}', wing=w, ab=ab, atk=a, hp=h,
                    prompt=f'{fn}, a determined {role.lower()} trapped in a deadly escape game, {r_.choice(POSES)}, {TW_WINGS[w][1]}')
    unit('Minion', 62); unit('Survivor', 54)
    for _ in range(39):
        nm = uniq(lambda: f'{r_.choice(TRAP_A)} {r_.choice(TRAP_N)}', used); cost = r_.randint(1, 5); w = pick_wing('Trap')
        fx = r_.choice(TW_TRAP_FX); trig = r_.choice(TW_TRIG)
        body = fill(('', f'Set this face-down. When {trig}, spring it: {fx[0]}.', '', fx[2]), cost)['body']
        add(name=f'The {nm}' if r_.random() < .4 else nm, cost=cost, type='Trap', sub=r_.choice(['Mechanism','Snare','Hazard']), wing=w,
            ab=[{'kw':'Hidden.','body':body,'rem':''}], badge='TRAP',
            prompt=f'a deadly {nm.lower()} trap mechanism, ominous dramatic close-up, {TW_WINGS[w][1]}')
    for _ in range(35):
        nm = uniq(lambda: f'{r_.choice(DEV_A)} {r_.choice(DEV_N)}', used); cost = r_.randint(1, 5); w = pick_wing('Device')
        ab = [fill(r_.choice(TW_DEV), cost)]
        add(name=nm, cost=cost, type='Device', sub=r_.choice(['Clockwork','Contraption','Relic']), wing=w, ab=ab, badge='DEVICE',
            prompt=f'a sinister ornate {nm.lower()}, an antique clockwork contraption, macro still life on a scarred workbench, {TW_WINGS[w][1]}')
    for _ in range(29):
        nm = uniq(lambda: f'The {r_.choice(ROOM_A)} {r_.choice(ROOM_N)}', used); num = r_.randint(1, 99); cost = r_.randint(2, 5); w = pick_wing('Room')
        ab = [fill(r_.choice(TW_ROOM), cost), {'kw':'Escape Hatch.','body':f'Pay {r_.randint(2,4)}: Destroy this Room.','rem':''}]
        add(name=f'Room {num}: {nm}', cost=cost, type='Room', sub='Location', wing=w, ab=ab, badge='ROOM',
            prompt=f'interior of {nm.lower()[4:]}, a horror escape room, wide establishing shot, {TW_WINGS[w][1]}')
    for nm in TRIALS[:24]:
        cost = r_.randint(1, 5); w = pick_wing('Trial')
        add(name=nm, cost=cost, type='Trial', sub='Event', wing=w, ab=[fill(r_.choice(TW_TRIAL), cost)], badge='TRIAL',
            prompt=f'symbolic horror scene: {r_.choice(TRIAL_SCENES)}, {TW_WINGS[w][1]}')
    for nm in EVENTS[:22]:
        cost = r_.randint(1, 5); w = pick_wing('Event')
        add(name=nm, cost=cost, type='Event', sub='Action', wing=w, ab=[fill(r_.choice(TW_EVENT), cost)], badge='EVENT',
            prompt=f'{r_.choice(EVENT_SCENES)}, {TW_WINGS[w][1]}')
    # flavor: rarer cards and short-text cards first
    for c in sorted(cards, key=lambda c: ('LRUC'.index(c.get('r','C')) if c.get('r') else 3, len(c['ab']))):
        if not c.get('flavor') and flav and len(c['ab']) == 1: c['flavor'] = flav.pop()
    return cards

# =====================================================================
#                           STARFALL ARMADA
# =====================================================================
SF_STYLE = ('epic cinematic sci-fi concept art for a premium trading card game, detailed hard-surface spaceship and mecha design, '
            'volumetric light, lens flare, ultra detailed digital painting, AAA game key art quality, 4:3 landscape composition, '
            'no text, no letters, no watermark')
SF_FACT = {
 'United Navy': ('disciplined fleets and Shields','sleek white and navy-blue armor with gold trim'),
 'Helios Syndicate': ('Stations and Energy','polished gold and black corporate armor with glowing amber lights'),
 'Red Talon': ('raids, Ramming and Salvage','scrappy rust-red pirate armor covered in welded scrap and tally marks'),
 'Void Choir': ('Cloak and strange tricks','biomechanical violet alien hull with glowing purple veins'),
 'Frontier Union': ('Hangars and Repairs','rugged olive-green mining hulls with yellow hazard stripes'),
}
SF_PLACES = ['above a ringed gas giant','in a dense asteroid belt','near a dying red star','inside a swirling purple nebula','over a frozen moon',
             'in an orbital shipyard drydock','above a burning desert planet','at the edge of a black hole accretion disk','in a debris field of wrecked ships',
             'over a blue ocean world at dawn']
FLAGSHIPS = [('UNS Dawnbreaker','United Navy'),('HSS Gilded Sovereign','Helios Syndicate'),('"Butcher\'s Bill"','Red Talon'),('The Hymnal of Ash','Void Choir'),
             ('FUV Long Haul','Frontier Union'),('UNS Ironclad Mercy','United Navy'),('HSS Aurelian Throne','Helios Syndicate'),('"Widowmaker"','Red Talon'),
             ('Void Seed "Aeon"','Void Choir'),('FUV Stubborn Ox','Frontier Union'),('UNS Starfall','United Navy'),('HSS Ledger of Suns','Helios Syndicate'),
             ('"Kraken\'s Maw"','Red Talon'),('The Silent Cathedral','Void Choir')]
CLASS_W = ['Halberd','Tempest','Resolute','Valkyrie','Corsair','Gladius','Nomad','Aegis','Brimstone','Harbinger','Seraph','Mako','Orca','Bastille',
           'Cinder','Lodestar','Typhoon','Wraith','Anvil','Cutlass','Meridian','Javelin','Hydra','Pilgrim','Scythe','Tortoise','Vesper','Zenith']
CLASSES = ['Frigate','Destroyer','Cruiser','Carrier','Corvette','Gunship','Monitor','Battlecruiser']
MODEL = ['Vanguard','Bastion','Striker','Goliath','Kestrel','Rampart','Hydra','Titan','Mantis','Sentinel','Raptor','Atlas','Ronin','Banshee',
         'Brawler','Paladin','Reaper','Juggernaut','Specter','Longbow']
CALL = ['Hammer','Lucky','Gravedigger','Halo','Nightjar','Ironsides','Comet','Bulldog','Wraith','Saint','Viper','Boxcar','Monsoon','Ember',
        'Glacier','Tusk','Hex','Echo','Rook','Stinger','Doc','Blackjack','Cinder','Sundog','Mule','Lancer','Zero','Chaplain']
RANK = ['Commander','Lieutenant','Ensign','Captain','Major','Sergeant','Chief','Wing Leader']
PF = 'Kenji Amara Dmitri Sol Priya Mateo Yuki Kwame Freya Rashid Lena Tomas Nia Oskar Mei Darius Zara Ivo Leila Rhys Ayo Santi Hana Bram Tavi Keira Juno Emeka Soren Lucia'.split()
PL = 'Okafor Tanaka Reyes Volkov Sharma Lindqvist Haddad Moreau Nakamura Ortega Kowalski Mensah Brandt Castillo Ivanova Quist Arden Sato Novak Achebe Ferro Kade Lund Maro Petrov Rook Salas Teague Vey Wilde'.split()
SQ_A = ['Hornet','Lancer','Spectre','Ember','Ghost','Comet','Dagger','Wasp','Falcon','Raven','Sparrow','Phoenix','Locust','Jackal','Kite','Starling','Hellcat','Mosquito']
SQ_N = ['Wing','Squadron','Flight','Swarm']
TACTICS = ['Full Broadside','Evasive Maneuvers','Emergency Warp','Shield Overload','Target Lock','Boarding Party','EMP Burst','Salvage Run',
           'Decoy Beacon','Torpedo Spread','Reactor Overclock','Scramble Fighters','Hold the Line','Flank Speed','Minefield','Tractor Beam',
           'Kinetic Barrage','Ion Storm','Distress Call','Last Stand','Hull Breach','Sensor Ghost','Rail Volley','Point Defense Grid',
           'Counter-Battery Fire','Ram Speed','Black Box Recovery','Field Repairs','Supply Drop','Signal Jammer','Nova Charge','Gravity Well',
           'Cold Launch','Ambush in the Rings','Comms Blackout','Ace Maneuver','Override Protocol','Abandon Ship','Void Whisper','Plasma Lance',
           'Strategic Retreat','Coordinated Strike','Flak Screen','Quantum Jump']
STATIONS = ['Kepler Drydock','Halcyon Relay','Fort Meridian','Tycho Refinery','Bastion Gate','Corsair\'s Rest','Ceres Exchange','The Choir\'s Spire',
            'Haven Ring','Ironworks Platform','Lantern Beacon','Arclight Array','Outpost Nine','Sundial Observatory']
UPGRADES = ['Reactive Armor Plating','Ion Cannon Mount','Shield Capacitor','Targeting Computer','Afterburners','Point-Defense Turrets','Stealth Coating',
            'Neural Link','Railgun Spine','Repair Drones','Cargo Pods','Jump Drive','Flak Batteries','Overcharged Core','Hardlight Blade']
SF_UNIT = [
 ('Shields {n}.','','(Prevent the first {n} damage dealt to this each turn.)',0.35),
 ('Swift.','','(Can attack the turn it enters.)',0),
 ('Hangar {n}.','At the start of your turn, launch a 1/1 Fighter token.','(Up to {n} at a time.)',0.3),
 ('Broadside {n}.','When this attacks, deal {n} damage to each other enemy ship.','',0.25),
 ('Screen.','Your other ships take 1 less damage from attacks.','',0),
 ('Cloak.','Can\'t be targeted by Tactics until it attacks.','',0),
 ('Lock-On.','When this enters, deal {n} damage to an enemy ship or Frame.','',0.5),
 ('Salvage.','Whenever an enemy unit is destroyed, gain 1 extra Energy next turn.','',0),
 ('Warp.','Pay 2: Return this to your hand.','',0),
 ('Ram.','When this attacks, deal {n} damage to the blocker before combat.','',0.5),
 ('Repair {n}.','At the end of your turn, restore {n} Hull to another ship.','',0.4),
 ('Point Defense.','Fighters and Squadrons deal no damage to this.','',0),
 ('Flak.','When this enters, deal 1 damage to each enemy Squadron.','',0),
 ('Escort.','Your Flagship has +1 Shields.','',0),
 ('Overdrive.','Pay 2: +3 ATK until end of turn. Then this loses its Shields.','',0),
]
SF_FRAME = [('Pilot Slot.','While a Pilot is attached, this gets +2 ATK and Swift.','',0),
            ('Jump Jets.','Can attack ships with Cloak.','',0),('Heavy Plating.','Takes 1 less damage from Tactics.','',0)]
SF_PILOT = [('Pilot.','Attach to a Frame you control. It gets +{n} ATK.','(If the Frame is destroyed, return this to your hand.)',0.4),
            ('Pilot.','Attach to a Frame you control. It gets Shields {n}.','(If the Frame is destroyed, return this to your hand.)',0.35),
            ('Pilot.','Attach to a ship or Frame you control. It gets Swift and +1 ATK.','(If it is destroyed, return this to your hand.)',0)]
SF_PILOT2 = [('Ace.','The first time each turn the attached unit destroys a unit, draw a card.','',0),
             ('Veteran.','The attached unit can\'t be destroyed by Tactics.','',0),
             ('Tactician.','Your Tactics cost 1 less.','',0),('Wingman.','Your Squadrons get +1 ATK.','',0),
             ('Daredevil.','The attached unit gets +2 ATK when attacking a bigger unit.','',0),
             ('Engineer.','At the end of your turn, restore {n} Hull to the attached unit.','',0.4)]
SF_TACTIC = [('Strike.','Deal {n} damage to a ship or Frame.','',1.1),('Barrage.','Deal {n} damage split as you choose among enemy units.','',1.0),
             ('Shields Up.','Your units get +{n} Shields until end of turn.','',0.4),('Intel.','Draw {n} cards.','',0.5),
             ('Retreat.','Return a unit to its owner\'s hand.','',0),('Repairs.','Restore {n} Hull to each of your ships.','',0.8),
             ('Overclock.','Gain {n} extra Energy this turn.','',0.5),('Launch.','Create {n} 1/1 Fighter tokens with Swift.','',0.6),
             ('Disable.','An enemy unit can\'t attack or block next turn and loses its Shields.','',0),
             ('Pierce.','Deal {n} damage to a unit. Shields don\'t stop this damage.','',0.9)]
SF_STATION = [('Orbit.','At the start of your turn, gain 1 extra Energy this turn.','',0),('Orbit.','At the start of your turn, restore {n} Hull to a ship you control.','',0.5),
              ('Orbit.','At the start of your turn, launch a 1/1 Fighter token.','',0),('Orbit.','Your ships get +1 Shields.','',0),
              ('Orbit.','At the start of your turn, deal 1 damage to each enemy Squadron.','',0),('Orbit.','At the start of your turn, look at the top card of your deck. You may put it on the bottom.','',0)]
SF_UPG = [('Install.','Attach to a ship or Frame you control. It gets +{n} ATK.','',0.6),('Install.','Attach to a ship or Frame you control. It gets +{n} Shields.','',0.4),
          ('Install.','Attach to a ship you control. It gets Swift and Warp.','',0),('Install.','Attach to a ship you control. It gets Broadside 1.','',0),
          ('Install.','Attach to a unit you control. It gets Repair {n}.','',0.4),('Install.','Attach to a unit you control. It gets Cloak.','',0)]
SF_FLAVOR = ['Flagship of the Seventh Fleet. Eleven kilometers of bad news.','Ten meters of armor, waiting for a heartbeat.','"Talon, wake up. We have work."',
 'Fast, cheap and always first through the breach.','Fire mission confirmed. Impact in four seconds.','Fuel, repairs and a cold drink. In that order.',
 'In space, nobody hears you reload.','The Belt doesn\'t care who wins. It just keeps score.','Shields at forty percent. Smile anyway.',
 '"Bring her about. Let them see our teeth."','Every hull plate has a name painted on the inside.','The Choir sings in frequencies that make radios weep.',
 'Profit is just victory with paperwork.','Red Talon doesn\'t sink ships. It recycles them.','Out here, a wrench is worth more than a medal.',
 '"Launch everything. And I mean everything."','The stars are only quiet until the fleet arrives.','Ninety seconds to jump. Make them count.',
 'Pilots say the Frame dreams when it\'s powered down.','Gold paint, black heart, perfect aim.','The Frontier builds things to last. Usually.',
 '"Hold the line until the line holds you."','A thousand tons of steel, falling in perfect formation.','When the lights go purple, run.',
 'The navy has a regulation for everything. Except this.','Its reactor hums like a lullaby. Its guns do not.','"Ace is a title. Alive is a skill."',
 'Salvage rights belong to whoever\'s still breathing.','Sensors showed nothing. Then they showed everything.','The rings of Kessa hide a thousand wrecks.',
 'Built in orbit. Born for war.','Station life: cramped, loud and the only home they have.','"Lock on. Breathe out. Fire."',
 'The hangar doors opened like a mouth.','Starlight is just old news from very far away.','"We don\'t retreat. We advance somewhere else."',
 'Its hull still carries scorch marks from the first war.','The Void Choir does not negotiate. It harmonizes.','Each kill marked with a strip of red paint.',
 'Engines lit. Course laid in. No turning back.','Every pilot remembers their first drop.','The miners called it the Long Haul. The pirates called it lunch.',
 'Mass times velocity equals respect.','The jump drive whined like a dying star.','A station is a promise that someone will come back.',
 '"Shields are for people who plan to miss."','Gravity is a suggestion. Thrust is an argument.','The fleet moved like one creature with many hearts.',
 'Somewhere in the dark, the Choir was listening.','Rust never sleeps, and neither do the Talon.','Every Frame has a pilot. Every pilot has a reason.',
 'The battle lasted eleven minutes. The repairs took a year.','"Light them up."','Twenty fighters in, nineteen fighters home. Good day.',
 'The Syndicate bills by the second.','From orbit, every city looks like a target.','Hard light, harder decisions.','Its silence was louder than the guns.',
 'They named it after the dawn because it always arrives.','No one remembers who fired first. Everyone remembers who fired last.']

def sf_cards():
    r_.seed(4310)
    cards, used = [], set()
    def add(**c):
        c.setdefault('set', 'SFA'); cards.append(c); used.add(c['name']); return c
    add(name="UNS Leviathan's Wake", cost=8, type='Flagship', sub='Dreadnought', wing='United Navy', r='L', foil=True,
        ab=[{'kw':'Broadside.','body':'When this attacks, deal 2 damage to each other enemy ship.','rem':''},{'kw':'Hangar 2.','body':'At the start of your turn, launch a 1/1 Fighter token.','rem':'(Up to 2 at a time.)'}],
        flavor='Flagship of the Seventh Fleet. Eleven kilometers of bad news.', atk=9, hull=12, shld=3, svg='sf-leviathan',
        prompt='a colossal wedge-shaped grey navy dreadnought battleship with turrets and a bridge tower firing a red laser volley, escort ships around it, an orange planet below')
    add(name='Vanguard Frame "Talon"', cost=5, type='Frame', sub='Assault Mech', wing='United Navy', r='R',
        ab=[{'kw':'Pilot Slot.','body':'While a Pilot is attached, this gets +2 ATK and can attack the turn it enters.','rem':''},{'kw':'Overdrive.','body':'Pay 2: +3 ATK until end of turn. Then this loses its Shields.','rem':''}],
        flavor='Ten meters of armor, waiting for a heartbeat.', atk=5, hull=6, shld=1, svg='sf-talon',
        prompt='a towering white and orange armored battle mech standing in a hangar bay under floodlights, welding sparks, hazard stripes on the floor')
    add(name='Commander Ilsa Varro', cost=3, type='Pilot', sub='Human Ace', wing='United Navy', r='R',
        ab=[{'kw':'Pilot.','body':'Attach to a Frame you control. That Frame gets +1 ATK and Shields 1.','rem':'(If the Frame falls, Ilsa returns to hand.)'},{'kw':'Ace.','body':'The first time each turn the attached Frame destroys a unit, draw a card.','rem':''}],
        flavor='"Talon, wake up. We have work."', atk=2, hull=2, svg='sf-ilsa',
        prompt='close portrait of a determined female mech pilot in a white flight helmet, sunset reflected in her visor, glowing cockpit HUD around her')
    add(name='Interceptor Wing', cost=2, type='Squadron', sub='Fighters', wing='Frontier Union', r='C',
        ab=[{'kw':'Swift.','body':'Can attack the turn it enters.','rem':''},{'kw':'Screen.','body':'Ships you control with Hangar take 1 less damage from attacks.','rem':''}],
        flavor='Fast, cheap and always first through the breach.', atk=2, hull=1, svg='sf-wing',
        prompt='a squadron of orange-winged interceptor fighters streaking through a colorful nebula, engine trails')
    add(name='Orbital Lance Strike', cost=4, type='Tactic', sub='Bombardment', wing='Helios Syndicate', r='U',
        ab=[{'kw':'Strike.','body':'Deal 5 damage to a ship or Frame. Shields don\'t stop this damage.','rem':''},{'kw':'Overcharge.','body':'If you control a Station, deal 2 damage to your opponent too.','rem':''}],
        flavor='Fire mission confirmed. Impact in four seconds.', badge='TACTIC', svg='sf-lance',
        prompt='a white-hot energy beam fired from an orbital platform striking a planet surface, shockwave rings spreading through clouds')
    add(name='Helios Station', cost=4, type='Station', sub='Orbital', wing='Helios Syndicate', r='U',
        ab=[{'kw':'Orbit.','body':'At the start of your turn, gain 1 extra Energy this turn.','rem':''},{'kw':'Drydock.','body':'Pay 2: Restore 3 Hull to a ship you control.','rem':''}],
        flavor='Fuel, repairs and a cold drink. In that order.', badge='STATION', svg='sf-helios',
        prompt='a huge ring-shaped space station with solar panel arrays silhouetted against a blazing star')
    flav = [f for f in SF_FLAVOR if f not in {c.get('flavor') for c in cards}]; r_.shuffle(flav)
    F = list(SF_FACT)
    def look(f): return SF_FACT[f][1]
    def shipstats(r, cost, ab, lean=.5):
        a, h = stats_for(r or 'C', cost, len(ab), lean)
        sh = next((int(re.findall(r'\d+', x['kw'])[0]) for x in ab if x['kw'].startswith('Shields')), None)
        return a, h, sh
    # flagships
    for nm, fac in FLAGSHIPS:
        cost = r_.randint(7, 9); ab = [fill(t, cost) for t in r_.sample([SF_UNIT[0], SF_UNIT[2], SF_UNIT[3], SF_UNIT[10], SF_UNIT[6]], 2)]
        a, h, sh = shipstats('L', cost, ab, .42)
        add(name=nm, cost=cost, type='Flagship', sub=r_.choice(['Dreadnought','Supercarrier','Battleship','Command Ship']), wing=fac, r='L', foil=True,
            ab=ab, atk=a, hull=h + 2, shld=sh, prompt=f'a colossal flagship battleship with {look(fac)}, majestic hero shot with escort ships, {r_.choice(SF_PLACES)}')
    # ships
    for _ in range(70):
        cl = r_.choice(CLASSES); nm = uniq(lambda: f'{r_.choice(CLASS_W)}-class {cl}', used); fac = r_.choice(F)
        cost = {'Corvette':2,'Frigate':3,'Gunship':3,'Destroyer':4,'Monitor':5,'Cruiser':5,'Carrier':6,'Battlecruiser':6}[cl] + r_.choice([-1,0,0,1])
        cost = max(1, cost); nab = r_.choice([1, 2, 2])
        pool = SF_UNIT if cl != 'Carrier' else [SF_UNIT[2]] + SF_UNIT
        ab = [fill(t, cost) for t in r_.sample(pool, nab)] if cl != 'Carrier' else [fill(SF_UNIT[2], cost)] + [fill(r_.choice(SF_UNIT[3:]), cost)]
        a, h, sh = shipstats(None, cost, ab)
        add(name=nm, cost=cost, type='Ship', sub=cl, wing=fac, ab=ab, atk=a, hull=h, shld=sh,
            prompt=f'a {cl.lower()} warship with {look(fac)}, dynamic three-quarter view in combat, {r_.choice(SF_PLACES)}')
    # frames
    for _ in range(59):
        nm = uniq(lambda: f'{r_.choice(MODEL)} Frame "{r_.choice(CALL)}"', used); fac = r_.choice(F); cost = r_.randint(2, 7)
        ab = [fill(r_.choice(SF_FRAME), cost)] + ([fill(r_.choice(SF_UNIT[:2] + SF_UNIT[6:7] + SF_UNIT[9:10] + SF_UNIT[14:]), cost)] if r_.random() < .6 else [])
        a, h, sh = shipstats(None, cost, ab, .55)
        add(name=nm, cost=cost, type='Frame', sub=r_.choice(['Assault Mech','Heavy Mech','Scout Mech','Siege Mech','Duelist Mech']), wing=fac, ab=ab,
            atk=a, hull=h, shld=sh, prompt=f'a giant armored battle mech with {look(fac)}, heroic low-angle pose, {r_.choice(["in a hangar bay under floodlights","on a moon surface with Earth-like planet above","mid-battle on an asteroid with explosions behind","launching from a carrier catapult"])}')
    # pilots
    for _ in range(44):
        nm = uniq(lambda: f'{r_.choice(RANK)} {r_.choice(PF)} {r_.choice(PL)}', used); fac = r_.choice(F); cost = r_.randint(1, 4)
        ab = [fill(r_.choice(SF_PILOT), cost)] + ([fill(r_.choice(SF_PILOT2), cost)] if r_.random() < .65 else [])
        a, h = stats_for('C', cost, len(ab), .5)
        add(name=nm, cost=cost, type='Pilot', sub=r_.choice(['Human Ace','Human Officer','Human Veteran','Cyborg Ace','Human Rookie']), wing=fac, ab=ab,
            atk=a, hull=h, prompt=f'a cinematic portrait of {nm.split(" ",1)[1]}, a mech pilot in a flight suit and helmet with {look(fac)}, glowing cockpit HUD reflections')
    # squadrons
    for _ in range(34):
        nm = uniq(lambda: f'{r_.choice(SQ_A)} {r_.choice(SQ_N)}', used); fac = r_.choice(F); cost = r_.randint(1, 4)
        ab = [{'kw':'Swift.','body':'','rem':'(Can attack the turn it enters.)'}] + ([fill(r_.choice(SF_UNIT[4:]), cost)] if r_.random() < .6 else [])
        a, h, sh = shipstats(None, cost, ab, .62)
        add(name=nm, cost=cost, type='Squadron', sub='Fighters', wing=fac, ab=ab, atk=a, hull=h, shld=sh,
            prompt=f'a squadron of agile starfighters with {look(fac)} flying in tight formation, engine trails, {r_.choice(SF_PLACES)}')
    for nm in TACTICS:
        fac = r_.choice(F); cost = r_.randint(1, 6); ab = [fill(r_.choice(SF_TACTIC), cost)]
        add(name=nm, cost=cost, type='Tactic', sub=r_.choice(['Maneuver','Bombardment','Protocol','Gambit']), wing=fac, ab=ab, badge='TACTIC',
            prompt=f'dramatic space battle moment illustrating "{nm}", warships with {look(fac)}, {r_.choice(SF_PLACES)}')
    for nm in STATIONS:
        fac = r_.choice(F); cost = r_.randint(3, 5); ab = [fill(r_.choice(SF_STATION), cost)]
        add(name=nm, cost=cost, type='Station', sub='Orbital', wing=fac, ab=ab, badge='STATION',
            prompt=f'a massive orbital space station with {look(fac)}, docking ships around it, {r_.choice(SF_PLACES)}')
    for nm in UPGRADES:
        fac = r_.choice(F); cost = r_.randint(1, 4); ab = [fill(r_.choice(SF_UPG), cost)]
        add(name=nm, cost=cost, type='Upgrade', sub='Equipment', wing=fac, ab=ab, badge='UPGRADE',
            prompt=f'technical hero shot of {nm.lower()} being mounted onto a warship hull with {look(fac)}, engineers and sparks, shipyard lighting')
    for c in sorted(cards, key=lambda c: ('LRUC'.index(c['r']) if c.get('r') else 3, len(c['ab']))):
        if not c.get('flavor') and flav and len(c['ab']) == 1: c['flavor'] = flav.pop()
    return cards

def finish(cards, code, style, typeorder, wingorder):
    assert len(cards) == 300, (code, len(cards))
    assign_rarities(cards, None)
    cards.sort(key=lambda c: (wingorder.index(c['wing']), typeorder.index(c['type']), c['cost'], c['name']))
    for i, c in enumerate(cards, 1):
        c['num'] = f'{i:03d}/300'; c['id'] = f'{code}-{i:03d}'
        c['art_prompt'] = f"{c.pop('prompt')}. {style}"
        if c.get('type') in ('Mastermind',) or c['r'] == 'L': c['foil'] = True
    return cards

tw = finish(tw_cards(), 'TW', TW_STYLE, ['Mastermind','Survivor','Minion','Trap','Device','Room','Trial','Event'], list(TW_WINGS))
sf = finish(sf_cards(), 'SFA', SF_STYLE, ['Flagship','Ship','Frame','Pilot','Squadron','Station','Upgrade','Tactic'], list(SF_FACT))
sets = {
 'TW': {'code':'TW','name':'TRAPWORKS','subtitle':'The Lower Floors','wings':{k:v[0] for k,v in TW_WINGS.items()},'cards':tw},
 'SFA':{'code':'SFA','name':'STARFALL ARMADA','subtitle':'Battle for the Helios Belt','wings':{k:v[0] for k,v in SF_FACT.items()},'cards':sf},
}
for k, s in sets.items():
    json.dump(s, open(os.path.join(OUT, f'cards_{k.lower()}.json'), 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, f'art_prompts_{k.lower()}.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['id', 'name', 'type', 'rarity', 'file_to_save_as', 'prompt'])
        for c in s['cards']: w.writerow([c['id'], c['name'], c['type'], c['r'], f"art/{k}/{c['id']}.png", c['art_prompt']])
open(os.path.join(OUT, 'cards.js'), 'w', encoding='utf-8').write('window.CARD_SETS=' + json.dumps(sets, ensure_ascii=False) + ';')
from collections import Counter
for k, s in sets.items():
    print(k, len(s['cards']), Counter(c['r'] for c in s['cards']), Counter(c['type'] for c in s['cards']))
