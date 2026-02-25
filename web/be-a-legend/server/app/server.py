import asyncio
import pickle
from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

class Stats:
    def __init__(self, hp, atk):
        self.hp = hp
        self.atk = atk

class Player:
    def __init__(self):
        self.stats = Stats(100, 10)

class Dragon:
    def __init__(self):
        self.stats = Stats(1000, 999)

class GameState:
    def __init__(self):
        self.player = Player()
        self.dragon = Dragon()
        self.last_save = None
        self.combat_task = None
        self.is_dead = False
        self.is_win = False # Need this to make people "happy," whatever that means.
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state['last_save'] = None
        state['combat_task'] = None
        return state

game_states = {}

def get_game_state(connection_id):
    if connection_id not in game_states:
        game_states[connection_id] = GameState()
    return game_states[connection_id]

async def fight_loop(ws, connection_id):
    state = get_game_state(connection_id)
    player = state.player
    dragon = state.dragon

    try:
        while True:
            await asyncio.sleep(0.3)
            # Exit game conditions
            if state.is_dead or state.is_win:
                # I doubt the player will win, lets just reuse this frontend signal instead.
                ws.send("You have died. Game Over.")
                ws.send("PLAYER_DIED")  # Signal to frontend
                break

            damage = min(player.stats.atk, 50)
            dragon.stats.hp -= damage
            ws.send(f"You hit the dragon for {damage} damage. Dragon HP: {dragon.stats.hp:,}")

            await asyncio.sleep(0.3) # Cool turn based combat

            player.stats.hp -= dragon.stats.atk
            ws.send(f"The dragon hits you for {dragon.stats.atk:,} damage. Your HP: {player.stats.hp}")

            # Check and set our exit conditions
            if player.stats.hp <= 0:
                state.is_dead = True
            
            # Wincon
            if dragon.stats.hp <= 0:
                state.is_win = True
                ws.send(
                    "The dragon collapses in defeat!\n\n"
                    "FLAG: bkctf{s4v3_5cumm1ng_but_c001}\n\n"
                    "Congratulations, brave warrior!"
                )

    except Exception as e:
        ws.send(f"Combat error: {str(e)}")

async def save_game(connection_id):
    state = get_game_state(connection_id)
    state.last_save = pickle.dumps(state)

async def load_game(connection_id):
    state = get_game_state(connection_id)
    if state.last_save is None:
        return False

    loaded_state = pickle.loads(state.last_save)
    
    # Preserve last_save and combat_task before updating
    saved_last_save = state.last_save
    saved_combat_task = state.combat_task
    
    state.__dict__.update(loaded_state.__dict__)    
    state.last_save = saved_last_save
    state.combat_task = saved_combat_task
    
    return True

@sock.route("/ws")
def ws_handler(ws):
    connection_id = id(ws)
    state = get_game_state(connection_id)

    ws.send(
        "Connected to Dragon's Lair\n"
        "Commands: STATS, FIGHT, SAVE, LOAD, RESET, QUIT\n"
        "Player! Defeat the evil dragon to be a legend and claim the legendary flag!")

    try:
        while True:
            msg = ws.receive()
            
            if msg is None:
                break

            command = msg.strip().upper()

            if command == "STATS":
                ws.send(
                    f"Current Stats:\n"
                    f"   Player HP: {state.player.stats.hp} | ATK: {state.player.stats.atk}\n"
                    f"   Dragon HP: {state.dragon.stats.hp:,} | ATK: {state.dragon.stats.atk:,}"
                )

            elif command == "FIGHT":
                if state.is_dead:
                    ws.send("You are dead! Use RESET to try again.")
                elif state.combat_task is None or (hasattr(state.combat_task, 'is_alive') and not state.combat_task.is_alive()):
                    ws.send("You engage the dragon in combat!")
                    
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    import threading
                    def run_combat():
                        asyncio.run(fight_loop(ws, connection_id))
                    
                    combat_thread = threading.Thread(target=run_combat, daemon=True)
                    combat_thread.start()
                    state.combat_task = combat_thread
                    
                else:
                    ws.send("You're already in combat!")

            elif command == "SAVE":
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                loop.run_until_complete(save_game(connection_id))
                ws.send("Game saved.")

            elif command == "LOAD":
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                success = loop.run_until_complete(load_game(connection_id))
                if success:
                    ws.send("Game loaded.")
                else:
                    ws.send("No save file found.")

            elif command == "RESET":
                # Only allow reset if player is dead
                if not state.is_dead:
                    ws.send("You cannot reset while still alive! Fight on!")
                else:
                    state.player = Player()
                    state.dragon = Dragon()
                    state.last_save = None
                    state.is_dead = False
                    state.is_win = False
                    state.combat_task = None
                    ws.send("CLEAR_TERMINAL")
                    ws.send("Game reset to initial state.")
                    ws.send("GAME_RESET")

            elif command == "QUIT":
                ws.send("Goodbye, COWARD!")
                break

            else:
                ws.send(f"Unknown command: {msg}")

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if connection_id in game_states:
            del game_states[connection_id]

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    print("Be a Legend")
    print("Server starting on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)