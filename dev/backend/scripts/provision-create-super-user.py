import pexpect

child = pexpect.spawn("python manage.py createsuperuser --username admin --email viperey@gmail.com")
child.expect('.*assword.*', timeout=4)
child.sendline("12341234")
child.expect('.*assword.*', timeout=3)
child.sendline("12341234")
child.expect(pexpect.EOF)
