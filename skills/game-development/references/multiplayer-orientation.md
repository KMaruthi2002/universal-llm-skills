# Multiplayer orientation

Read this before committing to multiplayer. Multiplayer is not a feature added to a single-player game; it changes the architecture of state, timing, input and testing, and it brings ongoing server costs and moderation duties. Decide early, because retrofitting networking onto a game built around local state is often a rewrite.

## First question: which kind?

| Kind | What it needs | Difficulty |
|---|---|---|
| Local (same screen / split screen) | Multiple input devices, camera/viewport management | Low–moderate |
| Asynchronous (turns by mail, leaderboards, ghosts) | A backend storing state or results; no real-time sync | Moderate |
| Turn-based online | Server-authoritative turn validation, reconnection | Moderate |
| Real-time cooperative | State sync, latency hiding; cheating less critical | High |
| Real-time competitive | Server authority, lag compensation, anti-cheat, matchmaking | Very high |

If the user's idea works as local or asynchronous multiplayer, say so; it is dramatically cheaper.

## Architectures

- **Client-server, server-authoritative.** The server owns the true game state; clients send inputs; the server simulates and broadcasts state. Default for anything competitive. Costs: you run servers.
- **Listen server / host.** One player's machine is the server. Cheaper; host advantage and host-leaves problems.
- **Peer-to-peer lockstep.** All peers run the same deterministic simulation from the same inputs. Low bandwidth (inputs only), common in RTS and fighting games; requires strict determinism (fixed timestep, deterministic maths across platforms, no unordered iteration affecting state) and is sensitive to the slowest peer.
- **Rollback netcode.** Predict remote inputs, simulate ahead, and roll back and re-simulate when real inputs arrive. Excellent feel for fighting/action games; requires fast save/restore of full game state and determinism.

## Latency hiding techniques

- **Client-side prediction**: apply the local player's input immediately, reconcile when the server's authoritative state arrives.
- **Entity interpolation**: render remote entities slightly in the past, interpolating between received snapshots.
- **Lag compensation**: the server rewinds other entities to what the shooter saw when validating hits.
- **Snapshot compression and delta encoding** to reduce bandwidth.

## Practical guidance

- Separate simulation from presentation first (see the main skill); networked games are impossible to reason about without it.
- Use a fixed simulation tick.
- Prefer an engine's or a well-maintained library's networking layer over writing transport, reliability and NAT traversal yourself.
- Test with simulated latency, jitter and packet loss from day one; LAN testing hides almost every problem.
- Never trust the client for anything that affects other players: validate movement bounds, cooldowns, inventory and damage on the server.
- Plan reconnection, host migration (if applicable), and what happens when a player leaves mid-match.
- Budget for server hosting, matchmaking, accounts, abuse reporting and moderation (text/voice chat between strangers raises safety obligations, especially with minors).
- Online play generally requires privacy disclosures and may require age-appropriate design depending on audience and jurisdiction.
