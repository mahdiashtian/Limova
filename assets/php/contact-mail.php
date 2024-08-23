<?php

    // Only process POST reqeusts.
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Get the form fields and remove whitespace.
        $f_name = strip_tags(trim($_POST["name"]));
				$f_name = str_replace(array("\r","\n"),array(" "," "),$f_name);
        $f_email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
        $f_subject = trim($_POST["subject"]);
        $f_message = trim($_POST["message"]);

        // Check that data was sent to the mailer.
        if ( empty($f_name) OR empty($f_message) OR !filter_var($f_email, FILTER_VALIDATE_EMAIL)) {
            // Set a 400 (bad request) response code and exit.
            http_response_code(400);
            echo "Please complete the form and try again.";
            exit;
        }

        // Set the recipient email address.
        // FIXME: Update this to your desired email address.
        $recipient = "admin@devitems.com";

        // Set the email subject.
        $subject = "New contact from $f_name";

        // Build the email content.
        $email_content = "Name: $f_name\n";
        $email_content .= "Email: $f_email\n\n";
        $email_content .= "Email: $f_subject\n\n";
        $email_content .= "Message:\n$f_message\n";

        // Build the email headers.
        $email_headers = "From: $f_name <$f_email>";

        // Send the email.
        if (mail($recipient, $subject, $email_content, $email_headers)) {
            // Set a 200 (okay) response code.
            http_response_code(200);
            echo "Thank You! Your message has been sent.";
        } else {
            // Set a 500 (internal server error) response code.
            http_response_code(500);
            echo "Oops! Something went wrong and we couldn't send your message.";
        }

    } else {
        // Not a POST request, set a 403 (forbidden) response code.
        http_response_code(403);
        echo "There was a problem with your submission, please try again.";
    }

?>
