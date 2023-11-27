from faker import Faker
fake = Faker(locale="fr_FR")

print(fake.name())

print(fake.address())