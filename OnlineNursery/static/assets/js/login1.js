const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const signUpButton1 = document.getElementById('sellersignUp');
const signInButton2 = document.getElementById('sellersignIn');
const container = document.getElementById('container');
const container1 = document.getElementById('container1');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

signUpButton1.addEventListener('click', () => {
    container1.classList.add("right-panel-active");
});

signInButton2.addEventListener('click', () => {
    container1.classList.remove("right-panel-active");
});
var maxTry = 3;

function validate() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    //empty field validation
    if(username == ""|| password == "")
    {
        alert("Please check your Credentials");
    }
    
    //if name and password match
    if (username == "" && password == "") { 
        window.location = "./index.html";
        return false;
    }
    //code for try upto 3 chance then disable username and password field
    else {
        maxTry--;
        if (maxTry == 0) {
            document.getElementById("username").disabled = true;
            document.getElementById("password").disabled = true;
            document.getElementById("submit").disabled = true;
            return false;
        }
    }
}


function matchPassword() {
    var pw1 = document.getElementById("password");
    var pw2 = document.getElementById("password2");
    if (pw1 != pw2) {
        alert("Passwords did not match");
    } else {
        alert("Password created successfully");
    }
}
