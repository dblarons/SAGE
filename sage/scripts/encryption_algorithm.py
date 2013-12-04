import numpy, random, json, os

HILL_STRENGTH = 50
KEY_STRENGTH = 100000 # Upper end of range for private keys (don't make more than 10000000000)
MATRIX_SIZE = 15

''' PrivateKey
    
    PrivateKey takes no parameters for initialization, but p and q instance 
    variables are created on a PrivateKey object when a key is created or 
    retrieved. p and q are the private key pair and can be stored or 
    regenerated.

'''
class PrivateKey(object):

    def __init__(self):
        pass

    def generate_prime_number(self, n):
        # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
        """ Input n>=6, Returns a array of primes, 2 <= p < n """
        sieve = numpy.ones(n/3 + (n%6==2), dtype=numpy.bool)
        sieve[0] = False
        for i in xrange(int(n**0.5)/3+1):
            if sieve[i]:
                k=3*i+1|1
                sieve[      ((k*k)/3)      ::2*k] = False
                sieve[(k*k+4*k-2*k*(i&1))/3::2*k] = False
        return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0]+1)|1)]

    def create_private_key(self, n):
        primes = self.generate_prime_number(n)
        key = primes[random.randint(3, (len(primes) - 1))]
        return key

    def new_private_key_pair(self):
        self.p = self.create_private_key(KEY_STRENGTH)
        self.q = self.create_private_key(KEY_STRENGTH)
        while self.q == self.p:
            self.q = self.create_private_key(KEY_STRENGTH)

    def store_private_key(self, filepath):
        if not self.p or not self.q:
            self.new_private_key_pair()
        a = [str(self.p), str(self.q)]
        with open(filepath, 'w+') as f:
            f.write('.'.join(a))

    def retrieve_stored_key(self, filepath):
        with open(filepath, 'r') as f:
            keychain = f.read()
        self.p = int(keychain.partition(".")[0])
        self.q = int(keychain.partition(".")[2])


''' PublicKey 

    PublicKey is initialized with a private key pair and generates a public
    key from that private key pair. It includes methods for storing and 
    retrieving keys. n and e are the public key pair

'''
class PublicKey(object):
    def __init__(self):
        pass

    # n = p * q
    def generate_n(self, p, q):
        self.n = p * q

    def generate_e(self, p, q):
        private_key = PrivateKey()
        e = private_key.create_private_key(100)
        phi_n = generate_phi_n(p, q)
        while phi_n % e == 0:
            e = private_key.create_private_key(100)
        self.e = long(e)

    def new_public_key_pair(self, p, q):
        self.generate_n(p, q)
        self.generate_e(p, q)

    # stores public key in the format n.e
    def store_public_key(self, filepath):
        if not self.n or not self.e:
            raise NameError('Public key pair not generated. Please use new_public_key_pair.')
        a = [str(self.n), str(self.e)]
        with open(filepath, 'w+') as f:
            f.write('.'.join(a))

    def retrieve_stored_key(self, filepath):
        with open(filepath, 'r') as f:
            keychain = f.read()
        self.n = int(keychain.partition(".")[0])
        self.e = int(keychain.partition(".")[2])

class EncryptMessage(object):

    def __init__(self, n, e, filepath, matrix_size=MATRIX_SIZE):
        self.n = n
        self.e = e

        with open(filepath, 'r') as f:
            contents = f.read()
        self.message = contents

        self.matrix_size = matrix_size

        self.main()

    def main(self):
        number_text = self.numbers_for_letters()
        number_of_matrices = self.number_of_matrices()
        sizes = self.determine_matrix_sizes()
        cipher_one = self.generate_hill_cipher_one(sizes[0])
        cipher_two = self.generate_hill_cipher_two(sizes[1])
        cipher_text = self.encrypt_plain_text(number_text, cipher_one, cipher_two, number_of_matrices)
        encrypted_cipher_one = self.encrypt_cipher_with_public_key(cipher_one, self.n, self.e)
        encrypted_cipher_two = self.encrypt_cipher_with_public_key(cipher_two, self.n, self.e)
        encrypted_message_array = self.encrypt_message_with_public_key(cipher_text, self.n, self.e)
        self.encrypted_message = self.create_encrypted_string(sizes[0], sizes[1], encrypted_cipher_one, encrypted_cipher_two, encrypted_message_array)

    def generate_hill_cipher_one(self, size):
        matrix = numpy.eye(size)
        matrix[0] = matrix[0] * 2
        while numpy.linalg.det(matrix) != 1 and numpy.linalg.det(matrix) != -1:
            matrix = numpy.eye(size)
            for i in range(HILL_STRENGTH):
                a = random.randint(0, size - 1)
                b = random.randint(0, size - 1)
                while b == a:
                    b = random.randint(0, size - 1)
                matrix[a] = matrix[a] + matrix[b]
        return matrix

    def generate_hill_cipher_two(self, size):
        if size == 0:
            return [[0]]
        return self.generate_hill_cipher_one(size)

    # returns (first_matrix_size, second_matrix_size)
    def determine_matrix_sizes(self):
        text_length = len(self.message)
        if text_length / self.matrix_size == 0:  # Not enough to make one full-size matrix
            return text_length, 0
        elif text_length % self.matrix_size == 0:  # One matrix fits all
            return self.matrix_size, 0
        elif text_length % self.matrix_size == 1:
            if text_length / self.matrix_size == 1:  # ex/ size = 10, length = 11, so one 11x11 matrix
                return self.matrix_size + 1, 0
            else:                        # ex/ size = 10, length = 21
                return self.matrix_size, self.matrix_size + 1
        else:
            return self.matrix_size, text_length % self.matrix_size # ex output/ (10, 4)

    def number_of_matrices(self):
        text_length = len(self.message)
        if text_length % self.matrix_size == 1:  # ex/ 10 matrices for text_length = 100
            return text_length / self.matrix_size - 1
        else:
            return text_length / self.matrix_size

    # Use 87 character alphabet to convert each letter into a number
    def numbers_for_letters(self):
        alphabet = get_alphabet()
        message_in_numbers = []
        for i in range(len(self.message)):
            if self.message[i] in alphabet:
                number = alphabet.index(self.message[i])
                message_in_numbers.append(number)
            else:
                # Character is unrecognized; assign default
                message_in_numbers.append(86)
        return message_in_numbers

    def encrypt_plain_text(self, number_text, cipher1, cipher2, loops):
        encrypted_message_array = []
        for i in range(loops):
            array = []
            for j in range(len(cipher1[0])):
                array.append(number_text.pop(0))
            array2 = numpy.dot(array, cipher1)
            for i in range(len(array2)):
                encrypted_message_array.append(array2[i])
        try:
            cipher2[0][1] # This is what we're 'trying.' If this doesn't exist, it won't work.
            array3 = []
            for i in range(len(number_text)):
                array3.append(number_text.pop(0))
            array4 = numpy.dot(array3, cipher2)
            for i in range(len(array4)):
                encrypted_message_array.append(array4[i])
        except IndexError:
            pass
        return encrypted_message_array

    def encrypt_cipher_with_public_key(self, cipher, n, e):
        if not cipher[0][0] == 0:
            pk_encrypted_cipher = []
            for i in range(len(cipher[0])):
                array = cipher[i]
                for j in range(len(cipher[0])):
                    m = long(array[j])
                    c = pow(m, e, n)

                    pk_encrypted_cipher.append(c)
            return pk_encrypted_cipher
        else:
            return []

    def encrypt_message_with_public_key(self, message, n, e):
        pk_encrypted_message = []
        for i in range(len(message)):
            m = long(message[i])
            c = pow(m, e, n)
            pk_encrypted_message.append(c)
        return pk_encrypted_message

    def matrix_to_string(self, send_file, size, cipher):
        for i in range(size):
            send_file = send_file + str(cipher[i]) + "."
        return send_file

    def create_encrypted_string(self, size_one, size_two, cipher_one, cipher_two, message):
        send_file = str(size_one) + "." + str(size_two) + "."
        send_file = self.matrix_to_string(send_file, len(cipher_one), cipher_one)
        send_file = self.matrix_to_string(send_file, len(cipher_two), cipher_two)
        for i in range(len(message)):
            send_file += str(message[i]) + "."
        send_file = send_file[:(len(send_file) - 1)]
        return send_file

    def write(self, output_file):
        if not self.encrypted_message:
            raise NameError('encrypted_message not present')
        with open(output_file, 'w') as f:
            f.write(self.encrypted_message)


class DecryptMessage(object):
    def __init__(self, p, q, e, textfile):
        self.p = p
        self.q = q
        self.e = e
        self.n = p * q

        with open(textfile, 'r') as f:
            contents = f.read()
        self.encrypted_message = contents

        self.main()

    def main(self):
        matrices = self.separate_matrix_from_message() # (matrix1, matrix2, message, size1, size2)
        phi_n = generate_phi_n(self.p, self.q)
        d = self.generate_d(phi_n)
        matrix1 = self.decrypt_cipher(d, self.n, matrices[0], matrices[3])
        matrix2 = self.decrypt_cipher(d, self.n, matrices[1], matrices[4])
        imatrix1 = self.invert_cipher(matrix1)
        imatrix2 = self.invert_cipher(matrix2)
        decrypted_message = self.decrypt_pk_message(d, self.n, matrices[2])
        decrypted_hill_cipher = self.decrypt_hill_cipher(imatrix1, imatrix2, decrypted_message)
        self.message_to_plain_text(decrypted_hill_cipher)

    def separate_matrix_from_message(self):
        encrypted_array = self.encrypted_message.split(".")
        size_one = int(encrypted_array.pop(0))
        size_two = int(encrypted_array.pop(0))
        matrix_length_one = size_one ** 2
        matrix_length_two = size_two ** 2
        matrix_one = []
        for i in range(matrix_length_one):
            matrix_one.append(long(encrypted_array.pop(0)))
        matrix_two = []
        for i in range(matrix_length_two):
            matrix_two.append(long(encrypted_array.pop(0)))
        message = encrypted_array
        return matrix_one, matrix_two, message, size_one, size_two

    def generate_d(self, phi_n):
        a = 1
        while (a * phi_n + 1) % self.e != 0:
            a += 1
        d = (a * phi_n + 1) / self.e
        return d

    def decrypt_cipher(self, d, n, encrypted_cipher, size): # Cipher is c in the formula
        unencrypted_cipher = []
        for i in range(len(encrypted_cipher)):
            unencrypted_cipher.append(pow(encrypted_cipher[i], d, n))
        matrix = []
        for i in range(size):
            matrix1 = []
            for j in range(size):
                matrix1.append(unencrypted_cipher.pop(0))
            matrix.append(matrix1)
        return matrix

    def invert_cipher(self, unencrypted_cipher):
        if len(unencrypted_cipher) != 0:
            matrix = numpy.matrix(unencrypted_cipher).I
            for i in range(len(numpy.array(matrix))):
                matrix = numpy.array(matrix)
                for j in range(len(matrix[i])):
                    matrix[i][j] = round(matrix[i][j])
            return matrix
        else:
            return [0]

    def decrypt_pk_message(self, d, n, message):
        decrypted_message = []
        for i in range(len(message)):
            decrypted_message.append(pow(long(message[i]), d, n))
        return decrypted_message

    def decrypt_hill_cipher(self, inverted_matrix1, inverted_matrix2, decrypted_message):
        size = len(inverted_matrix1)
        message = []

        # if the second matrix needs to be used, use the first matrix one less time
        loops = 0
        if len(decrypted_message) == 1:
            loops = len(decrypted_message) / size
        elif len(decrypted_message) / size == 0:
            loops = 1
        elif len(decrypted_message) % size == 0:
            loops = len(decrypted_message) / size
        elif len(decrypted_message) % size > 0:
            if len(decrypted_message) % size == 1:
                loops = len(decrypted_message) / size - 1
            elif len(decrypted_message) % size > 1:
                loops = len(decrypted_message) / size

        for i in range(loops):
            array = []
            for j in range(len(inverted_matrix1)):
                array.append(decrypted_message.pop(0))
            message0 = numpy.dot(array, inverted_matrix1) # unencrypt this portion of the message
            message0 = numpy.array(message0)
            for j in range(size):
                message.append(message0[j])

        # return now if there is not a second matrix
        if len(inverted_matrix2) == 1:
            return message

        # decrypt the "leftovers" if there is a second matrix
        size = len(inverted_matrix2)
        array1 = []
        for i in range(size):
            array1.append(decrypted_message.pop(0))
        array2 = numpy.dot(array1, inverted_matrix2)
        array2 = numpy.array(array2)
        for i in range(size):
            message.append(array2[i])
        return message

    def message_to_plain_text(self, message):
        alphabet = get_alphabet()
        plain_text = ""
        for i in range(len(message)):
            plain_text = plain_text + alphabet[(int(message[i]) % 89)]
        self.decrypted_message = plain_text

    def write(self, output_file):
        if not self.decrypted_message:
            raise NameError('decrypted_message not present')
        with open(output_file, 'w') as f:
            f.write(self.decrypted_message)

# Helper methods

# phi(n) = (p - 1) * (q - 1)
def generate_phi_n(p, q):
    phi_n = (p - 1) * (q - 1)
    return phi_n

# Get the supported alphabet from its json file and make into array
def get_alphabet():
    here = os.path.abspath(os.path.dirname(__file__))
    alphabet = os.path.join(here, 'alphabet.json')
    with open(alphabet, 'r') as f:
        alphabet = json.loads(f.read())
    return alphabet
