"""Octa Partner Network — Supabase database layer."""
import streamlit as st
from supabase import create_client, Client
from datetime import datetime


@st.cache_resource
def _client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


def db() -> Client:
    return _client()


# ── Partners ──────────────────────────────────────────────────────────────────

def get_all_partners() -> list:
    try:
        resp = db().table("partners").select("*").order("full_name").execute()
        return resp.data or []
    except Exception:
        return []


def get_partner_by_id(pid: int) -> dict | None:
    try:
        resp = db().table("partners").select("*").eq("id", pid).execute()
        return resp.data[0] if resp.data else None
    except Exception:
        return None


def upsert_partner(data: dict) -> tuple:
    """Insert or update a partner. Returns (ok, id|error)."""
    try:
        data["updated_at"] = datetime.now().isoformat()
        if data.get("id"):
            pid = data.pop("id")
            db().table("partners").update(data).eq("id", pid).execute()
            return True, pid
        else:
            resp = db().table("partners").insert(data).execute()
            new_id = resp.data[0]["id"] if resp.data else None
            return True, new_id
    except Exception as e:
        return False, str(e)


def delete_partner(pid: int) -> tuple:
    try:
        db().table("partners").delete().eq("id", pid).execute()
        return True, "Deleted."
    except Exception as e:
        return False, str(e)


# ── Contacts ──────────────────────────────────────────────────────────────────

def get_contacts(partner_id: int) -> list:
    try:
        resp = db().table("partner_contacts").select("*") \
                   .eq("partner_id", partner_id) \
                   .order("last_name").execute()
        return resp.data or []
    except Exception:
        return []


def upsert_contact(data: dict) -> tuple:
    try:
        data["updated_at"] = datetime.now().isoformat()
        if data.get("id"):
            cid = data.pop("id")
            db().table("partner_contacts").update(data).eq("id", cid).execute()
            return True, cid
        else:
            resp = db().table("partner_contacts").insert(data).execute()
            new_id = resp.data[0]["id"] if resp.data else None
            return True, new_id
    except Exception as e:
        return False, str(e)


def delete_contact(cid: int) -> tuple:
    try:
        db().table("partner_contacts").delete().eq("id", cid).execute()
        return True, "Deleted."
    except Exception as e:
        return False, str(e)


# ── Proposals (read-only, for map color logic) ────────────────────────────────

def get_proposals_for_map() -> list:
    """Return proposal_id, status, partners_list, coordinator for map logic."""
    try:
        resp = db().table("proposals").select(
            "proposal_id,status,partners_list,coordinator,associates_list"
        ).execute()
        return resp.data or []
    except Exception:
        return []
