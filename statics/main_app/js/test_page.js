
function load_data(e) {
    e.preventDefault();

    let hostel_id = document.getElementById('hostel_id').value;

    xhr = new XMLHttpRequest();
    xhr.open('POST', '')
}

document.getElementById('load_hostel').addEventListener('submit', load_data);
