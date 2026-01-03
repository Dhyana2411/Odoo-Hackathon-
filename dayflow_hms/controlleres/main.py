from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request
import odoo.http as http

class DayflowSignup(AuthSignupHome):
    
    def do_signup(self, qcontext):
        # This function runs when you click "Sign Up" button
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password')}
        
        # Capture our custom fields
        values['role_selection'] = qcontext.get('role_selection')
        
        # If they entered a company name, we might want to update their user later
        # For the hackathon, we just ensure the user is created successfully
        super(DayflowSignup, self).do_signup(qcontext)