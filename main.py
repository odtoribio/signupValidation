
import webapp2
import re

form = """
        <html>
<head>
    <title>Sign up user</title>
    <style type="text/css">
    .label{text-align: right;}
    .error{color: red}
    </style>
</head>
<body>
    <h2>Signup</h2>
    <form method="post">
        <table>
            <tr>
                <td class="label">
                    Username
                </td>
                <td>
                    <input type="text" name="username" value="%(name)s">
                </td>
                <td class="error">
                    %(username_error)s
                </td>
            </tr>
            <tr>
                <td class="label">
                    Password
                </td>
                <td>
                    <input type="password" name="password" value="">
                </td>
                <td class="error">
                    %(password_error)s
                </td>
            </tr>
            <tr>
                <td class="label">
                    Verify password
                </td>
                <td>
                    <input type="password" name="verify" value="">
                </td>
                <td class="error">
                    %(verify_error)s
                </td>
            </tr>
            <tr>
                <td class="label">
                    Email(optional)
                </td>
                <td>
                    <input type="text" name="email" value="%(em)s">
                </td>
                <td class="error">
                    %(email_error)s
                </td>
            </tr>

            <br>
            <br>

        </table>
        <input type="submit">
    </form>

</body>
</html>
"""


class MainHandler(webapp2.RequestHandler):

    username_error = ""
    password_error =""
    verify_error = ""
    email_error = ""
    name = ""
    em=""

    def valid_username(self,username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        status = USER_RE.match(username)

        if status == None:
            self.username_error = "That's not valid Username"
            return False
        else:
            self.name = username
            return True

    def valid_email(self,email):
        email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        status = email_re.match(email)

        if (status != None) or (not email):
            self.em = email
            return True
        else:
            self.email_error = "That's not valid email"
            return False

    def valid_password(self,password,verify):
        password_re = re.compile(r"^.{3,20}$")

        if not password:
            self.password_error = "That's wasn't a valid password"
            return False
        else:
            status = password_re.match(password)
            if (status != None):
                if password == verify:
                    return True
                else:
                    self.verify_error = "Your passwords didn't match"
                    return False
            else:
                self.password_error = "That's wasn't a valid password"
                return False

    def get(self):
        self.response.write(form %{"em":self.em,"name":self.name,"username_error":self.username_error,
                                   "password_error" : self.password_error, "verify_error":self.verify_error, "email_error" :self.email_error} )

    def post(self):

        user = self.request.get("username")
        password = self.request.get("password")
        eml = self.request.get("email")
        username = self.valid_username(self.request.get("username"))
        passw = self.valid_password(self.request.get("password"), self.request.get("verify"))
        email = self.valid_email(self.request.get("email"))

        if  username and  passw and email :
            self.redirect('/welcome?username='+user)
        else:
            self.response.write(form %{"em":self.em,"name":self.name,"username_error":self.username_error,
                                       "password_error" : self.password_error, "verify_error":self.verify_error, "email_error" :self.email_error})

class TestHandler(webapp2.RequestHandler):

    def get(self):
        user_loged = self.request.get("username")
        self.response.write("Welcome, "+user_loged+"!")

app = webapp2.WSGIApplication([
    ('/signup', MainHandler),
    ('/welcome', TestHandler)
], debug=True)

