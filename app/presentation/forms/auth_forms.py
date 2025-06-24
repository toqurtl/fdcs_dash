from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('사용자명', validators=[
        DataRequired(message='사용자명을 입력해주세요.'),
        Length(min=3, max=20, message='사용자명은 3-20자 사이여야 합니다.')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요.'),
        Length(min=4, message='비밀번호는 최소 4자 이상이어야 합니다.')
    ])
    remember_me = BooleanField('로그인 상태 유지')
    submit = SubmitField('로그인')