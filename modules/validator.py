def password_validator(password, confirm):
    if len(password) < 8:
        return {'status': 'error', 'msg': 'Password must be at least 8 characters.'}

    if password.isdigit():
        return {'status': 'error', 'msg': 'Password is fully numeric. Must contain alphabets.'}

    if password.isalpha():
        return {'status': 'error', 'msg': 'Password is fully alphabetic. Must contain numbers.'}
    
    if password != confirm:
        return {'status': 'error', 'msg': 'Password did not match.'}
    
    return True