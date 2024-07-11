import hashlib

def calculate_file_hash(file_path, algorithm='sha256'):
    hash_function = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_function.update(chunk)
    return hash_function.hexdigest()

file_path = '/Users/karolinaryzka/Documents/AIUS/research_ai-usage-in-science/models/Modelfile'  # Replace with the actual file path
algorithm = 'sha256'
hash_value = calculate_file_hash(file_path, algorithm)
print(f'The {algorithm} hash of the file is: {hash_value}')

# hash = d321304e6d1f8541cddca1d6994b8d34de50852d390c2a1ad7af1867423e5239

# git commit c5041266168b258f1dfd30d27e1501ef50d6e298


