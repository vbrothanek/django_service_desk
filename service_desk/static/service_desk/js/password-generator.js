function generatePassword(length = 12) {
    const lowercaseChars = 'abcdefghijklmnopqrstuvwxyz';
    const uppercaseChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const numberChars = '0123456789';
    const symoblChars = '!@#$%^&*_+?.';

    const allChars = lowercaseChars + uppercaseChars + numberChars + symoblChars;

    let password = '';

    password += lowercaseChars.charAt(Math.floor(Math.random() * lowercaseChars.length));
    password += uppercaseChars.charAt(Math.floor(Math.random() * uppercaseChars.length));
    password += numberChars.charAt(Math.floor(Math.random() * numberChars.length));
    password += symoblChars.charAt(Math.floor(Math.random() * symoblChars.length));

    for (let n = password.length; n < length; n++) {
        password += allChars.charAt(Math.floor(Math.random() * allChars.length));
    }

    password = password.split('').sort(() => 0.5 - Math.random()).join('')

    return password;

}

const generateButton = document.getElementById('pwd-gen');
const passwordField = document.getElementById('generated-password');

generateButton.addEventListener('click', e => {
    const newPassword = generatePassword(12)
    passwordField.innerHTML = newPassword
})

//	<div>
// 		<button class="btn btn-primary" id="pwd-gen" type="button" >Generate</button>
// 		<p>Generated password</p>
// 		<span id="generated-password"></span>
// 	</div>