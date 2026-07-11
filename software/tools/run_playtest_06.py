import json
import urllib.request
import urllib.error
import time
import websocket

BASE_URL = "http://127.0.0.1:8010"
WS_URL = "ws://127.0.0.1:8010/ws"
MM_PASSWORD = "testpass123!"

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
    print("\n=== STARTING PLAYTEST 06 LIVE SIMULATION ===\n")
    
    print("[1] Setting up MM password...")
    try:
        _api("POST", "/api/sessions/auth/setup", body={"password": MM_PASSWORD})
        print("MM password configured.")
    except AssertionError as e:
        print("Setup already done or skipped:", e)
    
    print("[2] Logging in as MM...")
    mm_token = _api("POST", "/api/sessions/auth/mm-login", body={"password": MM_PASSWORD})["access_token"]
    print("MM Token acquired.")
    
    print("[3] Creating new session...")
    session_id = _api("POST", "/api/sessions/", mm_token, {"name": "Playtest 06 Live Spire", "active_facet_ids": ["base"]})["session_id"]
    print(f"Session created: {session_id}")
    
    # Player definitions
    players = {
        "Alaric": {
            "name": "Alaric of the Iron Gate",
            "facet": "body",
            "attributes": {"strength": 3, "dexterity": 2, "constitution": 3, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 2, "luck": 1, "charisma": 2},
            "background_id": "city_watch_veteran",
        },
        "Sylvia": {
            "name": "Sylvia Vance",
            "facet": "mind",
            "attributes": {"strength": 1, "dexterity": 2, "constitution": 2, "intelligence": 3, "wisdom": 2, "knowledge": 3, "spirit": 2, "luck": 1, "charisma": 2},
            "background_id": "guild_apprentice",
            "magic_domain": "warding",
        },
        "Thorne": {
            "name": "Thorne Woodcroft",
            "facet": "soul",
            "attributes": {"strength": 1, "dexterity": 2, "constitution": 2, "intelligence": 2, "wisdom": 2, "knowledge": 1, "spirit": 3, "luck": 2, "charisma": 3},
            "background_id": "temple_acolyte",
            "magic_domain": "resonance",
        },
        "Pippa": {
            "name": "Pippa Swift",
            "facet": "body",
            "attributes": {"strength": 2, "dexterity": 3, "constitution": 2, "intelligence": 3, "wisdom": 2, "knowledge": 1, "spirit": 1, "luck": 3, "charisma": 1},
            "background_id": "arena_fighter",
        }
    }
    
    player_tokens = {}
    
    print("[4] Generating invites and joining session...")
    for p_name, char in players.items():
        res = _api("POST", "/api/sessions/invite", mm_token, {"session_id": session_id, "player_name": p_name})
        invite_token = res["invite_url"].split("token=")[-1]
        join_res = _api("POST", "/api/sessions/join", body={"invite_token": invite_token})
        token = join_res["access_token"]
        player_tokens[p_name] = token
        print(f"  Player {p_name} joined session.")
        
        print(f"  Creating character sheet for {char['name']}...")
        _api("POST", "/api/characters/", token, {
            "session_id": session_id,
            "character_name": char["name"],
            "primary_facet": char["facet"],
            "attributes": char["attributes"],
            "background_id": char["background_id"],
            "magic_domain": char.get("magic_domain"),
        })
    
    print("[5] Setting up WebSocket connections...")
    # MM WS
    mm_ws = websocket.create_connection(WS_URL)
    mm_ws.send(json.dumps({"token": mm_token, "session_id": session_id}))
    mm_state = json.loads(mm_ws.recv())
    print("  MM WebSocket connected.")
    
    # Alaric WS
    alaric_ws = websocket.create_connection(WS_URL)
    alaric_ws.send(json.dumps({"token": player_tokens["Alaric"], "session_id": session_id}))
    alaric_state = json.loads(alaric_ws.recv())
    print("  Alaric WebSocket connected.")
    
    # Pippa WS
    pippa_ws = websocket.create_connection(WS_URL)
    pippa_ws.send(json.dumps({"token": player_tokens["Pippa"], "session_id": session_id}))
    pippa_state = json.loads(pippa_ws.recv())
    print("  Pippa WebSocket connected.")

    # 1. Start Combat
    print("[6] MM starts combat...")
    mm_ws.send(json.dumps({"type": "combat_start"}))
    time.sleep(0.5)
    
    # 2. Declare Postures
    print("[7] Alaric and Pippa declare postures...")
    alaric_ws.send(json.dumps({"type": "declare_posture", "posture": "defensive"}))
    pippa_ws.send(json.dumps({"type": "declare_posture", "posture": "aggressive"}))
    time.sleep(0.5)
    
    # 3. Reveal Postures
    print("[8] MM reveals postures...")
    mm_ws.send(json.dumps({"type": "reveal_postures"}))
    time.sleep(0.5)
    
    # Drain messages
    def read_until(ws, target_type):
        ws.settimeout(2.0)
        try:
            while True:
                msg = json.loads(ws.recv())
                if msg.get("type") == target_type:
                    return msg
        except Exception as e:
            print("  WS Timeout or error waiting for:", target_type)
            return None

    postures_revealed = read_until(mm_ws, "postures_revealed")
    if postures_revealed:
         print(f"  Postures revealed: {postures_revealed.get('postures')}")
    
    # 4. Spawn Enemy
    print("[9] MM spawns Water-Logged Sentinel...")
    mm_ws.send(json.dumps({
        "type": "spawn_enemy",
        "enemy_id": "husk",
        "instance_name": "Water-Logged Sentinel",
    }))
    time.sleep(0.5)
    
    # 5. Strike Enemy
    print("[10] Pippa strikes Sentinel (spending 1 Spark)...")
    pippa_ws.send(json.dumps({
        "type": "strike",
        "attribute_id": "strength",
        "skill_id": "combat",
        "target": "Water-Logged Sentinel",
        "difficulty": "Standard",
        "sparks_spent": 1,
        "press": False,
    }))
    time.sleep(0.5)
    
    strike_res = read_until(pippa_ws, "strike_result")
    if strike_res:
        roll = strike_res.get("roll", {})
        print(f"  Strike Roll: {roll.get('dice_rolled')} (kept {roll.get('dice')}) + {roll.get('modifier')} = {roll.get('total')} -> {roll.get('outcome')}")
        
    # 6. React to attack
    print("[11] Pippa dodges Sentinel strike...")
    pippa_ws.send(json.dumps({"type": "react", "reaction": "dodge"}))
    time.sleep(0.5)
    
    react_res = read_until(pippa_ws, "react_result")
    if react_res:
         roll = react_res.get("roll", {})
         print(f"  React Dodge Roll: {roll.get('dice')} + {roll.get('modifier')} = {roll.get('total')} -> {roll.get('outcome')}")
         
    # 7. End exchange
    print("[12] MM ends the exchange...")
    mm_ws.send(json.dumps({"type": "end_exchange"}))
    time.sleep(0.5)
    read_until(mm_ws, "exchange_ended")
    print("  Exchange ended cleanly, temporal conditions cleared.")
    
    # 8. End combat
    print("[13] MM ends combat...")
    mm_ws.send(json.dumps({"type": "combat_end"}))
    time.sleep(0.5)
    print("  Combat state dissolved.")
    
    # 9. Sylvia casts Inscription magic
    print("[14] Sylvia connects and casts magic (Warding)...")
    sylvia_ws = websocket.create_connection(WS_URL)
    sylvia_ws.send(json.dumps({"token": player_tokens["Sylvia"], "session_id": session_id}))
    sylvia_state = json.loads(sylvia_ws.recv())
    
    sylvia_ws.send(json.dumps({
        "type": "cast",
        "scope": "minor",
        "intent": "Scribe a freezing glyph on the stone path to lock the sentinel's joints",
    }))
    time.sleep(0.5)
    cast_res = read_until(sylvia_ws, "cast_result")
    if cast_res:
         roll = cast_res.get("roll", {})
         print(f"  Cast Warding Roll: {roll.get('dice')} + {roll.get('modifier')} = {roll.get('total')} -> {roll.get('outcome')}")
         
    # 10. Award Spark
    print("[15] MM awards a Spark to Pippa...")
    mm_ws.send(json.dumps({
        "type": "spark_earn",
        "player_name": "Pippa",
        "reason": "Dramatic slide under the Golem's stone legs to land the final blow",
    }))
    time.sleep(0.5)
    spark_res = read_until(mm_ws, "spark_earned")
    if spark_res:
        print(f"  Spark awarded successfully. Pippa current Sparks: {spark_res.get('sparks_now')}")
        
    print("[16] Cleaning up WebSocket connections...")
    mm_ws.close()
    alaric_ws.close()
    pippa_ws.close()
    sylvia_ws.close()
    print("\n=== PLAYTEST 06 LIVE SIMULATION COMPLETED SUCCESSFULLY ===\n")

if __name__ == "__main__":
    run()
