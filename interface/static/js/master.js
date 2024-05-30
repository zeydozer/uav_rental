const TOKEN = JSON.parse(localStorage.getItem('token'))

let master = {
    alert: function (type, message) {
        $('.alert').addClass('alert-' + type).html(message).show()
        setTimeout(() => {
            $('.alert').removeClass('alert-' + type).hide()
        }, 3000)
    },
    logout: function () {
        localStorage.removeItem('token')
        location.reload()
    },
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
    order: function (d) {
        if (d.order && d.order.length) {
            var columnIdx = d.order[0].column
            var dir = d.order[0].dir
            var columnName = d.columns[columnIdx].data
            return (dir === 'desc' ? '-' : '') + columnName
        }
        return ''
    },
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