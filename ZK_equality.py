from zksk import Secret, DLRep
from zksk import utils

def ZK_equality(G, H):
    # Generate two random secrets r1 and r2
    r1 = Secret(utils.get_random_num(bits=128))
    r2 = Secret(utils.get_random_num(bits=128))
    
    # Generate a random bit m (0 or 1)
    m = Secret(utils.get_random_num(bits=1))

    # Create two elliptic curve points C1 and C2
    C1 = r1 * G
    C2 = r1 * H + (m * G)

    # Create two elliptic curve points D1 and D2
    D1 = r2 * G
    D2 = r2 * H + (m * G)

    # Define the proof statement for both scenarios (m=0 and m=1)
    if m==1:
        stmt1 = DLRep(C2, r1 * H, simulated=True) | DLRep((C2 - G), r1 * H)
        stmt2 = DLRep(D2, r2 * H, simulated=True) | DLRep((D1 - G), r2 * H)
    else: # m=0
        stmt1 = DLRep(C2, r1 * H) | DLRep((C2 - G), r1 * H,simulated=True)
        stmt2 = DLRep(D2, r2 * H) | DLRep((D2 - G), r2 * H,simulated=True)

    # Generate a non-interactive zero-knowledge proof for the statement
    zk_proof = stmt1.prove() & stmt2.prove()

    # Return the elliptic curve points C1, C2, D1, D2, and the proof
    return C1, C2, D1, D2, zk_proof
