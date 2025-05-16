with open('.env', 'w', encoding='utf-8') as f:
    f.write('DATABASE_URI=mysql+pymysql://root:16112004@localhost/ph_agua\n')
    f.write('SECRET_KEY=phobjectiveactive\n')

print("Arquivo .env criado com sucesso.")
