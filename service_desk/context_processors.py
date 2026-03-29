"""
Context processors for the Service Desk application.

This module provides context processors that automatically inject
user role information into every template context.
This eliminates the need to pass role flags (is_agent, is_admin) manually from views.

Available context variables:
  - is_admin: True if the current user belongs to the 'Admins' group
  - is_supervisor: True if the current user belongs to the 'Supervisors' group
  - is_agent: True if the current user belongs to the 'Agents' group
  - is_customer: True if the current user belongs to the 'Customers' group
  - is_manager: True if the current user belongs to the 'Managers' group
"""

def user_roles(request):
    roles = {
        'is_admin': False,
        'is_supervisor': False,
        'is_agent': False,
        'is_customer': False,
        'is_manager': False,
    }

    if request.user.is_authenticated:
        groups = request.user.groups.values_list('name', flat=True)
        roles = {
            'is_admin': 'Admins' in groups,
            'is_supervisor': 'Supervisors' in groups,
            'is_agent': 'Agents' in groups,
            'is_customer': 'Customers' in groups,
            'is_manager': 'Managers' in groups,
        }

        return roles
    return roles