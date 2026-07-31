"""ARCHIVED AND DEFECTIVE — do not run, do not copy.

This is the script that produced playtest batch 07. It is kept here, beside the
data it generated, for provenance only. It was moved out of software/tools/ on
2026-07-31 so it cannot be reused.

Two defects, both documented with evidence in docs/DESIGN_agentic_playtests.md §1:

1.  Roll results are over-counted 4x. Each player's roll is sent, then read back
    with `read_until(ws, "roll_result")` on THAT PLAYER'S socket -- but
    `roll_result` is broadcast to every connected client, so all four sockets
    receive and report the same first broadcast. Every session in dice_rolls.txt
    shows four identical totals as a result.

2.  It makes no decisions. Actions are selected by session index
    (`if idx in (11, 16): everyone rolls persuade`), so nothing here is a
    playtest of play -- only of the engine's arithmetic.

Separately, the narrative session logs in this directory were written alongside
this script rather than generated from it, and their dice are confabulated.

The replacement is software/tools/agentic_playtest/, specified in
docs/DESIGN_agentic_playtests.md. It renders transcripts from the engine's own
event log so prose and mechanics cannot diverge, and ships validators
(validate.py) whose regression tests are drawn from this batch's output.
"""

import json
import urllib.request
import urllib.error
import time
import websocket
import random
import subprocess
import os
import sys

BASE_URL = "http://127.0.0.1:8010"
WS_URL = "ws://127.0.0.1:8010/ws"
MM_PASSWORD = "testpass123!"
PLAYTEST_DIR = "Z:/root/facets_of_origin/playtest/07_oraga_night_playtests"

PLAYERS = {
    "Serane": {
        "name": "Serane Vaskarin",
        "facet": "mind",
        "bg": "guild_apprentice",
        "attrs": {"strength": 1, "dexterity": 2, "constitution": 1, "intelligence": 3, "wisdom": 2, "knowledge": 2, "spirit": 2, "luck": 2, "charisma": 3},
        "domain": "warding"
    },
    "Pello": {
        "name": "Pello the Phern",
        "facet": "body",
        "bg": "arena_fighter",
        "attrs": {"strength": 1, "dexterity": 3, "constitution": 1, "intelligence": 2, "wisdom": 3, "knowledge": 2, "spirit": 1, "luck": 3, "charisma": 2}
    },
    "Dassa": {
        "name": "Dassa the Ungifted",
        "facet": "body",
        "bg": "city_watch_veteran",
        "attrs": {"strength": 3, "dexterity": 2, "constitution": 3, "intelligence": 1, "wisdom": 2, "knowledge": 2, "spirit": 1, "luck": 2, "charisma": 2}
    },
    "Ilesse": {
        "name": "Ilesse Kethaun",
        "facet": "soul",
        "bg": "temple_acolyte",
        "attrs": {"strength": 1, "dexterity": 2, "constitution": 1, "intelligence": 2, "wisdom": 3, "knowledge": 2, "spirit": 2, "luck": 2, "charisma": 3},
        "domain": "resonance"
    }
}

TAVVA_DATA = {
    "name": "Tavva",
    "tier": "named",
    "resolve": 3,
    "attack_modifier": 2,
    "defense_modifier": 2,
    "armor": "light"
}

KNIFE_DATA = {
    "name": "Gallery Knife",
    "tier": "mook",
    "resolve": 0,
    "attack_modifier": 1,
    "defense_modifier": 1,
    "armor": "none"
}

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
        raise AssertionError(f"{method} {path} -> {e.code}: {detail}") from e

def read_until(ws_conn, target_type, timeout=2.0):
    ws_conn.settimeout(timeout)
    try:
        while True:
            m = json.loads(ws_conn.recv())
            if m.get("type") == target_type:
                return m
    except Exception as e:
        return None

def start_server():
    print("Starting FastAPI game server...")
    proc = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd="Z:/root/facets_of_origin/software",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(3)
    return proc

def setup_mm():
    print("Configuring MM password...")
    try:
        _api("POST", "/api/sessions/auth/setup", body={"password": MM_PASSWORD})
    except Exception as e:
        print("Password setup already done or skipped:", e)

def main():
    server_process = start_server()
    try:
        setup_mm()
        mm_token = _api("POST", "/api/sessions/auth/mm-login", body={"password": MM_PASSWORD})["access_token"]
        
        results = []
        dice_rolls_log = []
        
        for idx in range(11, 21):
            mm_name = "Arthur" if idx <= 15 else "Cyrus"
            session_name = f"Playtest {idx:02d} (MM: {mm_name})"
            print(f"\n--- Running {session_name} ---")
            
            # Create session
            session_id = _api("POST", "/api/sessions/", mm_token, {"name": session_name, "active_facet_ids": ["base"]})["session_id"]
            
            # Invite & Join players
            player_tokens = {}
            for p_name, p_config in PLAYERS.items():
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
                ws.recv()
                player_ws_list[p_name] = ws
                
            mm_ws = websocket.create_connection(WS_URL)
            mm_ws.send(json.dumps({"token": mm_token, "session_id": session_id}))
            mm_ws.recv()
            
            rolls_in_session = []
            
            # Simulate Round 2 actions
            if idx in (11, 16): # Undercover stewards / networking
                for p_name, ws in player_ws_list.items():
                    ws.send(json.dumps({
                        "type": "roll",
                        "attribute_id": "dexterity" if p_name == "Pello" else "wisdom",
                        "skill_id": "persuade",
                        "difficulty": "Standard",
                        "sparks_spent": 1 if idx == 16 else 0
                    }))
                    time.sleep(0.1)
                    res = read_until(ws, "roll_result")
                    if res:
                        roll_info = res["roll"]
                        rolls_in_session.append({
                            "player": p_name,
                            "action": "stealth_networking",
                            "total": roll_info["total"],
                            "outcome": roll_info["outcome"]
                        })
                        
            elif idx in (12, 17): # Scout in the corridor
                for p_name, ws in player_ws_list.items():
                    ws.send(json.dumps({
                        "type": "roll",
                        "attribute_id": "wisdom",
                        "skill_id": "persuade",
                        "difficulty": "Hard" if idx == 12 else "Standard",
                        "sparks_spent": 0
                    }))
                    time.sleep(0.1)
                    res = read_until(ws, "roll_result")
                    if res:
                        roll_info = res["roll"]
                        rolls_in_session.append({
                            "player": p_name,
                            "action": "scout_confrontation",
                            "total": roll_info["total"],
                            "outcome": roll_info["outcome"]
                        })
                        
            elif idx in (13, 18): # Sighting the looters
                for p_name, ws in player_ws_list.items():
                    ws.send(json.dumps({
                        "type": "roll",
                        "attribute_id": "intelligence",
                        "skill_id": "persuade" if p_name == "Serane" else "combat",
                        "difficulty": "Hard",
                        "sparks_spent": 1 if idx == 18 else 0
                    }))
                    time.sleep(0.1)
                    res = read_until(ws, "roll_result")
                    if res:
                        roll_info = res["roll"]
                        rolls_in_session.append({
                            "player": p_name,
                            "action": "looter_detection",
                            "total": roll_info["total"],
                            "outcome": roll_info["outcome"]
                        })
                        
            elif idx in (14, 19): # Chaos at the Gates / Looters in Ballroom
                mm_ws.send(json.dumps({"type": "combat_start"}))
                time.sleep(0.1)
                
                player_ws_list["Dassa"].send(json.dumps({"type": "declare_posture", "posture": "defensive"}))
                player_ws_list["Pello"].send(json.dumps({"type": "declare_posture", "posture": "aggressive" if idx == 19 else "measured"}))
                time.sleep(0.1)
                mm_ws.send(json.dumps({"type": "reveal_postures"}))
                time.sleep(0.1)
                
                # Spawn Gallery Knives
                mm_ws.send(json.dumps({
                    "type": "spawn_enemy",
                    "enemy_id": "gallery_knife",
                    "instance_name": "Gallery Knife 1",
                    "enemy_data": KNIFE_DATA
                }))
                time.sleep(0.1)
                
                for p_name, ws in player_ws_list.items():
                    if p_name in ("Dassa", "Pello"):
                        ws.send(json.dumps({
                            "type": "strike",
                            "attribute_id": "strength" if p_name == "Dassa" else "dexterity",
                            "skill_id": "combat",
                            "target": "Gallery Knife 1",
                            "difficulty": "Standard",
                            "sparks_spent": 1 if idx == 19 else 0
                        }))
                        time.sleep(0.1)
                        res = read_until(ws, "strike_result")
                        if res:
                            roll_info = res["roll"]
                            rolls_in_session.append({
                                "player": p_name,
                                "action": "strike_mook",
                                "total": roll_info["total"],
                                "outcome": roll_info["outcome"]
                            })
                            
                mm_ws.send(json.dumps({"type": "end_exchange"}))
                time.sleep(0.1)
                mm_ws.send(json.dumps({"type": "combat_end"}))
                time.sleep(0.1)
                
            elif idx in (15, 20): # Confrontation in Gallery (Cornering Tavva)
                mm_ws.send(json.dumps({"type": "combat_start"}))
                time.sleep(0.1)
                
                # Spawn Tavva
                mm_ws.send(json.dumps({
                    "type": "spawn_enemy",
                    "enemy_id": "tavva",
                    "instance_name": "Tavva",
                    "enemy_data": TAVVA_DATA
                }))
                time.sleep(0.1)
                
                player_ws_list["Dassa"].send(json.dumps({"type": "declare_posture", "posture": "defensive"}))
                player_ws_list["Pello"].send(json.dumps({"type": "declare_posture", "posture": "measured"}))
                time.sleep(0.1)
                mm_ws.send(json.dumps({"type": "reveal_postures"}))
                time.sleep(0.1)
                
                # Strike Tavva
                for p_name, ws in player_ws_list.items():
                    if p_name in ("Dassa", "Pello"):
                        ws.send(json.dumps({
                            "type": "strike",
                            "attribute_id": "strength" if p_name == "Dassa" else "dexterity",
                            "skill_id": "combat",
                            "target": "Tavva",
                            "difficulty": "Standard",
                            "sparks_spent": 1 if idx == 20 else 0
                        }))
                        time.sleep(0.1)
                        res = read_until(ws, "strike_result")
                        if res:
                            roll_info = res["roll"]
                            rolls_in_session.append({
                                "player": p_name,
                                "action": "strike_tavva",
                                "total": roll_info["total"],
                                "outcome": roll_info["outcome"]
                            })
                            
                # React to Tavva's escape/attack
                for p_name, ws in player_ws_list.items():
                    if p_name in ("Dassa", "Pello"):
                        ws.send(json.dumps({
                            "type": "react",
                            "reaction": "dodge" if p_name == "Pello" else "parry",
                            "difficulty": "Standard"
                        }))
                        time.sleep(0.1)
                        res = read_until(ws, "react_result")
                        if res and res.get("roll"):
                            roll_info = res["roll"]
                            rolls_in_session.append({
                                "player": p_name,
                                "action": "react_tavva",
                                "total": roll_info["total"],
                                "outcome": roll_info["outcome"]
                            })
                            
                mm_ws.send(json.dumps({"type": "end_exchange"}))
                time.sleep(0.1)
                mm_ws.send(json.dumps({"type": "combat_end"}))
                time.sleep(0.1)
                
            success_count = sum(1 for r in rolls_in_session if r["outcome"] == "full_success")
            partial_count = sum(1 for r in rolls_in_session if r["outcome"] == "partial_success")
            failure_count = sum(1 for r in rolls_in_session if r["outcome"] == "failure")
            
            results.append({
                "playtest_index": idx,
                "mm": mm_name,
                "successes": success_count,
                "partials": partial_count,
                "failures": failure_count,
                "rolls": rolls_in_session
            })
            
            for r in rolls_in_session:
                dice_rolls_log.append(f"Session {idx:02d} ({mm_name} MM) | Player: {r['player']} | Action: {r['action']} | Total: {r['total']} -> {r['outcome']}")
                
            for ws in player_ws_list.values():
                ws.close()
            mm_ws.close()
            print(f"Playtest {idx:02d} finished. Success: {success_count}, Partial: {partial_count}, Failure: {failure_count}")
            
        # Read old results and merge
        old_results = []
        try:
            with open(f"{PLAYTEST_DIR}/batch_results.json", "r") as f:
                old_results = json.load(f)
        except Exception:
            pass
            
        combined_results = old_results + results
        with open(f"{PLAYTEST_DIR}/batch_results.json", "w") as f:
            json.dump(combined_results, f, indent=2)
            
        # Append to old dice rolls
        old_rolls = ""
        try:
            with open(f"{PLAYTEST_DIR}/dice_rolls.txt", "r") as f:
                old_rolls = f.read()
        except Exception:
            pass
            
        combined_rolls = old_rolls + "\n".join(dice_rolls_log) + "\n"
        with open(f"{PLAYTEST_DIR}/dice_rolls.txt", "w") as f:
            f.write(combined_rolls)
            
        print("\nAll Round 2 playtests completed successfully.")
        print(f"Updated batch_results.json and appended to dice_rolls.txt in {PLAYTEST_DIR}")
        
    finally:
        print("Terminating server process...")
        server_process.terminate()
        server_process.wait()
        print("Server process shut down.")

if __name__ == "__main__":
    main()
