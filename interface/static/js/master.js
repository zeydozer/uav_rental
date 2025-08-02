const TOKEN = JSON.parse(localStorage.getItem('token'))

// 🎯 Master utilities and common functions
let master = {
    // 🚨 Show alert messages
    alert: function (type, message) {
        $('.alert').addClass('alert-' + type).html(message).show()
        setTimeout(() => {
            $('.alert').removeClass('alert-' + type).hide()
        }, 3000)
    },
    // 🚪 Logout user
    logout: function () {
        localStorage.removeItem('token')
        location.reload()
    },
    // 🔄 Refresh JWT token
    refresh: function () {
        $.ajax({
            type: 'POST',
            url: '/api/refresh',
            data: {
                'refresh': TOKEN.refresh
            },
            success: function (resp) {
                TOKEN.access = resp.access
                localStorage.setItem('token', JSON.stringify(TOKEN))
                location.reload()
            },
            error: function () {
                location.href = '/login'
            }
        })
    },
    // 📊 Handle DataTable ordering
    order: function (d) {
        if (d.order && d.order.length) {
            var columnIdx = d.order[0].column
            var dir = d.order[0].dir
            var columnName = d.columns[columnIdx].data
            return (dir === 'desc' ? '-' : '') + columnName
        }
        return ''
    },
    // ⏱️ Delay function for search input
    delay: function (callback, ms) {
        var timer = 0
        return function () {
            var context = this, args = arguments
            clearTimeout(timer)
            timer = setTimeout(function () {
                callback.apply(context, args)
            }, ms || 0)
        }
    }
}