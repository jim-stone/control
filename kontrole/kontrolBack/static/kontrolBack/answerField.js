$(document).ready(

    function () {       
        $(".toggler").click (
            function() {
                $(".comment").toggle();
                $(this).text(
                    function(newText, currentText) {
                        return currentText === "Ukryj komentarze" ? "Pokaż komentarze" : "Ukryj komentarze"
                    });
            }
        )
    }
);