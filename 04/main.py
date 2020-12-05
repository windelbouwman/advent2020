import re

def load_documents():
    with open('input.txt', 'r') as f:
        documents = []
        doc = []
        for line in f:
            line = line.strip()
            if line:
                for pair in line.split(' '):
                    key, value = pair.split(':')
                    doc.append((key, value))
            else:
                documents.append(doc)
                doc = []
        if doc:
            documents.append(doc)
    return documents

documents = load_documents()

required_keys = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
# 'cid' is optional


def is_valid(doc):
    present_keys = set(key for key, _ in doc)
    return required_keys.issubset(present_keys)


print('valid documents', sum(map(is_valid, documents)))

def is_valid_improved(doc):
    present_keys = set(key for key, _ in doc)
    if not required_keys.issubset(present_keys):
        return False
    props = {key: value for key, value in doc}

    # Check birth year:
    byr = int(props['byr'])
    if not (1920 <= byr <= 2002):
        return False
    
    # Check issue year:
    iyr = int(props['iyr'])
    if not (2010 <= iyr <= 2020):
        return False

    # Check expiration year:
    eyr = int(props['eyr'])
    if not (2020 <= eyr <= 2030):
        return False
    
    # Check height:
    hgt = props['hgt']
    if hgt.endswith('cm'):
        cm = int(hgt[:-2])
        if not (150 <= cm <= 193):
            return False
    elif hgt.endswith('in'):
        inches = int(hgt[:-2])
        if not (59 <= inches <= 76):
            return False
    else:
        return False
    
    # Check hair color:
    hcl = props['hcl']
    if not re.match(r'^#[0-9a-f]{6}$', hcl):
        return False
    
    # Check eye color:
    ecl = props['ecl']
    if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False
    
    pid = props['pid']
    if not re.match(r'^[0-9]{9}$', pid):
        return False

    return True

print('stricter valid documents', sum(map(is_valid_improved, documents)))