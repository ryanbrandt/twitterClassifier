    $(document).on('submit', '.keyword-form', function(event) {
        event.preventDefault();
        var keyword = $(this).serializeArray()[0];
        sendKeyword(keyword);
        document.getElementById('form').reset();
        $(document.getElementById('stream-list')).empty();
        document.getElementById('chartContainer').innerHTML = "";
        document.getElementById('stream-header').innerHTML = "";
        // push loader into DOM
        var loader = document.getElementById('loader');
        loader.style.display = "block";
        loader.style.border = "16px solid #f3f3f3";
        loader.style.borderTop = "16px solid #3498db";
        loader.style.borderRadius = "50%";
        loader.style.width = "120px";
        loader.style.height ="120px";
        loader.style.animation = "spin 2s linear infinite";
        document.getElementById('load-text').innerHTML = '<p style="font-style: italic;">' + "Fetching tweets... (This will take about 15-seconds)" + '</p>';

    });

    function sendKeyword(keyword){
        $.ajax({
            url: home,
            type: "POST",
            data: {'keyword': keyword},

            // clear loader, push tweets and chart into DOM
            success: function(data){
                document.getElementById('loader').style.display = 'none';
                document.getElementById('load-text').innerHTML = "";
                document.getElementById('stream-header').innerHTML = 'Stream';
                var list = document.getElementById('stream-list');
                if(typeof data[0] == 'undefined'){
                    $(list).prepend('<p style="font-style: italic;">' + "Hmmm... couldn't find any tweets for that keyword, try another?" + '</p>');

                } else {

                    var tweets = data[0];
                    var pos = data[1];
                    var neg = data[2];
                    var overall = data[3];
                    var neuPct = data[4];
                    var posPct = data[5];
                    var negPct = data[6];
                    for(var i = 0; i < tweets.length; i++){
                        $(list).prepend('<li style="list-style-type: none;">' + tweets[i] + '<br/>' + '<strong>' + "positive: " + '</strong>' +  pos[i] + '<br/>' + '<strong>' + " negitive: " + '</strong>' + neg[i] + '<br/>' + '<strong>' + "overall: " + '</strong>' + overall[i] + '</li>' + '<br/>');
                    }
                    var chart = new CanvasJS.Chart("chartContainer", {
                        animationEnabled: true,
                        title: {
                            text: "Overall Sentiment"
                        },
                        data: [{
                            type: "pie",
                            startAngle: 240,
                            yValueFormatString: "##0.00\"%\"",
                            indexLabel: "{label} {y}",
                            dataPoints: [
                                {y: neuPct, label: "Neutral"},
                                {y: posPct, label: "Positive"},
                                {y: negPct, label: "Negative"}
                            ]
                        }]
                    });
                    chart.render();
                }
            },
            error: function(status){
                console.log('err ' + status);
            }
        })
    };