import bcrypt

# Generate password hashes
table_password = "table123"
admin_password = "admin123"

table_hash = bcrypt.hashpw(table_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
admin_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"Table password hash: {table_hash}")
print(f"Admin password hash: {admin_hash}")
