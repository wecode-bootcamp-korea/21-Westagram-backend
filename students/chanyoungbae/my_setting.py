import pymysql
SECRET_KEY = 'django-insecure-=8a#hmcj)%qi_#4ujuu8vn9late#gp)xel$a=86s6f0*%%j+6+'
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'westargram',
        'USER': 'root',
        'PASSWORD': 'cksdud4607',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()