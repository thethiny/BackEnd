from Requests.outlook.values import __email
import os, requests

# Get token from environment and store it in dictionary
auth = {"Authorization": os.getenv("TOKEN")}

# Get account URL from environment and store it
url = os.getenv("ACCOUNT")


# General function to send an email using Zoho API
def email(sender, recipient, subject, body):
    # Post a request with token in the header and return status
    return requests.post(url, headers=auth, json={
        # Specify sender and recipient
        "fromAddress": sender,
        "toAddress": recipient,
        # Specify email subject and body
        "subject": subject,
        "content": body
    }).status_code


# Sends a email announcement about a grade of a course
def grade_announcement(sid, course, grade):
    # Store grade article as "an" for (A, F) or "a" for other grades
    article = "an" if grade == "A" or grade == "F" else "a"
    # Send the email
    return email(
        # Sender is UOS HUB NO-REPLY
        "UOS HUB <no-reply@uoshub.com>",
        # Recipient is the student
        __email(sid),
        # Email subject and body details the grade and the course
        "You got " + article + " " + grade + " in " + course,
        "This is an automated notification from uoshub.com<br><br>" +
        "It is to inform you that you got " + article + " <b>" + grade + "</b> in <b>" + course + "</b>"
    )


# Sends a email announcement about subscription and grades so far
def grades_summary(sid, courses, gpa):
    return email(
        # Sender is UOS HUB NO-REPLY
        "UOS HUB <no-reply@uoshub.com>",
        # Recipient is the student
        __email(sid),
        # Email subject
        "Subscribed to UOS HUB!",
        # Email body contains grades and GPA details
        "<br>".join([
            "Thank you for subscribing to UOS HUB Grades Checker,",
            "You'll get another email whenever a new grade comes out.<br><br>"
        ] + ([
            "For now, here's a summary for what's already out:<br>",
            "<b>Term grades so far:</b>",
            *[f"{course[1]}: {course[2]}" for course in sorted(courses, key=lambda course: len(course[1]))],
            f"<br><b>Term GPA so far</b>: {gpa['term']:.2f}",
            f"Cumulative GPA without this term was: {gpa['old']:.2f}",
            f"Cumulative GPA with this term so far is: <b>{gpa['new']:.2f}</b>"
        ] if courses else [
            "None of this term's grades have come out yet.",
            f"Your Cumulative GPA without this term is: {gpa['old']:.2f}"
        ]))
    )
