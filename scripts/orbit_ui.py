"""Orbit AI menu for the CyberShield launcher (Option 22).

This is the UI layer. All engine work goes through the middleware at
tools/orbit_ai/nodes.py — this file only prints, reads input, and displays
results. No engine imports here except the middleware itself.
"""

import os
import sys

_BHASA_ROOT = r"C:\BhasaGrid-Project"
if _BHASA_ROOT not in sys.path:
    sys.path.insert(0, _BHASA_ROOT)

try:
    from tools.orbit_ai import nodes as orbit_nodes
    _BRIDGE_ERROR = None
except Exception as e:
    orbit_nodes = None
    _BRIDGE_ERROR = e

from scripts.utils import clear_keyboard_buffer


def _prompt(msg):
    try:
        return input(msg)
    except (KeyboardInterrupt, EOFError):
        return ""


def _need_bridge():
    if orbit_nodes is None:
        print("\n[-] Orbit AI bridge unavailable: %s" % (_BRIDGE_ERROR,))
        print("[!] Check that C:\\BhasaGrid-Project\\tools\\orbit_ai\\nodes.py exists.")
        return False
    return True


def _run_chat():
    st = orbit_nodes.get_status()
    print("\n[*] Chat  | provider=%s model=%s  (type /exit to leave)" % (
        st.get("provider"), st.get("model")))
    while True:
        text = _prompt("\n  You: ").strip()
        if not text:
            continue
        if text.lower() in {"/exit", "/quit", "/q", "exit", "quit"}:
            print("  Leaving chat. History saved by the engine.")
            return
        try:
            res = orbit_nodes.chat_turn(text)
        except ValueError as e:
            print("  [!] %s" % e)
            continue
        except RuntimeError as e:
            print("  [!] Engine failure: %s" % e)
            continue
        print("\n  Orbit AI:\n  %s" % orbit_nodes.mask(res["reply"])[:4000])


def _run_conversations():
    menu = (
        "\n  -- Conversation management --\n"
        "  [1] List past conversations\n"
        "  [2] View a conversation\n"
        "  [3] Export a conversation\n"
        "  [4] Delete a conversation\n"
        "  [5] Clear current history\n"
        "  [B] Back\n"
    )
    while True:
        print(menu)
        clear_keyboard_buffer()
        choice = _prompt("  orbit/conversations > ").strip().lower()
        if choice == "1":
            try:
                sessions = orbit_nodes.list_conversations()
            except (ValueError, RuntimeError) as e:
                print("  [!] %s" % e)
                continue
            if not sessions:
                print("  (no saved conversations yet)")
            for i, s in enumerate(sessions, 1):
                print("  [%d] %s  %s  %s/%s  (%d msgs)" % (
                    i, s["session_id"], s["timestamp"],
                    s["provider"], s["model"], s["messages"]))
        elif choice in {"2", "3", "4"}:
            try:
                sessions = orbit_nodes.list_conversations()
            except (ValueError, RuntimeError) as e:
                print("  [!] %s" % e)
                continue
            if not sessions:
                print("  (no saved conversations yet)")
                continue
            for i, s in enumerate(sessions, 1):
                print("  [%d] %s  %s  (%d msgs)" % (
                    i, s["session_id"], s["timestamp"], s["messages"]))
            pick = _prompt("  Select 1-%d (Enter=cancel): " % len(sessions)).strip()
            if not pick or not pick.isdigit() or not (1 <= int(pick) <= len(sessions)):
                if pick:
                    print("  [!] Invalid selection.")
                continue
            name = sessions[int(pick) - 1]["name"]
            if choice == "2":
                try:
                    data = orbit_nodes.get_conversation(name)
                except (ValueError, RuntimeError) as e:
                    print("  [!] %s" % e)
                    continue
                hist = data.get("history", [])
                print("\n  -- %s [%s/%s] --" % (
                    data.get("session_id", name),
                    data.get("provider", "?"), data.get("model", "?")))
                shown = 0
                for msg in hist[-200:]:
                    if not isinstance(msg, dict):
                        continue
                    role = "You" if msg.get("role") == "user" else "Orbit AI"
                    print("\n  %s:\n  %s" % (role, orbit_nodes.mask(msg.get("content", ""))[:2000]))
                    shown += 1
                if data.get("omitted"):
                    print("\n  ... (%d older messages omitted)" % data["omitted"])
                print("\n  -- end (%d shown) --" % shown)
            elif choice == "3":
                try:
                    dest = orbit_nodes.export_conversation(name)
                    print("  Exported -> %s" % dest)
                except (ValueError, RuntimeError) as e:
                    print("  [!] %s" % e)
            else:
                confirm = _prompt("  Permanently delete '%s'? Type DELETE to confirm: " % name).strip()
                try:
                    orbit_nodes.delete_conversation(name, confirm)
                    print("  Deleted '%s'." % name)
                except (ValueError, RuntimeError) as e:
                    print("  [!] %s" % e)
        elif choice == "5":
            confirm = _prompt("  Clear current history? (y/N): ").strip().lower()
            if confirm != "y":
                print("  Cancelled.")
                continue
            try:
                orbit_nodes.clear_history()
                print("  History cleared.")
            except (ValueError, RuntimeError) as e:
                print("  [!] %s" % e)
        elif choice in {"b", "back", "q", "quit", "exit", ""}:
            return
        else:
            print("  [!] Choose 1-5 or B.")


def _run_test_connection():
    try:
        results = orbit_nodes.test_connection()
    except (ValueError, RuntimeError) as e:
        print("  [!] %s" % e)
        return
    print("\n  -- Connection test (offline-safe, no quota spent) --")
    for provider, r in results.items():
        status = "READY" if (r["available"] and r["rate_ok"]) else "BLOCKED"
        print("  [%s] %-8s key=%s  rate=%s" % (
            status, provider, r["key"],
            "ok" if r["rate_ok"] else r["rate_msg"][:70]))
    blocked = [p for p, r in results.items() if not (r["available"] and r["rate_ok"])]
    if blocked:
        print("  Note: %s unavailable/limited - chat auto-fallbacks per engine priority."
              % ", ".join(blocked))
    extra = _prompt("  Send one live probe message? (costs quota) (y/N): ").strip().lower()
    if extra != "y":
        return
    try:
        live = orbit_nodes.test_connection(live=True)
    except (ValueError, RuntimeError) as e:
        print("  [!] %s" % e)
        return
    for provider, r in live.items():
        print("  live %-8s : %s" % (provider, r["live"]))


def run_orbit_menu():
    """Entry point used by launcher Option 22. Returns when user goes Back."""
    if not _need_bridge():
        _prompt("\nPress ENTER to return to menu...")
        return
    try:
        st = orbit_nodes.get_status()
        print("\n[*] Orbit AI Nodes  | provider=%s model=%s rich_ui=%s saved=%s" % (
            st.get("provider"), st.get("model"), st.get("rich_ui"),
            st.get("saved_conversations")))
    except (ValueError, RuntimeError) as e:
        print("\n[-] Orbit engine failed to start: %s" % e)
        _prompt("\nPress ENTER to return to menu...")
        return
    menu = (
        "\n  [1] Start a chat\n"
        "  [2] Conversation management\n"
        "  [3] Test connection\n"
        "  [Q] Back\n"
    )
    while True:
        print(menu)
        clear_keyboard_buffer()
        choice = _prompt("  orbit > ").strip().lower()
        if choice == "1":
            _run_chat()
        elif choice == "2":
            _run_conversations()
        elif choice == "3":
            _run_test_connection()
        elif choice in {"q", "quit", "exit", "b", "back", ""}:
            print("  Leaving Orbit AI Nodes.")
            return
        else:
            print("  [!] Choose 1, 2, 3 or Q.")
