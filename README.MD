# Django Rest framework skeleton app
## Simple example for quick start with Django Rest:
1. Simple JWT token: refresh + accept token 
2. User actions: register, login, reset password, change password
3. Docker file for quick dev start: pgSql + nginx
4. Admin backend: login, password reset
5. Base project configuration: app structure
6. Swagger support for "pretty" API views

# Install
docker-compose up

In case of permission error type "chmod +x entrypoint.sh" in console
Also make sure that database port is correct in .env file

### Simple JWT + Reset password
1. https://github.com/davesque/django-rest-framework-simplejwt
2. https://pypi.org/project/django-rest-passwordreset/

## Django Cachalot
https://django-cachalot.readthedocs.io/
### Invalidate cache
```docker-compose run --rm app sh -c "python manage.py invalidate_cachalot"```

### For create google storage access
1. https://console.cloud.google.com/storage/browser
2. Create bucket button
3. Paste unique name
4. For better speed choose location region europe/fr
5. Standart class data
6. Fine-granted(default)
7. Google manage key

### After that
1. Go to IAM & Admin
2. Service account – create service account button
3. django – as service account name
4. Owner as role
5. Create key in the ...

### JWT token authorization using Swagger
1. Create JWT access token.
2. In Swagger view click "Authorize".
3. Paste "Bearer xxx.yyy.zzz" (no quotes) where xxx.yyy.zzz is a generated token.


