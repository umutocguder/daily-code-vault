"""
Architectural Notes: Raft vs Paxos Consensus
"""

CONSENSUS_PRINCIPLES = {
    "Leader Election": "Heartbeats trigger randomized timeouts to elect a unique leader.",
    "Log Replication": "Leader accepts client commands, appends to log, and broadcasts AppendEntries RPCs.",
    "Safety Guarantee": "Election safety, Leader Append-Only, and Log Matching Invariants ensure linearizability.",
}


def get_consensus_summary() -> dict:
    return CONSENSUS_PRINCIPLES
