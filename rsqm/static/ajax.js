$(function(){

    $('#search_s').keyup(function(){

        $.ajax({
            type: "POST",
            url: "/supplier/search/",
            data: {
                'search_text' : $('#search_s').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#search_results').html(data);
}