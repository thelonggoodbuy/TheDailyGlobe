from passlib.context import CryptContext

# Создаем экземпляр CryptContext с использованием схемы bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def main():
    print('Input text for hashing:')
    user_input = input()
    hashed_text = hash_password(user_input)
    print(hashed_text)

if __name__ == "__main__":
    main()