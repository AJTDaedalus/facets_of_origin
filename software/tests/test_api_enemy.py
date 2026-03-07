"""API tests for enemy and encounter CRUD endpoints."""
import pytest

from app.auth.tokens import create_mm_token, create_session_token


# ---------------------------------------------------------------------------
# Enemy API
# ---------------------------------------------------------------------------

class TestEnemyAPI:
    def test_create_enemy_requires_mm(self, client, active_session):
        player_token = create_session_token("Alice", active_session["session_id"])
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/enemies/", json={
            "session_id": active_session["session_id"],
            "id": "thug", "name": "Thug",
        }, headers=headers)
        assert resp.status_code == 403

    def test_create_enemy_success(self, client, mm_headers, active_session):
        resp = client.post("/api/enemies/", json={
            "session_id": active_session["session_id"],
            "id": "harbor_thug",
            "name": "Harbor Thug",
            "tier": "mook",
            "attack_modifier": 0,
            "description": "A hired thug.",
        }, headers=mm_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["enemy"]["name"] == "Harbor Thug"
        assert data["tr"] >= 1

    def test_create_named_enemy_with_tr(self, client, mm_headers, active_session):
        resp = client.post("/api/enemies/", json={
            "session_id": active_session["session_id"],
            "id": "sergeant",
            "name": "City Watch Sergeant",
            "tier": "named",
            "endurance": 6,
            "attack_modifier": 2,
            "defense_modifier": 2,
            "armor": "light",
        }, headers=mm_headers)
        assert resp.status_code == 200
        assert resp.json()["tr"] == 8

    def test_list_enemies(self, client, mm_headers, active_session):
        # Create two enemies
        sid = active_session["session_id"]
        client.post("/api/enemies/", json={
            "session_id": sid, "id": "thug1", "name": "Thug A",
        }, headers=mm_headers)
        client.post("/api/enemies/", json={
            "session_id": sid, "id": "thug2", "name": "Thug B",
        }, headers=mm_headers)
        resp = client.get(f"/api/enemies/{sid}", headers=mm_headers)
        assert resp.status_code == 200
        assert "thug1" in resp.json()["enemies"]
        assert "thug2" in resp.json()["enemies"]

    def test_delete_enemy(self, client, mm_headers, active_session):
        sid = active_session["session_id"]
        client.post("/api/enemies/", json={
            "session_id": sid, "id": "to_delete", "name": "Delete Me",
        }, headers=mm_headers)
        resp = client.delete(f"/api/enemies/{sid}/to_delete", headers=mm_headers)
        assert resp.status_code == 200
        assert resp.json()["deleted"] == "to_delete"
        # Verify gone
        resp = client.get(f"/api/enemies/{sid}", headers=mm_headers)
        assert "to_delete" not in resp.json()["enemies"]

    def test_delete_nonexistent_enemy_returns_404(self, client, mm_headers, active_session):
        resp = client.delete(
            f"/api/enemies/{active_session['session_id']}/nope",
            headers=mm_headers,
        )
        assert resp.status_code == 404

    def test_create_enemy_session_not_found(self, client, mm_headers):
        resp = client.post("/api/enemies/", json={
            "session_id": "no-such-session", "id": "thug", "name": "Thug",
        }, headers=mm_headers)
        assert resp.status_code == 404

    def test_enemy_with_tactics_and_personality(self, client, mm_headers, active_session):
        resp = client.post("/api/enemies/", json={
            "session_id": active_session["session_id"],
            "id": "boss",
            "name": "Archive Guardian",
            "tier": "boss",
            "endurance": 10,
            "attack_modifier": 3,
            "tactics": "Fights defensively at first.",
            "personality": "Not malevolent. Patient.",
            "loot": ["Guardian Core", "Ancient Key"],
        }, headers=mm_headers)
        assert resp.status_code == 200
        data = resp.json()["enemy"]
        assert data["tactics"] == "Fights defensively at first."
        assert data["loot"] == ["Guardian Core", "Ancient Key"]


# ---------------------------------------------------------------------------
# Encounter API
# ---------------------------------------------------------------------------

class TestEncounterAPI:
    def test_create_encounter_requires_mm(self, client, active_session):
        player_token = create_session_token("Alice", active_session["session_id"])
        headers = {"Authorization": f"Bearer {player_token}"}
        resp = client.post("/api/encounters/", json={
            "session_id": active_session["session_id"],
            "id": "fight", "name": "Fight",
        }, headers=headers)
        assert resp.status_code == 403

    def test_create_encounter_success(self, client, mm_headers, active_session):
        sid = active_session["session_id"]
        # First create an enemy
        client.post("/api/enemies/", json={
            "session_id": sid, "id": "thug", "name": "Thug", "tier": "mook",
        }, headers=mm_headers)
        # Create encounter
        resp = client.post("/api/encounters/", json={
            "session_id": sid,
            "id": "tavern-brawl",
            "name": "Tavern Brawl",
            "difficulty": "standard",
            "enemies": [{"enemy_id": "thug", "count": 4}],
            "lateral_solutions": ["Bribe the bartender"],
            "rewards_sparks": 1,
        }, headers=mm_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["encounter"]["name"] == "Tavern Brawl"
        assert data["effective_tr"] > 0

    def test_list_encounters(self, client, mm_headers, active_session):
        sid = active_session["session_id"]
        client.post("/api/encounters/", json={
            "session_id": sid, "id": "enc1", "name": "Encounter 1",
        }, headers=mm_headers)
        resp = client.get(f"/api/encounters/{sid}", headers=mm_headers)
        assert resp.status_code == 200
        assert "enc1" in resp.json()["encounters"]

    def test_delete_encounter(self, client, mm_headers, active_session):
        sid = active_session["session_id"]
        client.post("/api/encounters/", json={
            "session_id": sid, "id": "to_delete", "name": "Delete Me",
        }, headers=mm_headers)
        resp = client.delete(f"/api/encounters/{sid}/to_delete", headers=mm_headers)
        assert resp.status_code == 200

    def test_create_encounter_session_not_found(self, client, mm_headers):
        resp = client.post("/api/encounters/", json={
            "session_id": "no-such-session", "id": "enc", "name": "Enc",
        }, headers=mm_headers)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Character notes/inventory API
# ---------------------------------------------------------------------------

class TestCharacterNotesAPI:
    def test_player_updates_own_notes(self, client, session_with_character):
        session, char = session_with_character
        sid = session["session_id"]
        pname = char["player_name"]
        token = create_session_token(pname, sid)
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.put(
            f"/api/characters/{sid}/{pname}/notes",
            json={"notes_player": "My notes"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["notes_player"] == "My notes"

    def test_player_cannot_set_mm_notes(self, client, session_with_character):
        session, char = session_with_character
        sid = session["session_id"]
        pname = char["player_name"]
        token = create_session_token(pname, sid)
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.put(
            f"/api/characters/{sid}/{pname}/notes",
            json={"notes_mm": "Secret info"},
            headers=headers,
        )
        assert resp.status_code == 403

    def test_mm_updates_both_notes(self, client, mm_headers, session_with_character):
        session, char = session_with_character
        sid = session["session_id"]
        pname = char["player_name"]
        resp = client.put(
            f"/api/characters/{sid}/{pname}/notes",
            json={"notes_player": "Player note", "notes_mm": "MM secret"},
            headers=mm_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["notes_player"] == "Player note"
        assert resp.json()["notes_mm"] == "MM secret"

    def test_notes_character_not_found(self, client, mm_headers, active_session):
        resp = client.put(
            f"/api/characters/{active_session['session_id']}/Nobody/notes",
            json={"notes_player": "test"},
            headers=mm_headers,
        )
        assert resp.status_code == 404

    def test_player_cannot_update_other_player_notes(self, client, session_with_character):
        session, char = session_with_character
        sid = session["session_id"]
        pname = char["player_name"]
        token = create_session_token("SomeOtherPlayer", sid)
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.put(
            f"/api/characters/{sid}/{pname}/notes",
            json={"notes_player": "Hacked"},
            headers=headers,
        )
        assert resp.status_code == 403


class TestCharacterInventoryAPI:
    def test_player_updates_own_inventory(self, client, session_with_character):
        session, char = session_with_character
        sid = session["session_id"]
        pname = char["player_name"]
        token = create_session_token(pname, sid)
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.put(
            f"/api/characters/{sid}/{pname}/inventory",
            json={"inventory": ["Sword", "Shield", "Rope"]},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["inventory"] == ["Sword", "Shield", "Rope"]

    def test_mm_updates_any_inventory(self, client, mm_headers, session_with_character):
        session, char = session_with_character
        sid = session["session_id"]
        pname = char["player_name"]
        resp = client.put(
            f"/api/characters/{sid}/{pname}/inventory",
            json={"inventory": ["Magic Ring"]},
            headers=mm_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["inventory"] == ["Magic Ring"]

    def test_inventory_character_not_found(self, client, mm_headers, active_session):
        resp = client.put(
            f"/api/characters/{active_session['session_id']}/Nobody/inventory",
            json={"inventory": []},
            headers=mm_headers,
        )
        assert resp.status_code == 404

    def test_player_cannot_update_other_inventory(self, client, session_with_character):
        session, char = session_with_character
        sid = session["session_id"]
        pname = char["player_name"]
        token = create_session_token("OtherPlayer", sid)
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.put(
            f"/api/characters/{sid}/{pname}/inventory",
            json={"inventory": ["Stolen Goods"]},
            headers=headers,
        )
        assert resp.status_code == 403
