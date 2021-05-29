from django.core.exceptions import ValidationError

def validate_email(email):
    if '@' not in email or '.' not in email:
        raise ValidationError('이메일 형식에 맞지 않습니다.')

def validate_password(password):
    if len(password) < 8:
        raise ValidationError('8자리 이상 입력해주세요.')



