$(document).ready(function() {
    // populate the ontsel select with ontologies from the chosen server
    $('#svrsel').on('change', function() {
        let svrid = $('#svrsel option:selected').val();
        let spin = $('#spinner')
        let sel = $("#trm_ont");
        let src = $("#srcstr");
        spin.show();
        $.ajax({
            type: 'POST',
            dataType: "json",
            context: document.body,
            url: 'http://127.0.0.1:8001/onts/bysvr/' + svrid,
            success: function (data) {
                let cnt = data.length;
                for(let i = 0; i<cnt; i++) {
                    let ont = data[i];
                    let ostr = '<option value="' + ont['ns'] + '">' + ont['title'] + ' (' + ont['count'] + ')</option>'
                    sel.append(ostr);
                }
                sel.prop("disabled", false);
                src.prop("disabled", false);
                spin.hide();
                return false;
                },
            error: function () {
                alert("Error");
                return false;
            }
        });
    });

    // populate the terms div with terms from the chosen ontologoy
    $('#ontsel').on('change', function() {
        // NOTE: ontid here is the ontology namespace, not a DB id as the request is done on the server
        let ontid = $('#ontsel option:selected').val();
        let svrid = $('#svrsel option:selected').val();
        $.ajax({
            type: 'POST',
            dataType: "json",
            context: document.body,
            url: 'http://127.0.0.1:8001/terms/byont/' + svrid + '/' + ontid,
            success: function (data) {
                let cnt = data.length;
                let div = $("#terms");
                for(let i = 0; i<cnt; i++) {
                    let trm = data[i];
                    let btn = '<input class="btn btn-sm btn-success item m-1" data-svrid="' + svrid + '" data-code="' + trm['code'] + '" data-content="' + trm['label'] + '" type="button" title="' + trm['label'] + '" value="' + trm['label'] + '">'
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

    $('#alias').on('blur', function() {
        // for form in template onts/add.html
        let input = $('#alias');
        let nss = $('#aliases').html();
        let ns = input.val();
        if (nss.includes(':' + ns + ':')) {
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

    // add field to context
    $('#ctxfldadd').on('change', function () {
        let ctxid = $(this).find(":selected").val();
        let fldid = $("#fldid").data('fldid');
        // alert(ctxid + ":" + fldid);
        $.post('/fields/join/', {fldid: fldid, ctxid: ctxid})
            .done(function (data) {
                // hide dom elements
                if (data === 'success') {
                    window.location.replace("/fields/view/" + fldid);
                } else {
                    alert("Deletion error :(");
                }
            });
        return false;
    });

    // Remove: save field data in form before adding a new field ...
    $(".updfld").on('change', function () {
        let input = $(this);
        let name = $('#name').val();
        let trmid = $('#term_id').find(":selected").text();
        let cat = $('#category').val();
        let con = $('#container').find(":selected").text();
        let type = $('#type').find(":selected").text();

        let form = input.closest('form');
        let fldid = form.attr('data-fldid')
        let ctxid = form.attr('data-ctxid')
        let saved = form.attr('data-saved');
        saved = {"name": name, "trmid": trmid, "cat": cat, "con": con, "type": type};
        form.data('saved', saved);
        return false;
    });

    // remove a field entry
    $(".delctxfld").on('click', function () {
        let btn = $(this);
        let fldid;let ctxid;
        if(btn.find('.flddel')) {
            ctxid = btn.data('ctxid');
            fldid = $('#fldid').val()
            alert(fldid + ":" + ctxid)
        }
        if(btn.find('.ctxdel')) {
            fldid = btn.data('fldid');
            ctxid = $('#ctxid').val()
            alert(fldid + ":" + ctxid)
        }
        // alert(fldid + ":" + ctxid)
        return false;
        let token = $('input[name="csrfmiddlewaretoken"]').val();
        $.post('/fields/delete/', {fldid: fldid, ctxid: ctxid, csrfmiddlewaretoken: token})
            .done(function ( data ) {
                // hide dom elements
                if(data==='success') {
                    $(".editfld[fldid='" + fldid + "']").hide();
                    $(".delfld[fldid='" + fldid + "']").hide();
                    alert("Field removed from this context :)");
                } else {
                    alert("Deletion error :(");
                }
            });
        return false;
    });

    // search and show/hide terms in card
    $("#trmsrc").on('click',function(){
        let srcstr = $('#srcstr').val();
        let svrid = $('#svrsel option:selected').val();
        let div = $("#terms");
        let spin = $('#spinner');
        let sub = $('#subsrc');
        div.empty();  // remove previous search results
        spin.show();  // show spinner
        sub.hide();  // hide subsearch input in footer
        $.ajax({
            type: 'POST',
            dataType: "json",
            context: document.body,
            url: 'http://127.0.0.1:8001/terms/trmsrc/' + svrid + '/' + srcstr,
            success: function (data) {
                let cnt = data.length;
                for(let i = 0; i<cnt; i++) {
                    let trm = data[i];
                    let disp = '(<span class="emph_green">' + trm['ns'] + '</span>) [' + trm['code'] + '] ' +
                        trm['title'] + ': <em>' + trm['defn'] + '</em> (<span class="emph_red">' + trm['type'] + '</span>)';
                    let content = trm['title'].toLowerCase() + ' ' + trm['defn'].toLowerCase() + ' ' +
                        trm['ns'].toLowerCase() + trm['code'].toLowerCase()
                    let hit = '<a class="list-group-item item item-sm addtrm" data-svrid="' + svrid + '" data-code="' +
                        trm['code'] + '" data-title="' + trm['title'] + '" data-ns="' + trm['ns'] + '" data-defn="' +
                        trm['defn'] + '" data-ontid="' + trm['ontid'] + '" data-content="' + content + '" style="cursor: pointer;">' + disp + '</a>'
                    div.append(hit);
                }
                spin.hide();
                if(cnt>10) {
                    sub.show();
                }
                return false;
                },
            error: function () {
                alert("Error");
                return false;
            }
        });
    });

    // update the new term form with data from the server search
    $(document.body).on('click', '.addtrm', function(){
        // must use documentbody and 'selector' above as the <a> tags have been dynamically added to the DOM
        let trm = $(this);
        let code = trm.data('code');
        let title = trm.data('title');
        let defn = trm.data('defn');
        let ns = trm.data('ns');
        let ontid = trm.data('ontid');
        let svrid = $('#svrsel option:selected').val();
        $('#trm_title').val(title);
        $('#trm_defn').val(defn);
        $('#trm_code').val(code);
        $('#svrid').val(svrid);
        $('#ontid').val(ontid);
        $('#trm_ont option[value="' + ns + '"]').prop('selected', true);
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
        let ctxid = $("#createctx").data('ctxid');
        $.get('/contexts/write/' + ctxid).done(function() { alert( "Context file saved :)" ); });
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
        let fldid = fld.attr('data-fldid');
        $.get('/fields/read/' + fldid, function( fdata ) {
            let form = $('#fieldform');
            $('#name').val(fdata.name).data('old',fdata.name);
            $('#term_id').val(fdata.term_id).data('old',fdata.term_id);
            $('#category').val(fdata.category).data('old',fdata.category);
            $('#datatype').val(fdata.datatype).data('old',fdata.datatype);
            $('#container').val(fdata.container).data('old',fdata.container);
            $('#fldmodal').show()
            return false;
        });
    });

    // focus modal to first input field on open
    $('#fldmodal').on('shown.bs.modal', function () {
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