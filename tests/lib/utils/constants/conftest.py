"""Configuring Test Cases for testing of interfaces"""

from pytest import fixture


@fixture
def genders():
    """Testing the Enumeration of User Genders"""

    return ["male", "female", "other"], ["m", "f", "o"]


@fixture
def statuses():
    """Testing the Enumeration of Email Account Statuses"""

    return [
        "active",
        "inactive",
        "suspended",
        "disabled",
        "deleted",
        "new",
        "unverified",
        "verified",
    ]


@fixture
def roles():
    """Testing the Enumeration of User Roles"""

    return [
        "Super Administrator",
        "System Administrator",
        "Application Tester",
        "Application User",
        "Application developer",
    ]


@fixture
def email_status():
    """Testing Enumeration of Email Verification Statuses"""

    return [
        "New and Unverified",
        "Verified",
        "Verification Requested",
        "Verification Failed",
        "Verification Request Expired",
    ]


@fixture
def permissions():
    """Testing the Enumeration of User Device Permissions"""

    return [
        "camera",
        "STORAGE",
        "contacts",
    ]


@fixture
def login_methods():
    """Testing the Enumeration of User Login Methods"""
    return [
        "User Email and Password",
        "Github SSO",
        "Slack SSO",
        "Google SSO",
        "Facebook SSO",
    ]


@fixture
def communications():
    """Testing the Enumeration of User Communication Perferences"""

    return [
        "Email Messenger",
        "SMS",
        "Mobile Phone",
        "Slack Messenger",
    ]


@fixture
def occupations():
    """Testing the Enumeration of User Occupation Perferences"""

    return [
        "Software Engineer",
        "Hardware Engineer",
        "Electrical Engineer",
        "Mechanical Engineer",
        "Civil engineer",
        "Biomedical Engineer",
        "Doctor",
        "Nurse",
        "Teacher",
        "Professor",
        "Artist",
        "Musician",
        "Writer",
        "Accountant",
        "Lawyer",
        "Police Officer",
        "Firefighter",
        "Chef",
        "Architect",
        "Scientist",
        "Student",
        "Retiree",
        "Entrepreneur",
        "Athlete",
        "Journalist",
        "Designer",
        "Pharmacist",
        "Social Worker",
        "Other",
    ]
