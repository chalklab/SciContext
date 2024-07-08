$(document).ready(function() {
    $('#alias').on('blur', function() {
        // for form in template onts/add.html
        let input = $('#alias');
        let nss = $('#aliases').html();
        let ns = input.val();
        if (nss.includes(ns)) {
            input.val('');
            alert('Alias already in use');
        }
        return false;
    });

    $('.olsont').on('click', function() {
        // for ols ont list in template onts/add.html
        let ont = $(this);
        let meta = ont.attr('data-ont').split("*");
        let nss = $('#aliases').html();
        if (nss.includes(':' + meta[1].toLowerCase() + ':')) {
            alert('An ontology with this namespace is already in use');
        } else {
            $('#name').val(meta[0]);
            $('#alias').val(meta[1]);
            $('#path').val(meta[2]);
            $('#homepage').val(meta[3]);
        }
        return false;
    });

    // for ols ont list in template terms/add.html
    $('#olsont').on('change', function() {
        let ontid = $('#olsont option:selected').val();
        $.ajax({
            type: 'POST',
            dataType: "json",
            context: document.body,
            url: 'http://127.0.0.1:8001/terms/js/' + ontid,
            success: function (data) {
                let terms = data['terms'];
                let cnt = terms.length;
                let div = $("#terms");
                div.html('');
                for(let i = 0; i<cnt; i++) {
                    let term = terms[i];
                    let btn = '<input class="btn btn-sm btn-success terms m-1" data-alias="' + ontid + '" data-code="' + term[3] + '" data-defn="' + term[2] + '" type="button" title="' + term[1] + '" value="' + term[1] + '">'
                    div.append(btn);
                }
                return false;
                },
            error: function () {
                alert("Error");
                return false;
            }
        });
    });

    // populate onto term from ontology button on
    $('#terms').on('click','.terms', function() {
        // set event to fire on parent of dynamically added dom element ('.term')
        let term = $(this);
        let title = term.val();
        let nsid = term.attr('data-alias');
        let code = term.attr('data-code');
        let defn = term.attr('data-defn');
        $('#title').val(title);
        $('#definition').val(defn);
        $('#code').val(code);
        $('#nsid').val(nsid);
        return false;
    });

    // show a new field entry...
    $("#showcwk").on('click', function () {
        let table=$(this).attr('data-table');
        let type=table.substring(0,table.length-1);
        let nnum=$("." + type).length;
        let clone=$("#" + type + "0").clone(true,true);
        clone.attr('id',type + nnum);
        clone.attr('data-nnum',nnum);
        clone.removeClass('invisible');
        clone.removeClass('collapse');
        clone.find("#index" + nnum).text(nnum); // table field
        clone.find("#tbl0").attr('id','tbl' + nnum); // table field
        clone.find("#fld0").attr('id','fld' + nnum); // 'field' field
        clone.find("#trm0").attr('id','trm' + nnum); // ont term field
        clone.find("#sec0").attr('id','sec' + nnum); // section field
        clone.find("#typ0").attr('id','typ' + nnum); // aspect/facet type field
        clone.find("#cat0").attr('id','cat' + nnum); // category field
        clone.find("#dtp0").attr('id','dtp' + nnum); // datatype field
        clone.insertAfter("div." + type + ":last");
    });

    // add/update a new field entry...
    $(".updfld").on('change', function () {
        let input = $(this);
        let field = input.attr('id');
        let form = input.closest('form');
        let fldid = form.attr('data-fldid')
        let ctxid = form.attr('data-ctxid')
        let value = input.val();
        // if dbid is empty create new entry in fields table
        let url = '/fields/add/';
        $.ajax({
            type: 'POST',
            dataType: "json",
            context: document.body,
            url: url,
            data: {fldid: fldid, cxtid: ctxid, field: field, value: value},
            success: function (resp) {
                // note term title and url put in temp field (title|url)
                let html = '<b>' + resp.field + ' -> </b>';
                if(resp.newname) {
                    html += ' ' + resp.newname;
                } else {
                    html += ' ' + resp.field;
                }
                html += ' (' + resp.datatype + ')';
                if(resp.temp) {
                    let temp = resp.temp.split('|');
                    html += ' means <em>' + temp[0] + '</em> [' + temp[1] + ']';
                }
                if(!fldid) {
                    // set the field id if it was not set (new entry)
                    $('#modalform').attr("fldid",resp.id);
                    // add the new entry to the page
                    let newitem = '<div class="col-11 pr-0">';
                    newitem += '<a id="fld' + resp.id + '" class="editfld list-group-item items py-1" data-fldid="' + resp.id + '" data-toggle="modal" data-target="#fldmodal" style="cursor: pointer;">' + html + '</a>';
                    newitem += '</div><div class="col-1 pl-0">';
                    newitem += '<button class="btn btn-sm btn-danger delcwk col-12" data-fldid="' + resp.id + '" title="Delete">X</button>'
                    newitem += '</div>';
                    $("#flds").append(newitem);
                } else {
                    $('#fld' + fldid).html(html);
                }
                return false;
            },
            error: function () {
                alert("Error");
                return false;
            }
        });
        return false;
    });

    // remove a field entry
    $(".delcwk").on('click', function () {
        let cwk = $(this);
        let cwkid = cwk.attr('cwkid');
        $.post('/xwalks/delete/', {cwkid: cwkid})
            .done(function ( data ) {
                // hide dom elements
                if(data['response']==='success') {
                    $(".editcwk[cwkid='" + cwkid + "']").hide();
                    $(".delcwk[cwkid='" + cwkid + "']").hide();
                    alert("Field deleted :)");
                } else {
                    alert("Deletion error :(");
                }
            });
        return false;
    });

    // search and show/hide terms in card
    $("#btnsrc").on('keyup',function(){
        let val=$(this).val().toLowerCase().trim();
        let items=$('.items');
        let terms=$('.terms');
        let delbtns=$('.delcwk');
        items.show(); // for html elements that have content inside the element
        terms.show(); // for buttons (with attr 'value')
        delbtns.show(); // for fields to also hide delete buttons along with <a> links
        console.log(val);
        if(val!=='') {
            terms.not('[value*="' + val + '"]').hide();
            let nomatch = items.not(':contains(' + val + ')')
            nomatch.each(function (i, el) {
                let item=$(el);
                $(".delcwk[cwkid='" + item.attr('cwkid') + "']").hide();
            });
            nomatch.hide();
        }
    });

    // search and show/hide terms in card
    $("#listsrc").on('keyup',function(){
        let val=$(this).val().toLowerCase().trim();
        let items=$('.item');
        items.show();
        if(val!=='') {
            items.not('[data-content*="' + val + '"]').hide();
        }
    });

    // create context JSON-LD file
    $("#createctx").on('click', function () {
        let id = $("#createctx").attr('dbid');
        $.get('/contexts/write/' + id).done(function() { alert( "Context file saved :)" ); });
        return false;
    });

    // config the modal for a new field entry
    $("#addfld").on('click', function () {
        // clear form
        let form = $('#modalform');
        form[0].reset();
        form.attr('data-fldid','');
        form.attr('data-ctxid','');
        // process
        let btn = $(this);
        let ctxid = btn.attr('data-ctxid');
        form.attr("data-ctxid",ctxid);
    });

    // edit a field entry
    $(".editfld").on('click', function () {
        let fld = $(this);
        let fldid = fld.attr('fldid');
        $.get('/fields/read/' + fldid, function( fdata ) {
            let form = $('#modalform');
            form.attr("fldid",fldid);
            form.attr("cxtid",fdata.context);
            $('#table').val(fdata.table).attr('old',fdata.table);
            $('#field').val(fdata.field).attr('old',fdata.field);
            $('#term_id').val(fdata.term);
            $('#category').val(fdata.category).attr('old',fdata.category);
            $('#datatype').val(fdata.datatype);
            return false;
        });
    });

    // focus modal to first input field on open
    $('#cwkmodal').on('shown.bs.modal', function () {
        $('#table').trigger('focus')
    });

    // load ontologies from an ontology server
    $('#loadonts').on('click', function () {
        let svrid = $(this).attr('data-dbid');
        $.get('/servers/ontupd/' + svrid, function( sdata ) {
            $('#debug').val(sdata);
        });
    });

    // load ontologies from an ontology server
    $('#loadtrms').on('click', function () {
        let svrid = $(this).attr('data-svrid');
        let ontid = $(this).attr('data-ontid');
        $.get('/onts/ontsee/' + svrid + '/' + ontid, function( tdata ) {
            $('#terms').val(tdata);
        });
    });

});