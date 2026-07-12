import json
import urllib.request
import urllib.error
import time
import websocket

BASE_URL = "http://127.0.0.1:8010"
WS_URL = "ws://127.0.0.1:8010/ws"
MM_PASSWORD = "testpass123!"
SESSION_ID = "89fdc5c8-5da8-4c13-9ccf-1a055a1559d9"

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
    print("Waiting 10 seconds for rate limit window to clear...")
    time.sleep(10)
    
    print("[1] Logging in as MM...")
    mm_token = None
    for attempt in range(5):
        try:
            mm_token = _api("POST", "/api/sessions/auth/mm-login", body={"password": MM_PASSWORD})["access_token"]
            print("Logged in successfully as MM.")
            break
        except Exception as e:
            print(f"Login attempt {attempt + 1} failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            
    if not mm_token:
        print("Could not login as MM. Exiting.")
        return
        
    print("[2] Getting player token for Thorne...")
    invite = _api("POST", "/api/sessions/invite", mm_token, {"session_id": SESSION_ID, "player_name": "Thorne Woodcroft"})
    invite_token = invite["invite_url"].split("token=")[-1]
    
    join_res = _api("POST", "/api/sessions/join", body={"invite_token": invite_token})
    thorne_token = join_res["access_token"]
    print("Thorne token acquired.")
    
    print("[3] Connecting Thorne to WebSocket...")
    thorne_ws = websocket.create_connection(WS_URL)
    thorne_ws.send(json.dumps({"token": thorne_token, "session_id": SESSION_ID}))
    thorne_ws.recv() # Consume state message
    
    print("[4] Casting Resonance magic (Minor scope)...")
    thorne_ws.send(json.dumps({
        "type": "cast",
        "scope": "minor",
        "intent": "Project a destructive sound wave through the golem's core to shatter internal gears"
    }))
    
    def read_until(ws, target_types):
        ws.settimeout(5.0)
        try:
            while True:
                m = json.loads(ws.recv())
                if m.get("type") in target_types:
                    return m
        except Exception as e:
            return {"type": "error", "message": str(e)}

    cast_msg = read_until(thorne_ws, ("cast_result", "error"))
    print("CAST RESULT FROM SERVER:", json.dumps(cast_msg))
    
    # MM WS connection to clean up combat
    mm_ws = websocket.create_connection(WS_URL)
    mm_ws.send(json.dumps({"token": mm_token, "session_id": SESSION_ID}))
    mm_ws.recv() # Consume state
    
    if cast_msg.get("type") == "cast_result":
        roll = cast_msg.get("roll", {})
        outcome = roll.get("outcome")
        print(f"Resonance Cast Roll Total: {roll.get('total')} -> {outcome}")
        
        if outcome in ("full_success", "partial_success"):
            print("[5] Cast succeeded. Concluding combat...")
            mm_ws.send(json.dumps({"type": "combat_end"}))
            time.sleep(0.2)
            
            print("[6] Awarding Spark to Thorne...")
            mm_ws.send(json.dumps({
                "type": "spark_earn",
                "player_name": "Thorne Woodcroft",
                "reason": "Successfully shattered the golem's core with resonant sound waves"
            }))
            time.sleep(0.2)
            read_until(mm_ws, ("spark_earned",))
            
            print("[7] Awarding Spark to Alaric...")
            mm_ws.send(json.dumps({
                "type": "spark_earn",
                "player_name": "Alaric of the Iron Gate",
                "reason": "Heroic shield interception to absorb the molten heat backlash"
            }))
            time.sleep(0.2)
            read_until(mm_ws, ("spark_earned",))
            print("Combat successfully concluded and Sparks awarded.")
        else:
            print("[5] Cast failed. Golem remains active.")
            
    thorne_ws.close()
    mm_ws.close()
    print("Cleanup complete.")

if __name__ == "__main__":
    run()
