var table = new DataTable('#rental-table', {
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": "/api/rentals",
        "type": "GET",
        "data": function (d) {
            return $.extend({}, d, {
                "search": $("[type=search]").val(),
                "length": d.length,
                "start": d.start / d.length + 1,
                "ordering": master.order(d).replace('.', '__'),
                "uav__brand": $("#rental-table [name=uav]").val(),
                "renting_member__username": $("#rental-table [name=member]").val(),
                "start_date": $("#rental-table [name=start]").val(),
                "end_date": $("#rental-table [name=end]").val()
            })
        },
        "beforeSend": function (xhr) {
            xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
        },
        "error": function (xhr) {
            if (xhr.status == 401)
                master.refresh()
        }
    },
    "columns": [
        { "data": "uav.brand" },
        { "data": "renting_member.username" },
        { "data": "start_date" },
        { "data": "end_date" },
        { "data": "id" },
        { "data": "id" },
    ],
    "pageLength": 10,
    "columnDefs": [{
        "targets": [2, 3],
        "render": function (data) {
            return new Date(data).toDateString()
        }
    }, {
        "targets": [4],
        "render": function (data) {
            return `<button class="btn btn-info" onclick="rental.get(${data})">Edit</button>`
        }
    }, {
        "targets": [5],
        "render": function (data) {
            return `<button class="btn btn-danger" onclick="rental.delete(${data})">Del</button>`
        }
    }],
    "order": [[2, 'asc']],
    "initComplete": function () {
        $('tfoot input').addClass('form-control')
    },
    "language": {
        "lengthMenu": "_MENU_",
        "search": ""
    }
})
$(document).on('keyup', 'tfoot input', master.delay(function () {
    table.draw()
}, 1000))
let rental = {
    get: function (id) {
        $.ajax({
            type: 'GET',
            url: '/api/rentals/' + id,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
            },
            success: function (resp) {
                $('#edit-data').attr('data-id', resp.id).modal('show')
                $('#edit-data [name="uav_id"]').val(resp.uav.id)
                $('#edit-data [name="renting_member_id"]').val(resp.renting_member.id)
                $('#edit-data [name="start_date"]').val(new Date(resp.start_date).toISOString().substr(0, 16))
                $('#edit-data [name="end_date"]').val(new Date(resp.end_date).toISOString().substr(0, 16))
            }
        })
    },
    edit: function (_this) {
        let id = $('#edit-data').attr('data-id')
        $.ajax({
            type: 'PUT',
            url: '/api/rentals/' + id,
            data: new FormData(_this),
            processData: false,
            contentType: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
            },
            success: function (resp) {
                master.alert('success', 'Rental updated...')
                setTimeout(() => {
                    $('#edit-data').modal('hide')
                    table.draw()
                }, 3000)
            },
            error: function () {
                master.alert('danger', 'Something went wrong!')
            }
        })
    },
    vehicle: function () {
        $.ajax({
            type: 'GET',
            url: '/api/uavs',
            data: {
                length: 1000
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
            },
            success: function (resp) {
                let options = ``
                resp.data.forEach((v, i) => {
                    options += `<option value="${v.id}">${v.brand}</option>`
                })
                $('#edit-data [name="uav_id"]').html(options)
            }
        })
    },
    member: function () {
        $.ajax({
            type: 'GET',
            url: '/api/users',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
            },
            success: function (resp) {
                let options = ``
                resp.forEach((v, i) => {
                    options += `<option value="${v.id}">${v.username}</option>`
                })
                $('#edit-data [name="renting_member_id"]').html(options)
            }
        })
    },
    delete: function (id) {
        $.ajax({
            type: 'DELETE',
            url: '/api/rentals/' + id,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
            },
            success: function (resp) {
                table.draw()
            }
        })
    }
}
rental.vehicle()
rental.member()