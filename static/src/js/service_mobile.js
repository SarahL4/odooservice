


odoo.define('service_mobile.index', function (require) {
    'use strict';


    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');

    //~ Odoos översättningsfunktion
    var _t = core._t;

    //~ Kontrollera att klass finns på sidan (inte ladda i onödan)
    if (!$('.service_mobile').length) { 
        return $.Deferred().reject("DOM doesn't contain '.service_mobile'");
    }



        // Hitta på sidan
    $('#table').on('click','.check', function (ev) {

        //~ If this method is called, the default action of the event will not be triggered.
        ev.preventDefault();

        var $link = $(ev.currentTarget);

        //~ Logga länken användaren klickade på
        console.log($link.data('href'));

        // href pekar unikt på respektive order, använder inloggning från sessionen när vi anropar vår controller /service/<model("sale.order"):order>/order/flag
        ajax.jsonRpc($link.data('href'), 'call', {})
            .then(function (data) {

                //~ Logga responsen från vår controller
                console.log(data);

                // Felhantering
                if(data.error) {
                    var $warning;
                    if(data.error === 'anonymous_user') {
                        $warning = $('<div class="alert alert-danger alert-dismissable oe_forum_alert" id="check_alert">'+
                            '<button type="button" class="close notification_close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
                            _t('Sorry you must be logged in to confirm an invoice') +
                            '</div>');
                    } else if(data.error === 'post_non_check') {
                        $warning = $('<div class="alert alert-danger alert-dismissable oe_forum_alert" id="check_alert">'+
                            '<button type="button" class="close notification_close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
                            _t('This invoice can not be confirmed') +
                            '</div>');
                    }

                    //~ Hitta meddelanderutan för länken
                    var flag_alert = $link.parent().find("#check_alert");

                    //~ Lägg in varningen i vår meddelanderuta
                    if (flag_alert.length === 0) {
                        $link.parent().append($warning);
                    }

                } else if(data.success) {
                    //~ Om allt går bra: logga lite data:
                    console.log(data.success);
                    console.log(data.check_value);

                    //~ Uppdatera vår textruta med prio.
                    if(data.check_value === "invoiced") {
                        // Sätt texten i div med id="order_status_???" till Prio eller Normal beroende på om prio är true/false
                        $("#invoice_status_" + data.order_id).html("Invoiced");
                        $("#invoice_text_" + data.order_id).html("Invoiced");
                        $("#invoice_ba_" + data.order_id).html('<span class="badge badge-success">Invoiced</span>');
                    } else if(data.check_value === "to invoice"){
                        $("#invoice_status_" + data.order_id).html("Not Confirm Invoice Yet");
                        $("#invoice_text_" + data.order_id).html("Not Confirm Invoice Yet");
                        $("#invoice_ba_" + data.order_id).html('<span class="badge badge-danger">To Invoice</span>');
                    } else {
                        $("#invoice_status_" + data.order_id).html("No Invoice");
                        $("#invoice_text_" + data.order_id).html("No Invoice");
                        $("#invoice_ba_" + data.order_id).html('<span class="badge badge-warning">No Invoice</span>');
                    }
                }
            });
    });

    // Hitta på sidan
    $('#table').on('click','.flag', function (ev) {

        //~ If this method is called, the default action of the event will not be triggered.
        ev.preventDefault();

        var $link = $(ev.currentTarget);

        //~ Logga länken användaren klickade på
        console.log($link.data('href'));

        // href pekar unikt på respektive order, använder inloggning från sessionen när vi anropar vår controller /service/<model("sale.order"):order>/order/flag
        ajax.jsonRpc($link.data('href'), 'call', {})
            .then(function (data) {

                //~ Logga responsen från vår controller
                console.log(data);

                // Felhantering
                if(data.error) {
                    var $warning;
                    if(data.error === 'anonymous_user') {
                        $warning = $('<div class="alert alert-danger alert-dismissable oe_forum_alert" id="flag_alert">'+
                            '<button type="button" class="close notification_close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
                            _t('Sorry you must be logged in to flag a post') +
                            '</div>');
                    } else if(data.error === 'post_non_flaggable') {
                        $warning = $('<div class="alert alert-danger alert-dismissable oe_forum_alert" id="flag_alert">'+
                            '<button type="button" class="close notification_close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
                            _t('This post can not be flagged') +
                            '</div>');
                    }

                    //~ Hitta meddelanderutan för länken
                    var flag_alert = $link.parent().find("#flag_alert");

                    //~ Lägg in varningen i vår meddelanderuta
                    if (flag_alert.length === 0) {
                        $link.parent().append($warning);
                    }

                } else if(data.success) {
                    //~ Om allt går bra: logga lite data:
                    console.log(data.success);
                    console.log(data.flag_value);

                    //~ Uppdatera vår textruta med prio.
                    if(data.flag_value === true) {
                        // Sätt texten i div med id="order_status_???" till Prio eller Normal beroende på om prio är true/false
                        $("#prio_status_" + data.order_id).html('<span class="badge badge-danger">Prio</span>');
                        $("#prio_text_" + data.order_id).html('Prio');
                    } else {
                        $("#prio_status_" + data.order_id).html('<span class="badge badge-info">Normal/Non-Prio</span>');
                        $("#prio_text_" + data.order_id).html('Normal/Non-Prio');
                    }
                }
            });
    });

  $('#table').DataTable({
//  url: 'data1.json',
  pagination: true,
  search: true,
  })

//     Sort by order.amount_total
//    $('.sort_amount').on('click', function (ev) {
//
//
//        //~ If this method is called, the default action of the event will not be triggered.
//        ev.preventDefault();
//        var $link = $(ev.currentTarget);
//        var header=$link.data('header')
//
//
//        //~ Logga länken användaren klickade på
//        console.log($link.data('header')); //amount_total
//        console.log($link.data('href')); //'/service/order/sort_amount'
//
//        // href pekar unikt på respektive order, använder inloggning från sessionen när vi anropar vår controller /service/<model("sale.order"):order>/order/flag
//        ajax.jsonRpc($link.data('href'), 'call', {})
//            .then(function (data) {
//
//            var $link_url='';
//
//                //~ Logga responsen från vår controller
//                console.log(data);  // All data pacage from controller sort_amount
//
//                // Felhantering
//                if(data.success) {
//                    //~ Om allt går bra: logga lite data:
//                    // from data pacakge from controller
//                    console.log(data.success);
//                    console.log(data.order_ids);
//                    console.log(data.order_ids_sorted);
//
//                    //~ Uppdatera vår textruta med prio.
//                    if(data.order_ids_sorted==true || $link.data('header')=='amount_total') {
//                    console.log($link.data('header')=='amount_total');
//                    console.log('oh my god');
//
//                    //~ Lägg in varningen i vår meddelanderuta
////                    order_ids = http.request.env['sale.order'].search([]).sorted(key=lambda r: r.amount_total, reverse=True)
////                    <t t-set='foo' t-value='order_ids.sorted(key=lambda x:x.amount_total)'>
////                        $link_url=$('<t t-set="foo" t-value="'+data.order_ids+'".sorted(key=lambda x:x.'+header+')"/>');
////
////                        $(".show_sort").append($link_url);
////                        $("#index_table.show_sort").html('hahah');
////                        $("#show_sort").html('hahah');
//
//                        // Sätt texten i div med id="order_status_???" till Prio eller Normal beroende på om prio är true/false
////                        $("#sort_amount").html('<t t-set="foo" t-value="'+data.order_ids+'".sorted(key=lambda x:x.'+header+')"/>');
//                        $(".show_sort").html('<t t-set="foo" t-value="order_ids.sorted(key=lambda x:x.amount_total)"/>');
////                        $("#show_sort").html('<t t-set="foo" t-value="order_ids.sorted(key=lambda x:x.amount_total)"/>');
//                    } else {
//                    console.log('no');
////                    $("#sort_amount2").append('hahah');
////                        $link_url=$('<t t-set="foo" t-value="'+data.order_ids+'"/>');
////                        $("#sort_amount").append($link_url);
//////                        $("#sort_amount").append("ahahah");
//                        $("#show_sort").html('<t t-set="foo" t-value="'+data.order_ids+'"/>');
//                    }
//
//            }else if(data.error) {
//                    var $warning;
//                    if(data.error === 'sort_amount not works. Sad!:(') {
//                        $warning = $('<div class="alert alert-danger alert-dismissable oe_forum_alert" id="flag_alert">'+
//                            '<button type="button" class="close notification_close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
//                            _t('Sorry you must be logged in to flag a post') +
//                            '</div>');
//                    }
//
//                    //~ Hitta meddelanderutan för länken
//                    var flag_alert = $link.parent().find("#flag_alert");
//
//                    //~ Lägg in varningen i vår meddelanderuta
//                    if (flag_alert.length === 0) {
//                        $link.parent().append($warning);
//                    }
//
//                }
//    });
//
//// js-------------------------------------------------------------------------------------------
////    var table = $('table');
////
////    $('#amount_total, #prio')
////        .wrapInner('<span title="sort this column"/>')
////        .each(function(){
////            var th = $(this),
////                thIndex = th.index(),
////                inverse = false;
////            th.click(function(){
////                table.find('td').filter(function(){
////                    return $(this).index() === thIndex;
////                }).sortElements(function(a, b){
////                    return $.text([a]) > $.text([b]) ?
////                        inverse ? -1 : 1
////                        : inverse ? 1 : -1;
////                }, function(){
////                    // parentNode is the element we want to move
////                    return this.parentNode;
////                });
////                inverse = !inverse;
////            });
////
////        });
//
//
//});

});