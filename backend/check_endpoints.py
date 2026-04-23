#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

def short(x, n=400):
    try:
        s = x.decode('utf-8')
    except Exception:
        s = str(x)
    return s.replace('\n', ' ')[:n]

def main():
    c = Client()
    endpoints = [
        '/',
        '/api/assets/',
        '/api/news/',
        '/admin/',
    ]

    for url in endpoints:
        try:
            resp = c.get(url)
            status = resp.status_code
            content = short(resp.content)
        except Exception as e:
            status = 'ERR'
            content = str(e)
        print(f"URL: {url}\nStatus: {status}\nPreview: {content}\n{'-'*60}")

    # Try authenticated access to watchlists using test credentials
    creds = [
        ('admin@example.com', 'admin123'),
        ('user@example.com', 'user123'),
    ]

    for email, pwd in creds:
        try:
            login_resp = c.post('/api/auth/login/', data={'email': email, 'password': pwd}, content_type='application/json')
            print(f"Login attempt for {email} -> {login_resp.status_code}")
            try:
                data = login_resp.json()
            except Exception:
                data = {}

            access = data.get('access')
            if access:
                resp = c.get('/api/watchlists/', HTTP_AUTHORIZATION=f'Bearer {access}')
                print(f"/api/watchlists/ as {email} -> {resp.status_code}\nPreview: {short(resp.content)}\n{'-'*60}")
            else:
                print(f"No access token for {email}, response: {data}\n{'-'*60}")
        except Exception as e:
            print(f"Error during login/check for {email}: {e}\n{'-'*60}")

if __name__ == '__main__':
    main()
