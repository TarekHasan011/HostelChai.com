$('.custom-file-input').on('change',function(){
    let splited_parts = $(this).val().split('\\');
    $(this).next('.custom-file-label').html(splited_parts[splited_parts.length-1]);
});
