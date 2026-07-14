from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

password = "amishipassword"

print(
    pwd_context.hash(password)
)