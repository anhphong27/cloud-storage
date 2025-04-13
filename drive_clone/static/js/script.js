function login(){
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(`/api/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json()).then(data => {
        if (data.status === 200) {
            window.location.href = data.redirect;
        }else {
            alert(data.message);
        }
    });
};

function register() {
    const name = document.getElementById('name').value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById('confirm_password').value

    fetch(`/api/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password,
            confirm_password : confirm_password
        })
    })
    .then(response => response.json()).then(data => {
        if (data.status === 200) {
            alert(data.message);
            window.location.href = data.redirect;
        }else {
            alert(data.message);
        }
    });
};

function upload_file(event) {
    let fileInput = event.target;
    let file = fileInput.files[0];

    if (!file) return;

    let formData = new FormData();
    formData.append("file", file);

    fetch("/api/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            window.location.href = "/main";
        } else {
            alert(data.message);
        }
    });
};

function download_file(url){
    window.location.href = url;
}


function delete_file(file_id){
    if (!confirm("Bạn có chắc chắn muốn xóa file này không?")) {
        return;
    }

    fetch(`/api/delete_file/${file_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json()).then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        }else {
            alert(data.message);
        }
    });
};


function openRenameModal(fileId, currentName) {
        fileIdToRename = fileId;
        document.getElementById('newFileName').value = currentName;
        document.getElementById('renameModal').classList.remove('hidden');
    }

function closeRenameModal() {
    document.getElementById('renameModal').classList.add('hidden');
}

function confirmRename() {
    let newName = document.getElementById('newFileName').value.trim();
    if (!newName) {
        alert("Tên file không được để trống!");
        return;
    }
    fetch(`/api/rename_file/${fileIdToRename}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ new_name: newName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert("Có lỗi xảy ra: " + data.message);
        }
    });
};

function pay(size,price){
    fetch(`/create_checkout_session`,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            size: size,
            price: price
        })
    }).then(response => response.json()).then(data => {
        if (data.success){
            window.location.href = data.checkout_url;
        }else{
            alert(data.error)
        }
    })
};
