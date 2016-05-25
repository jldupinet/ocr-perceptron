$( function() {
        $('td').click( function() {
                $(this).toggleClass("black-cell");
        } );
} );

function clearTable(){
        $("td").each(function() {
                $(this).removeClass();
        });
}

function getData(){
        var data = []
                $("td").each(function() {
                        if($(this).hasClass('black-cell')){
                                data.push(1);
                        } else{
                                data.push(0);
                        }
                });
        return data;
}

function recognizeMatrix(){
        matrixData = getData();
        $.post("recognize",JSON.stringify({ sensor: getData() }), function(data, status){
                // alert("Data: " + data['result'] + "\nStatus: " + status);
                $('#result').text(data['result']);                        
        });

}
