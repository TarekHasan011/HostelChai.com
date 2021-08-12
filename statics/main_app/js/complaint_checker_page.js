let complaint_id_selector = $('#complaint_id');

$('#load').attr('href', $(complaint_id_selector).val());

$(complaint_id_selector).on('change', function() {
    $('#load').attr('href', $(this).val());
});
