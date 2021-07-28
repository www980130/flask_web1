from passlib.hash import pbkdf2_sha256

#회원가입 기능 구현할 때 쓰기 위한 테스트
hash = pbkdf2_sha256.hash("toomanysecrets")

print(hash)
#로그인 기능 구현할 때 쓰기 위한 테스트
result = pbkdf2_sha256.verify("dfdftoomanysecrets", hash)
print(result)