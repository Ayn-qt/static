# ============================================================
#                   1)    CAESAR CIPHER
#          Encryption + Decryption + User Choice (e/d)
# ============================================================

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result
def decrypt(text, shift):
    return encrypt(text, -shift)
print("===== CAESAR CIPHER =====")
message = input("Enter your message: ")
shift = int(input("Enter shift value: "))
mode = input("Encrypt or Decrypt? (e/d): ").lower()
if mode == 'e':
    print("\nEncrypted message:", encrypt(message, shift))
elif mode == 'd':
    print("\nDecrypted message:", decrypt(message, shift))
else:
    print("\nInvalid choice! Please enter 'e' or 'd'.")









# ============================================================
#                 2) RAIL FENCE CIPHER (FULL)
#          Encryption + Decryption + User Interaction
# ============================================================

def encrypt_rail_fence(text, rails):
    rail_matrix = [['\n' for _ in range(len(text))] for _ in range(rails)]
    down = False
    row, col = 0, 0
    for char in text:
        if row == 0 or row == rails - 1:
            down = not down
        rail_matrix[row][col] = char
        col += 1
        row += 1 if down else -1
    result = []
    for r in rail_matrix:
        for c in r:
            if c != '\n':
                result.append(c)
    return "".join(result)
def decrypt_rail_fence(cipher, rails):
    rail_matrix = [['\n' for _ in range(len(cipher))] for _ in range(rails)]
    down = None
    row, col = 0, 0
    for _ in cipher:
        if row == 0:
            down = True
        if row == rails - 1:
            down = False
        rail_matrix[row][col] = '*'
        col += 1
        row += 1 if down else -1
    index = 0
    for i in range(rails):
        for j in range(len(cipher)):
            if rail_matrix[i][j] == '*' and index < len(cipher):
                rail_matrix[i][j] = cipher[index]
                index += 1
         
    result = []
    row, col = 0, 0
    for _ in range(len(cipher)):
        if row == 0:
            down = True
        if row == rails - 1:
            down = False
        if rail_matrix[row][col] != '\n' and rail_matrix[row][col] != '*':
            result.append(rail_matrix[row][col])
        col += 1
        row += 1 if down else -1
    return "".join(result)
print("===== RAIL FENCE CIPHER =====")
msg = input("Enter message: ")
rails = int(input("Enter number of rails: "))
choice = input("Encrypt or Decrypt? (e/d): ").lower()
if choice == "e":
    print("\nEncrypted:", encrypt_rail_fence(msg, rails))
else:
    print("\nDecrypted:", decrypt_rail_fence(msg, rails))


















# ============================================================
#                    3) PLAYFAIR CIPHER (FULL)
#                Encryption + Decryption + Input
# ============================================================

# Step 1: Generate 5x5 key matrix
def generate_key_matrix(key):
    key = key.upper().replace('J', 'I')
    used = []
    for char in key:
        if char.isalpha() and char not in used:
            used.append(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in used:
            used.append(char)

    matrix = [used[i:i+5] for i in range(0, 25, 5)]
    return matrix
def find_coords(matrix, char):
    char = char.upper().replace('J', 'I')
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return None, None
def prepare_text(text):
    text = text.upper().replace(" ", "").replace('J', 'I')
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'X'
        if a == b:
            result += a + 'X'
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += 'X'
    return result
def playfair(text, key, mode):
    matrix = generate_key_matrix(key)
    if mode == "encrypt":
        shift = 1
        text = prepare_text(text)
    else:
        shift = -1
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_coords(matrix, a)
        r2, c2 = find_coords(matrix, b)
        #Same Row
        if r1 == r2:
            result += matrix[r1][(c1 + shift) % 5]
            result += matrix[r2][(c2 + shift) % 5]
        #Same Column
        elif c1 == c2:
            result += matrix[(r1 + shift) % 5][c1]
            result += matrix[(r2 + shift) % 5][c2]
        #Rectangle Rule
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]
    return result
# Remove padding 'X'
def clean_playfair_output(text):
    cleaned = ""
    i = 0
    while i < len(text):
        if (
            i < len(text)-2 and
            text[i] == text[i+2] and
            text[i+1] == 'X'
        ):
            cleaned += text[i]
            i += 2
        else:
            cleaned += text[i]
            i += 1
    if cleaned.endswith("X"):
        cleaned = cleaned[:-1]
    return cleaned
print("===== PLAYFAIR CIPHER =====")
key = input("Enter keyword: ")
text = input("Enter text: ")
mode = input("Encrypt or Decrypt? (e/d): ").lower()
mode = 'encrypt' if mode == 'e' else 'decrypt'
output = playfair(text, key, mode)
if mode == "decrypt":
    output = clean_playfair_output(output)
print("\nResult:", output)
