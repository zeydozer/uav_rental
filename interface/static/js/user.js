// 👤 User Authentication Functions
let user = {
    // 🚨 Show alert messages
    alert: function (type, message) {
        $('.alert').addClass('alert-' + type).html(message).show()
        setTimeout(() => {
            $('.alert').removeClass('alert-' + type).hide()
        }, 3000)
    },
    // 🔐 User login
    login: function (_this) {
        $.ajax({
            type: 'POST',
            url: '/api/login',
            data: new FormData(_this),
            processData: false,
            contentType: false,
            success: function (resp) {
                user.alert('success', 'Logging in...')
                localStorage.setItem('token', JSON.stringify(resp))
                setTimeout(() => {
                    location.reload()
                }, 3000)
            },
            error: function () {
                user.alert('danger', 'Something went wrong!')
            }
        })
    },
    // 📝 User registration
    register: function (_this) {
        $.ajax({
            type: 'POST',
            url: '/api/register',
            data: new FormData(_this),
            processData: false,
            contentType: false,
            success: function (resp) {
                user.alert('success', 'You have registered, you are directed to the login...')
                setTimeout(() => {
                    location.href = '/login'
                }, 3000)
            },
            error: function () {
                user.alert('danger', 'Something went wrong!')
            }
        })
    }
}