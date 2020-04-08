function checkLevel() {
    let selection = document.querySelector("#level");
    switch (selection.value) {
        case "0":
            alert("Please select your skill level");
            selection.focus();
            break;
        case "1":
            window.location.href = "welcome.html"
            break;
        case "2":
            alert("Our website is for Rookies!\nHere is a video for your skill level ...");
            window.open("https://www.youtube.com/watch?v=Onkt3mIAz5Q");
            break;
        case "3":
            alert("Our website is for Rookies!\nHere is a video for your skill level ...");
            window.open("https://www.youtube.com/watch?v=_logRee_e0w");
            break;
        case "4":
            alert("Our website is for Rookies!\nHere is a video for your skill level ...");
            window.open("https://www.youtube.com/watch?v=1KfmzTewWyI");
            break;
        case "5":
            alert("Our website is for Rookies!\nHere is a video for your skill level ...");
            window.open("https://www.youtube.com/watch?v=A2nSe2Yia60");
            break;
        case "6":
            alert("Our website is for Rookies!\nHere is a video for your skill level ...");
            window.open("https://www.youtube.com/watch?v=qXRnJhkZawc");
            break;
        default:
            console.log("def");
    }
}