document.addEventListener('DOMContentLoaded', function() {

    $('#search_input').keyup(function(event){
        var query = ($("#search_input").val());
        console.log(query)

        if (query != '' || query !=' '){
            $.ajax({
            type: "GET",
            url: "search",
            data: {
                'q' : query,
                'csrfmiddlewaretoken' : '{{ csrf_token }}'
            },
            success: function(data) {
                $('#main-results-search').html(data);
            },
            error: function(data){
                console.log(data);
            }
        });    

        }
  
    });
});