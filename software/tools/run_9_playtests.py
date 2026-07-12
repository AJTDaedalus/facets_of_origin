import json
import urllib.request
import urllib.error
import time
import websocket
import random

BASE_URL = "http://127.0.0.1:8010"
WS_URL = "ws://127.0.0.1:8010/ws"
MM_PASSWORD = "testpass123!"

# Adventure names and character configurations for 9 runs
ADVENTURES = [
    {
        "name": "The Shattered Crypt",
        "enemy_id": "husk",
        "enemy_name": "Crypt Wight (TR 2)",
        "players": {
            "Gideon": {"facet": "body", "bg": "city_watch_veteran", "attrs": {"strength": 3, "dexterity": 2, "constitution": 3, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 1, "luck": 2, "charisma": 2}},
            "Kaelen": {"facet": "soul", "bg": "temple_acolyte", "attrs": {"strength": 1, "dexterity": 2, "constitution": 2, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 3, "luck": 2, "charisma": 3}, "domain": "resonance"}
        }
    },
    {
        "name": "The Whispering Caverns",
        "enemy_id": "husk",
        "enemy_name": "Sonic Bat (TR 1)",
        "players": {
            "Lyra": {"facet": "mind", "bg": "guild_apprentice", "attrs": {"strength": 1, "dexterity": 3, "constitution": 2, "intelligence": 3, "wisdom": 2, "knowledge": 2, "spirit": 2, "luck": 2, "charisma": 1}},
            "Finn": {"facet": "body", "bg": "arena_fighter", "attrs": {"strength": 3, "dexterity": 2, "constitution": 2, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 1, "luck": 3, "charisma": 2}}
        }
    },
    {
        "name": "The Molten Abyss",
        "enemy_id": "the_resonance",
        "enemy_name": "Magma Golem (TR 9)",
        "players": {
            "Ignis": {"facet": "soul", "bg": "temple_acolyte", "attrs": {"strength": 2, "dexterity": 2, "constitution": 2, "intelligence": 1, "wisdom": 2, "knowledge": 2, "spirit": 3, "luck": 2, "charisma": 2}, "domain": "warding"},
            "Brutus": {"facet": "body", "bg": "city_watch_veteran", "attrs": {"strength": 3, "dexterity": 1, "constitution": 3, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 2, "luck": 2, "charisma": 2}}
        }
    },
    {
        "name": "The Glacial Spire",
        "enemy_id": "husk",
        "enemy_name": "Ice Spider (TR 3)",
        "players": {
            "Eira": {"facet": "mind", "bg": "guild_apprentice", "attrs": {"strength": 1, "dexterity": 3, "constitution": 1, "intelligence": 3, "wisdom": 3, "knowledge": 2, "spirit": 2, "luck": 2, "charisma": 1}, "domain": "warding"},
            "Vane": {"facet": "body", "bg": "arena_fighter", "attrs": {"strength": 2, "dexterity": 3, "constitution": 2, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 1, "luck": 3, "charisma": 2}}
        }
    },
    {
        "name": "The Overgrown Canopy",
        "enemy_id": "husk",
        "enemy_name": "Spore Stalker (TR 2)",
        "players": {
            "Flora": {"facet": "soul", "bg": "temple_acolyte", "attrs": {"strength": 1, "dexterity": 2, "constitution": 2, "intelligence": 2, "wisdom": 3, "knowledge": 2, "spirit": 3, "luck": 1, "charisma": 2}, "domain": "resonance"},
            "Thorn": {"facet": "body", "bg": "city_watch_veteran", "attrs": {"strength": 3, "dexterity": 2, "constitution": 2, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 1, "luck": 2, "charisma": 3}}
        }
    },
    {
        "name": "The Iron Citadel",
        "enemy_id": "the_resonance",
        "enemy_name": "Steel Sentinel (TR 8)",
        "players": {
            "Ferrum": {"facet": "body", "bg": "arena_fighter", "attrs": {"strength": 3, "dexterity": 2, "constitution": 3, "intelligence": 1, "wisdom": 2, "knowledge": 1, "spirit": 2, "luck": 2, "charisma": 2}},
            "Sophia": {"facet": "mind", "bg": "guild_apprentice", "attrs": {"strength": 1, "dexterity": 2, "constitution": 2, "intelligence": 3, "wisdom": 2, "knowledge": 3, "spirit": 2, "luck": 1, "charisma": 2}, "domain": "warding"}
        }
    },
    {
        "name": "The Abyssal Rift",
        "enemy_id": "the_hollow",
        "enemy_name": "Void Shadow (TR 7)",
        "players": {
            "Umbra": {"facet": "soul", "bg": "temple_acolyte", "attrs": {"strength": 1, "dexterity": 2, "constitution": 2, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 3, "luck": 2, "charisma": 3}, "domain": "resonance"},
            "Lux": {"facet": "mind", "bg": "guild_apprentice", "attrs": {"strength": 2, "dexterity": 2, "constitution": 2, "intelligence": 3, "wisdom": 2, "knowledge": 2, "spirit": 2, "luck": 2, "charisma": 1}, "domain": "warding"}
        }
    },
    {
        "name": "The Lightning Ridge",
        "enemy_id": "husk",
        "enemy_name": "Storm Griffin (TR 4)",
        "players": {
            "Zephyr": {"facet": "body", "bg": "arena_fighter", "attrs": {"strength": 2, "dexterity": 3, "constitution": 2, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 1, "luck": 3, "charisma": 2}},
            "Volt": {"facet": "soul", "bg": "temple_acolyte", "attrs": {"strength": 1, "dexterity": 2, "constitution": 2, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 3, "luck": 2, "charisma": 3}, "domain": "resonance"}
        }
    },
    {
        "name": "The Clockwork Workshop",
        "enemy_id": "the_resonance",
        "enemy_name": "Steam Titan (TR 9)",
        "players": {
            "Gear": {"facet": "mind", "bg": "guild_apprentice", "attrs": {"strength": 1, "dexterity": 2, "constitution": 2, "intelligence": 3, "wisdom": 2, "knowledge": 3, "spirit": 2, "luck": 1, "charisma": 2}, "domain": "warding"},
            "Rust": {"facet": "body", "bg": "city_watch_veteran", "attrs": {"strength": 3, "dexterity": 2, "constitution": 3, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 1, "luck": 2, "charisma": 2}}
        }
    }
]

def _api(method: str, path: str, token: str = "", body: dict | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode() if e.fp else str(e)
        raise AssertionError(f"{method} {path} → {e.code}: {detail}") from e

def run():
    print("=== STARTING 9 SEQUENTIAL AUTOMATED PLAYTESTS ===")
    
    # 1. Login as MM
    mm_token = _api("POST", "/api/sessions/auth/mm-login", body={"password": MM_PASSWORD})["access_token"]
    
    results = []
    
    for idx, adv in enumerate(ADVENTURES):
        print(f"\n--- Running Playtest {idx+2}: {adv['name']} ---")
        
        # Create session
        session_id = _api("POST", "/api/sessions/", mm_token, {"name": f"Playtest {idx+2}: {adv['name']}", "active_facet_ids": ["base"]})["session_id"]
        
        # Invite & Join players
        player_tokens = {}
        for p_name, p_config in adv["players"].items():
            invite = _api("POST", "/api/sessions/invite", mm_token, {"session_id": session_id, "player_name": p_name})
            invite_token = invite["invite_url"].split("token=")[-1]
            token = _api("POST", "/api/sessions/join", body={"invite_token": invite_token})["access_token"]
            player_tokens[p_name] = token
            
            # Create character
            _api("POST", "/api/characters/", token, {
                "session_id": session_id,
                "character_name": p_name,
                "primary_facet": p_config["facet"],
                "attributes": p_config["attrs"],
                "background_id": p_config["bg"],
                "magic_domain": p_config.get("domain")
            })
            
        # Connect WebSockets
        player_ws_list = {}
        for p_name, token in player_tokens.items():
            ws = websocket.create_connection(WS_URL)
            ws.send(json.dumps({"token": token, "session_id": session_id}))
            ws.recv() # state
            player_ws_list[p_name] = ws
            
        mm_ws = websocket.create_connection(WS_URL)
        mm_ws.send(json.dumps({"token": mm_token, "session_id": session_id}))
        mm_ws.recv() # state
        
        # Start combat
        mm_ws.send(json.dumps({"type": "combat_start"}))
        time.sleep(0.1)
        
        # Declare postures
        postures = ["aggressive", "defensive", "measured"]
        for p_name, ws in player_ws_list.items():
            posture = random.choice(postures)
            ws.send(json.dumps({"type": "declare_posture", "posture": posture}))
            
        time.sleep(0.1)
        mm_ws.send(json.dumps({"type": "reveal_postures"}))
        time.sleep(0.1)
        
        # Spawn enemy
        mm_ws.send(json.dumps({"type": "spawn_enemy", "enemy_id": adv["enemy_id"], "instance_name": adv["enemy_name"]}))
        time.sleep(0.1)
        
        # Play out combat strikes & reactions
        rolls = []
        for p_name, ws in player_ws_list.items():
            # Strike
            ws.send(json.dumps({
                "type": "strike",
                "attribute_id": "strength" if adv["players"][p_name]["facet"] == "body" else "dexterity",
                "skill_id": "combat",
                "target": adv["enemy_name"],
                "difficulty": "Standard",
                "sparks_spent": 0,
                "press": False
            }))
            
            time.sleep(0.1)
            
            # Read strike result
            def read_until(ws_conn, t):
                ws_conn.settimeout(2.0)
                try:
                    while True:
                        m = json.loads(ws_conn.recv())
                        if m.get("type") == t:
                            return m
                except:
                    return None
            
            strike_msg = read_until(ws, "strike_result")
            if strike_msg:
                roll_info = strike_msg.get("roll", {})
                rolls.append({
                    "player": p_name,
                    "action": "strike",
                    "total": roll_info.get("total"),
                    "outcome": roll_info.get("outcome")
                })
                
            # React
            ws.send(json.dumps({"type": "react", "reaction": "dodge"}))
            time.sleep(0.1)
            react_msg = read_until(ws, "react_result")
            if react_msg and react_msg.get("roll"):
                roll_info = react_msg.get("roll", {})
                rolls.append({
                    "player": p_name,
                    "action": "react_dodge",
                    "total": roll_info.get("total"),
                    "outcome": roll_info.get("outcome")
                })
                
        # Cast Magic if any player has domain
        for p_name, ws in player_ws_list.items():
            if adv["players"][p_name].get("domain"):
                ws.send(json.dumps({
                    "type": "cast",
                    "scope": "minor",
                    "intent": f"Cast a spell related to {adv['players'][p_name]['domain']}"
                }))
                time.sleep(0.1)
                cast_msg = read_until(ws, "cast_result")
                if cast_msg:
                    roll_info = cast_msg.get("roll", {})
                    rolls.append({
                        "player": p_name,
                        "action": f"cast_{adv['players'][p_name]['domain']}",
                        "total": roll_info.get("total"),
                        "outcome": roll_info.get("outcome")
                    })
                    
        # End exchange and combat
        mm_ws.send(json.dumps({"type": "end_exchange"}))
        time.sleep(0.1)
        mm_ws.send(json.dumps({"type": "combat_end"}))
        time.sleep(0.1)
        
        # Clean up
        for ws in player_ws_list.values():
            ws.close()
        mm_ws.close()
        
        # Aggregate stats
        success_count = sum(1 for r in rolls if r.get("outcome") == "full_success")
        partial_count = sum(1 for r in rolls if r.get("outcome") == "partial_success")
        failure_count = sum(1 for r in rolls if r.get("outcome") == "failure")
        
        results.append({
            "playtest_index": idx + 2,
            "adventure_name": adv["name"],
            "enemy_name": adv["enemy_name"],
            "successes": success_count,
            "partials": partial_count,
            "failures": failure_count,
            "rolls": rolls
        })
        print(f"Playtest {idx+2} completed. Full Success: {success_count}, Partial Success: {partial_count}, Failure: {failure_count}")
        time.sleep(1) # cool down for rate limits
        
    print("\n=== All Playtests Completed successfully ===")
    
    with open("Z:/root/facets_of_origin/playtest/06_expert_novice_campaign/batch_results.json", "w") as f:
        json.dump(results, f, indent=2)
        print("Wrote batch results to Z:/root/facets_of_origin/playtest/06_expert_novice_campaign/batch_results.json")
        
if __name__ == "__main__":
    run()
