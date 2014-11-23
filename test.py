from hashEngine import HashEngine

x = HashEngine()

hash_value1 = x.generate_hash("janek", "kurzydlo")

hash_value2 = x.generate_hash("janek", "kurzydlo")

print x.compare_hashes(hash_value1, hash_value2)

#pamietac o gonerowaniu hasha