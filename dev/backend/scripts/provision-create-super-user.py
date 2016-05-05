import pexpect

child = pexpect.spawn("python manage.py createsuperuser --username admin --email viperey@gmail.com")
child.expect('.*assword.*', timeout=4)
child.sendline("password")
child.expect('.*assword.*', timeout=3)
child.sendline("password")
child.expect(pexpect.EOF)
