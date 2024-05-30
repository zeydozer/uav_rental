var table = new DataTable('#uav-table', {
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": "/api/uavs",
        "type": "GET",
        "data": function (d) {
            return $.extend({}, d, {
                "search": $("[type=search]").val(),
                "length": d.length,
                "start": d.start / d.length + 1,
                "ordering": master.order(d).replace('.', '__'),
                "brand": $("#uav-table [name=brand]").val(),
                "model": $("#uav-table [name=model]").val(),
                "weight": $("#uav-table [name=weight]").val(),
                "category": $("#uav-table [name=category]").val()
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
        { "data": "brand" },
        { "data": "model" },
        { "data": "weight" },
        { "data": "category" },
        { "data": "id" },
        { "data": "id" },
        { "data": "id" },
    ],
    "pageLength": 10,
    "columnDefs": [{
        "targets": [4],
        "render": function (data) {
            return `<button class="btn btn-info" onclick="uav.get(${data})">Edit</button>`
        }
    }, {
        "targets": [5],
        "render": function (data) {
            return `<button class="btn btn-danger" onclick="uav.delete(${data})">Del</button>`
        }
    }, {
        "targets": [6],
        "render": function (data) {
            return `<button class="btn btn-warning" onclick="uav.rent(${data})">Rent</button>`
        }
    }],
    "order": [[0, 'asc']],
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
let uav = {
    get: function (id) {
        $.ajax({
            type: 'GET',
            url: '/api/uavs/' + id,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
            },
            success: function (resp) {
                $('#edit-data').modal('show').attr('data-id', resp.id)
                $('#edit-data [name="brand"]').val(resp.brand)
                $('#edit-data [name="model"]').val(resp.model)
                $('#edit-data [name="weight"]').val(resp.weight)
                $('#edit-data [name="category"]').val(resp.category)
            }
        })
    },
    editOrAdd: function (_this) {
        let id = $('#edit-data').attr('data-id'),
            url = id != '' ?
            '/api/uavs/' + id :
            '/api/uavs'
        $.ajax({
            type: id != '' ?
                'PUT' :
                'POST',
            url: url,
            data: new FormData(_this),
            processData: false,
            contentType: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
            },
            success: function (resp) {
                master.alert('success', id != '' ? 'Uav updated...' : 'Uav created...')
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
    delete: function (id) {
        $.ajax({
            type: 'DELETE',
            url: '/api/uavs/' + id,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
            },
            success: function (resp) {
                table.draw()
            }
        })
    },
    rent: function (_this, confirm = false) {
        if (!confirm)
            $('#rent-data').attr('data-id', _this).modal('show')
        else {
            let id = $('#rent-data').attr('data-id')
            $.ajax({
                type: 'POST',
                url: '/api/uavs/'+ id +'/rent',
                data: new FormData(_this),
                processData: false,
                contentType: false,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization', 'Bearer ' + TOKEN.access)
                },
                success: function (resp) {
                    master.alert('success', 'Uav rented...')
                    setTimeout(() => {
                        $('#rent-data').modal('hide')
                        table.draw()
                    }, 3000)
                },
                error: function () {
                    master.alert('danger', 'Something went wrong!')
                }
            })
        }
    }
}

$('#edit-data').on('show.bs.modal', function () {
    $(this).find('input').val(null)
    $(this).attr('data-id', '')
    $(this).find('.modal-title').text('-')
})

$('#edit-data').on('shown.bs.modal', function () {
    let id = $(this).attr('data-id')
    $(this).find('.modal-title').text(id != '' ? 'Edit Uav' : 'Add Uav')
})