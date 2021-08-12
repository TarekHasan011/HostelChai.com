let date = new Date();
$('.dob').val(date.toISOString().split('T')[0]);

let student_registration_form = $('#student_registration');
let hostel_owner_registration_form = $('#hostel_owner_registration');

// student_registration_form.attr('disabled', true);
//
// student_registration_form.on('click', function () {
//     $(this).attr('disabled', true);
//     hostel_owner_registration_form.attr('disabled', false)
// });
//
// hostel_owner_registration_form.on('click', function () {
//     $(this).attr('disabled', true);
//     student_registration_form.attr('disabled', false)
// });