from zksk import Secret, DLRep
from zksk import utils

def ZK_equality(G, H):
    # Generate two random secrets r1 and r2
    r1 = Secret(utils.get_random_num(bits=128))
    r2 = Secret(utils.get_random_num(bits=128))

    # Create two elliptic curve points C1 and C2
    C1 = r1 * G
    C2 = r1 * H

    # Generate a random bit m (0 or 1)
    m = Secret(utils.get_random_num(bits=1))

    # Update C2 with the addition of m*G
    C2 += m.value * G

    # Create two elliptic curve points D1 and D2
    D1 = r2 * G
    D2 = r2 * H

    # Update D2 with the addition of m*G
    D2 += m.value * G

    # Define the proof statement for both scenarios (m=0 and m=1)
    stmt = (DLRep(C1, r1 * G) & DLRep(C2, r1 * H + m * G)) | (DLRep(D1, r2 * G) & DLRep(D2, r2 * H + m * G))

    # Generate a non-interactive zero-knowledge proof for the statement
    zk_proof = stmt.prove()

    # Return the elliptic curve points C1, C2, D1, D2, and the proof
    return C1, C2, D1, D2, zk_proof

