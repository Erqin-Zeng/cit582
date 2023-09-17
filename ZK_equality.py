from zksk import Secret, DLRep
from zksk import utils
from petlib.ec import EcPt

def ZK_equality(G, H):
    
    # Generate two random secrets r1 and r2
    r1 = Secret(utils.get_random_num(bits=128))
    r2 = Secret(utils.get_random_num(bits=128))
    
    # Generate a random message m 
    m = Secret(utils.get_random_num(bits=128)) #Secret(utils.get_random_num(bits=128))

    # Create two elliptic curve points C1 and C2
    C1 = r1.value * G
    C2 = r1.value * H + (m.value * G)

    # Create two elliptic curve points D1 and D2
    D1 = r2.value * G
    D2 = r2.value * H + (m.value * G)

    # Define the proof statement
    stmt = DLRep(C1,r1*G) & DLRep(C2,r1*H+m*G) & DLRep(D1,r2*G) & DLRep(D2,r2*H+m*G)

    # Generate a non-interactive zero-knowledge proof for the statement
    zk_proof = stmt.prove()
    
    # Return the elliptic curve points C1, C2, D1, D2, and the proof
    return (C1, C2), (D1, D2), zk_proof

