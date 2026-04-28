import random

def mod_add(a, b, p):
    return (a + b) % p

def mod_mul(a, b, p):
    return (a * b) % p

def mod_inv(a, p):
    # Fermat's Little Theorem (p must be prime)
    return pow(a, p - 2, p)


def generate_shares(secret, n, t, p):
    """
    secret: the secret value
    n: number of shares
    t: threshold
    p: prime modulus
    """
    # Polynomial coefficients
    coeffs = [secret] + [random.randint(1, p - 1) for _ in range(t - 1)]

    def polynomial(x):
        y = 0
        for i, coef in enumerate(coeffs):
            y = (y + coef * pow(x, i, p)) % p
        return y

    shares = [(i, polynomial(i)) for i in range(1, n + 1)]
    return shares

def reconstruct_secret(shares, p):
    """
    Reconstruct the secret using Lagrange interpolation
    shares: list of (x, y)
    """
    secret = 0

    for i, (xi, yi) in enumerate(shares):
        num = 1
        den = 1

        for j, (xj, _) in enumerate(shares):
            if i != j:
                num = (num * (-xj)) % p
                den = (den * (xi - xj)) % p

        lagrange_coeff = num * mod_inv(den, p)
        secret = (secret + yi * lagrange_coeff) % p

    return secret



def additive_share(secret, n, p):
    shares = [random.randint(0, p - 1) for _ in range(n - 1)]
    last_share = (secret - sum(shares)) % p
    shares.append(last_share)
    return shares

def reconstruct_additive(shares, p):
    return sum(shares) % p



def main():
    print("==== Shamir Secret Sharing ====")

    # Parameters
    p = 2089        # prime number
    secret = 1234
    n = 5           # total shares
    t = 3           # threshold

    # Generatation of shares
    shares = generate_shares(secret, n, t, p)
    print("Generated Shares:")
    for s in shares:
        print(s)

    # Correctection of reconstruction
    print("\nReconstructing with t shares:")
    recovered = reconstruct_secret(shares[:t], p)
    print("Recovered secret:", recovered)

    # Incorrect reconstruction (less than t)
    print("\nReconstructing with less than t shares:")
    recovered_wrong = reconstruct_secret(shares[:t-1], p)
    print("Recovered (incorrect):", recovered_wrong)

    print("\n==== Additive Secret Sharing ====")

    # Additive sharing
    add_shares = additive_share(secret, n, p)
    print("Additive Shares:", add_shares)

    # Reconstruction
    recovered_add = reconstruct_additive(add_shares, p)
    print("Recovered additive secret:", recovered_add)


if __name__ == "__main__":
    main()