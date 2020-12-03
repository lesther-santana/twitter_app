
setInterval(
    function () {
        $.getJSON(
            '/counters',
            {},
            function (data) {
                console.log(data);
            }
        )
    }
    ,20000);