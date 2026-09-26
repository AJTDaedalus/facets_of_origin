"""REST tests for enemy cards and encounters (MM only)."""
import pytest

from app.auth.tokens import create_session_token

CARD = {
    "id": "city_watch_sergeant", "name": "City Watch Sergeant", "level": 3, "role": "standard",
    "armor": 1, "morale": 8, "weapon": "Cudgel", "wants": "An arrest.",
    "special": "BACKUP — two watch arrive.", "when_bloodied": "Defends every exchange.",
    "tells": "Glances up the street.", "breaks": "Surrenders.",
    "twists": ["a", "b", "c", "d", "e", "f"],
}
MOOK = {**CARD, "id": "thug", "name": "Thug", "level": 1, "role": "mook", "armor": 0,
        "when_bloodied": None}


def _add(client, mm_headers, sid, card):
    return client.post("/api/enemies/", json={"session_id": sid, **card}, headers=mm_headers)


# ---------------------------------------------------------------------------
# Card preview
# ---------------------------------------------------------------------------

class TestPreviewCard:
    def test_preview_without_session(self, client, mm_headers):
        resp = client.post("/api/enemies/preview-card", json={"level": 3, "role": "standard"},
                           headers=mm_headers)
        assert resp.status_code == 200
        card = resp.json()["card"]
        assert (card["hp"], card["damage"], card["attack"], card["attacks"]) == (14, 6, 2, 1)

    def test_preview_with_session_and_overrides(self, client, mm_headers, active_session):
        resp = client.post("/api/enemies/preview-card", json={
            "session_id": active_session["session_id"], "level": 2, "role": "boss", "damage": 9,
        }, headers=mm_headers)
        card = resp.json()["card"]
        assert card["hp"] == 55 and card["damage"] == 9 and card["overrides"] == ["damage"]
        assert card["bloodied_phase"] is True

    def test_mook_preview_has_no_hp(self, client, mm_headers):
        card = client.post("/api/enemies/preview-card", json={"level": 1, "role": "mook"},
                           headers=mm_headers).json()["card"]
        assert card["hp"] is None and card["mob"] is True

    def test_bad_role_422(self, client, mm_headers):
        resp = client.post("/api/enemies/preview-card", json={"level": 1, "role": "dragon"},
                           headers=mm_headers)
        assert resp.status_code == 422

    def test_level_out_of_range_422(self, client, mm_headers):
        resp = client.post("/api/enemies/preview-card", json={"level": 11}, headers=mm_headers)
        assert resp.status_code == 422

    def test_unknown_session_404(self, client, mm_headers):
        resp = client.post("/api/enemies/preview-card",
                           json={"session_id": "nope", "level": 1}, headers=mm_headers)
        assert resp.status_code == 404

    def test_requires_mm(self, client, active_session):
        headers = {"Authorization":
                   f"Bearer {create_session_token('P', active_session['session_id'])}"}
        resp = client.post("/api/enemies/preview-card", json={"level": 1}, headers=headers)
        assert resp.status_code in (401, 403)
        assert client.post("/api/enemies/preview-card", json={"level": 1}).status_code in (401, 403)


# ---------------------------------------------------------------------------
# Enemy CRUD
# ---------------------------------------------------------------------------

class TestEnemyCrud:
    def test_create_complete_card(self, client, mm_headers, active_session):
        resp = _add(client, mm_headers, active_session["session_id"], CARD)
        assert resp.status_code == 200, resp.text
        enemy = resp.json()["enemy"]
        assert enemy["card"]["hp"] == 14 and enemy["name"] == "City Watch Sergeant"

    def test_incomplete_card_422(self, client, mm_headers, active_session):
        resp = _add(client, mm_headers, active_session["session_id"],
                    {**CARD, "twists": ["only one"], "special": ""})
        assert resp.status_code == 422
        errors = resp.json()["detail"]["errors"]
        assert any("twists" in e for e in errors) and any("SPECIAL" in e for e in errors)

    def test_non_mook_needs_when_bloodied(self, client, mm_headers, active_session):
        resp = _add(client, mm_headers, active_session["session_id"],
                    {**CARD, "when_bloodied": None})
        assert resp.status_code == 422

    def test_mook_without_when_bloodied_ok(self, client, mm_headers, active_session):
        assert _add(client, mm_headers, active_session["session_id"], MOOK).status_code == 200

    def test_create_unknown_session_404(self, client, mm_headers):
        assert _add(client, mm_headers, "nope", CARD).status_code == 404

    def test_list(self, client, mm_headers, active_session):
        sid = active_session["session_id"]
        _add(client, mm_headers, sid, CARD)
        resp = client.get(f"/api/enemies/{sid}", headers=mm_headers)
        assert resp.status_code == 200
        assert resp.json()["enemies"]["city_watch_sergeant"]["card"]["attack"] == 2

    def test_list_unknown_session_404(self, client, mm_headers):
        assert client.get("/api/enemies/nope", headers=mm_headers).status_code == 404

    def test_delete(self, client, mm_headers, active_session):
        sid = active_session["session_id"]
        _add(client, mm_headers, sid, CARD)
        resp = client.delete(f"/api/enemies/{sid}/city_watch_sergeant", headers=mm_headers)
        assert resp.status_code == 200
        assert client.get(f"/api/enemies/{sid}", headers=mm_headers).json()["enemies"] == {}

    def test_delete_missing_404(self, client, mm_headers, active_session):
        sid = active_session["session_id"]
        assert client.delete(f"/api/enemies/{sid}/ghost", headers=mm_headers).status_code == 404
        assert client.delete("/api/enemies/nope/ghost", headers=mm_headers).status_code == 404

    def test_crud_requires_mm(self, client, active_session):
        sid = active_session["session_id"]
        headers = {"Authorization": f"Bearer {create_session_token('P', sid)}"}
        assert client.post("/api/enemies/", json={"session_id": sid, **CARD},
                           headers=headers).status_code in (401, 403)
        assert client.get(f"/api/enemies/{sid}", headers=headers).status_code in (401, 403)


# ---------------------------------------------------------------------------
# Encounters
# ---------------------------------------------------------------------------

@pytest.fixture
def stocked(client, mm_headers, active_session):
    sid = active_session["session_id"]
    assert _add(client, mm_headers, sid, CARD).status_code == 200
    assert _add(client, mm_headers, sid, MOOK).status_code == 200
    return sid


class TestEncounters:
    def test_create_with_danger_read(self, client, mm_headers, stocked):
        resp = client.post("/api/encounters/", json={
            "session_id": stocked, "id": "street", "name": "Street Brawl",
            "enemies": [{"enemy_id": "thug", "count": 4}],
        }, headers=mm_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["danger"]["points"] == 1.0
        assert data["missing"] == []
        assert data["encounter"]["name"] == "Street Brawl"

    def test_create_reports_missing_foes(self, client, mm_headers, stocked):
        resp = client.post("/api/encounters/", json={
            "session_id": stocked, "id": "x", "name": "X",
            "enemies": [{"enemy_id": "ghost"}]}, headers=mm_headers)
        assert resp.json()["missing"] == ["ghost"]

    def test_create_unknown_session_404(self, client, mm_headers):
        resp = client.post("/api/encounters/", json={"session_id": "nope", "id": "x", "name": "X"},
                           headers=mm_headers)
        assert resp.status_code == 404

    def test_preview_with_party_overrides(self, client, mm_headers, stocked):
        resp = client.post("/api/encounters/preview", json={
            "session_id": stocked, "enemies": [{"enemy_id": "city_watch_sergeant", "count": 2}],
            "party_size": 4, "party_level": 3,
        }, headers=mm_headers)
        assert resp.status_code == 200
        assert resp.json()["danger"]["read"] == "skirmish"     # 2 points vs 4 PCs

    def test_preview_level_gap_scales_points(self, client, mm_headers, stocked):
        near = client.post("/api/encounters/preview", json={
            "session_id": stocked, "enemies": [{"enemy_id": "city_watch_sergeant", "count": 2}],
            "party_size": 4, "party_level": 1,
        }, headers=mm_headers).json()["danger"]
        assert near["points"] == 2.0          # level 3 vs party 1: gap 2, no doubling
        low = client.post("/api/encounters/preview", json={
            "session_id": stocked, "enemies": [{"enemy_id": "thug", "count": 4}],
            "party_size": 4, "party_level": 4,
        }, headers=mm_headers).json()["danger"]
        assert low["points"] == 0.5           # level 1 Mooks vs party 4: halved

    def test_preview_defaults_to_session_party(self, client, mm_headers, stocked):
        resp = client.post("/api/encounters/preview", json={
            "session_id": stocked, "enemies": [{"enemy_id": "city_watch_sergeant", "count": 2}],
        }, headers=mm_headers)
        assert resp.json()["danger"]["read"] == "deadly"       # 2 points vs 1 (empty party)

    def test_preview_unknown_enemy_404(self, client, mm_headers, stocked):
        resp = client.post("/api/encounters/preview", json={
            "session_id": stocked, "enemies": [{"enemy_id": "ghost"}]}, headers=mm_headers)
        assert resp.status_code == 404

    def test_list_and_delete(self, client, mm_headers, stocked):
        client.post("/api/encounters/", json={
            "session_id": stocked, "id": "street", "name": "Street",
            "enemies": [{"enemy_id": "thug", "count": 4}]}, headers=mm_headers)
        listed = client.get(f"/api/encounters/{stocked}", headers=mm_headers).json()
        assert listed["encounters"]["street"]["danger"]["read"] in (
            "skirmish", "fight", "hard", "deadly")
        assert client.delete(f"/api/encounters/{stocked}/street",
                             headers=mm_headers).status_code == 200
        assert client.delete(f"/api/encounters/{stocked}/street",
                             headers=mm_headers).status_code == 404

    def test_list_unknown_session_404(self, client, mm_headers):
        assert client.get("/api/encounters/nope", headers=mm_headers).status_code == 404

    def test_encounters_require_mm(self, client, active_session):
        sid = active_session["session_id"]
        headers = {"Authorization": f"Bearer {create_session_token('P', sid)}"}
        assert client.get(f"/api/encounters/{sid}", headers=headers).status_code in (401, 403)
