import random

def is_prime(num):
    """Checks if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def get_generator(p):
    """Finds a primitive root (generator) modulo p."""
    """
        - This function finds a primitive root (generator) modulo p.\
        - A generator g is a number such that its powers modulo p can produce all integers from 1 to p-1.\
        - The algorithm iterates through numbers from 2 to p-1 and \
            checks if each number is a generator by verifying that g^(phi/factor) mod p is not equal to 1 \
            for all prime factors of phi (where phi = p - 1).
    """

    """
        - This function finds a primitive root (generator) modulo p.\
    """
    if not is_prime(p):
        raise ValueError("p must be a prime number")
    
    """
        - A generator g is a number such that its powers modulo p can produce all integers from 1 to p-1.\
    """
    phi = p - 1
    factors = set()
    d = 2
    temp_phi = phi
    while d * d <= temp_phi:
        if temp_phi % d == 0:
            factors.add(d)
            while temp_phi % d == 0:
                temp_phi //= d
        d += 1
    if temp_phi > 1:
        factors.add(temp_phi)

    for res in range(2, p):
        """
        - The algorithm iterates through numbers from 2 to p-1 and \
            checks if each number is a generator by verifying that g^(phi/factor) mod p is not equal to 1 \
            for all prime factors of phi (where phi = p - 1).
        """
        
        is_generator = True
        for factor in factors:
            if pow(res, phi // factor, p) == 1:
                is_generator = False
                break
        if is_generator:
            return res
    return None

def diffie_hellman_key_exchange(p, g):
    """Performs the Diffie-Hellman key exchange."""
    """
        + Takes the public prime p and generator g as input.
        + Alice's Side:
            - Generates a secret private key alice_private_key.
            - Calculates her public key alice_public_key as g^alice_private_key mod p.
        + Bob's Side:
            - Generates a secret private key bob_private_key.
            - Calculates his public key bob_public_key as g^bob_private_key mod p.
        + Key Exchange (Simulated):
            - Prints the public keys that would be exchanged over an insecure channel.
        +Shared Secret Calculation:
            - Alice calculates the shared secret by raising Bob's public key to her private key modulo p: pow(bob_public_key, alice_private_key, p).
            - Bob calculates the shared secret by raising Alice's public key to his private key modulo p: pow(alice_public_key, bob_private_key, p).
    """

    # --- Alice's side ---
    alice_private_key = random.randint(1, p - 1)
    alice_public_key = pow(g, alice_private_key, p)
    print(f"Alice's private key (secret): {alice_private_key}")
    print(f"Alice's public key: {alice_public_key}\n")

    # --- Bob's side ---
    bob_private_key = random.randint(1, p - 1)
    bob_public_key = pow(g, bob_private_key, p)
    print(f"Bob's private key (secret): {bob_private_key}")
    print(f"Bob's public key: {bob_public_key}\n")

    # --- Exchange public keys (insecure channel) ---
    print("--- Exchanging public keys ---\n")

    # --- Alice computes the shared secret ---
    alice_shared_secret = pow(bob_public_key, alice_private_key, p)
    print(f"Alice's calculated shared secret: {alice_shared_secret}")

    # --- Bob computes the shared secret ---
    bob_shared_secret = pow(alice_public_key, bob_private_key, p)
    print(f"Bob's calculated shared secret: {bob_shared_secret}")

    if alice_shared_secret == bob_shared_secret:
        print("\nShared secret established successfully!")
        return alice_shared_secret
    else:
        print("\nError: Shared secrets do not match!")
        return None

if __name__ == "__main__":
    # Choose public parameters (should be large in a real-world scenario)
    p = 29  # A small prime number for demonstration
    g = get_generator(p)

    if g is None:
        print(f"Could not find a generator for p = {p}. Please choose another prime.")
    else:
        print(f"Publicly agreed prime (p): {p}")
        print(f"Publicly agreed generator (g): {g}\n")

        shared_secret = diffie_hellman_key_exchange(p, g)

        if shared_secret:
            print(f"\nShared secret key: {shared_secret}")