# Weibo_1.0 With Flask
Content:
<pre>
Weibo_1.0
│  config.py
│  manage.py
│  Weibo_1.0.py
│
├─app
│  │  ioc.py
│  │  socket.py
│  │  __init__.py
│  │
│  ├─api
│  │  │  __init__.py
│  │  │
│  │  ├─common
│  │  │      util.py
│  │  │      __init__.py
│  │  │
│  │  └─resources
│  │          classification.py
│  │          comment.py
│  │          role.py
│  │          user.py
│  │          __init__.py
│  │
│  ├─auth
│  │      errors.py
│  │      forms.py
│  │      views.py
│  │      __init__.py
│  │
│  ├─main
│  │      errors.py
│  │      forms.py
│  │      views.py
│  │      __init__.py
│  │
│  ├─models
│  │      classification_model.py
│  │      comment_model.py
│  │      follow_model.py
│  │      role_model.py
│  │      user_model.py
│  │      util_model.py
│  │      __init__.py
│  │
│  ├─repositories
│  │      base_repository.py
│  │      classification_repository.py
│  │      comment_repository.py
│  │      role_repository.py
│  │      user_repository.py
│  │      __init__.py
│  │
│  ├─services
│  │      __init__.py
│  │
│  ├─static
│  ├─templates
│  │  ├─auth
│  │  │  └─email
│  │  └─error
│  └─util
│          decorators.py
│          email.py
│          __init__.py
│
└─venv
</pre>
