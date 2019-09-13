<!DOCTYPE html>
<html>
<head>
    <title>Ewan Miles | Thank you!</title>
    <link href="./Stylesheets/style.css" type="text/css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Catamaran&display=swap" rel="stylesheet">
</head>

<!--Send the email grabbing data from form-->
<?php 
if(isset($_POST['submit'])){
    $to = "ewan.a.miles@gmail.com"; //Recipient Email
    $from = $_POST['email']; //Sender Email
    $name = $_POST['name'];
    $subject = "Contact via ewanmiles.com";
    $subject2 = "A copy of your form submission on ewanmiles.com";
    $message = $name . " wrote the following:" . "\n\n" . $_POST['message'];
    $message2 = "Here is a copy of your message " . $name . ":\n\n" . $_POST['message'] . "\n\nThanks for emailing! I'll get back to you soon.";

    $headers = "From:" . $from;
    $headers2 = "From:" . $to;
    mail($to,$subject,$message,$headers);
    mail($from,$subject2,$message2,$headers2); //Sends a copy of the message to the sender
    }
?>

<body>
    <div id="center" class="form">
        <h2>Your mail has been sent. Thanks for getting in touch!</h2>
        <a href="./home.php"><p>Back to Ewan's CV</p></a>
    </div>

    <div class="footer sent">
        <h4>Ewan Miles</h4>
        <h4>Copyright © ewanmiles.com</h4>
        <h4><span id="time"></span></h4>
    
        <!--Script for date in footer-->
        <script>
        var today = new Date();
        document.getElementById('time').innerHTML=today;
        </script>  

    </div>
</body>
</html>
