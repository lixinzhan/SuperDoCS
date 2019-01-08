$(document).ready(function(){
    // Force the voltages to be readonly
    $('#id_V_std').prop("readonly", true);
    $('#id_V_opp').prop("readonly", true);
    $('#id_V_low').prop("readonly", true);

    // Force correction factors to be readonly
    $('#id_P_isf').prop("readonly", true);
    $('#id_P_tp').prop("readonly", true);

    // Hide and/or change button name
    $('input[name="_addanother"]').hide();
    $('input[name="_continue"]').val("Calculate and Save");

    //$('label[for="id_Has_Pion_Ppol"]').attr("required", true);

//// Show or Hide measurements for low/opp voltages
    $('#id_Has_Pion_Ppol').is(':checked')?hideOppLow():showOppLow();
    $('#id_Has_Pion_Ppol').click(function() {
        $(this).is(':checked')?hideOppLow():showOppLow();
    });
    function hideOppLow() {
        $('#id_V_opp').parent('div').parent('div').hide();
        $('#id_M_opp').parent('div').parent('div').hide();
        $('#id_V_low').parent('div').parent('div').hide();
        $('#id_M_low').parent('div').parent('div').hide();
        $('#id_P_ion').prop("readonly", false);
        $('#id_P_pol').prop("readonly", false);
    }
    function showOppLow() {
        $('#id_V_opp').parent('div').parent('div').show();
        $('#id_M_opp').parent('div').parent('div').show();
        $('#id_V_low').parent('div').parent('div').show();
        $('#id_M_low').parent('div').parent('div').show();
        $('#id_P_ion').prop("readonly", true);
        $('#id_P_pol').prop("readonly", true);
    }

//// Automatic calculate P_ion and Ppol
    $('#id_M_std').change(function() {
        updatePion();
        updatePpol();
    });
    $('#id_M_opp').change(function() {
        updatePpol();
    });
    $('#id_M_low').change(function() {
        updatePion();
    });
    function updatePion() {
        if ($('#id_Has_Pion_Ppol').is(':not(:checked)')) {
            var vh = parseFloat($('#id_V_std').val());
            var vl = parseFloat($('#id_V_low').val());
            var mh = parseFloat($('#id_M_std').val());
            var ml = parseFloat($('#id_M_low').val());
            var pion = (1.0-(vh/vl)**2)/(mh/ml-(vh/vl)**2);
            $('#id_P_ion').val(pion);
        }
    }
    function updatePpol() {
        if ($('#id_Has_Pion_Ppol').is(':not(:checked)')) {
            var mstd = parseFloat($('#id_M_std').val());
            var mopp = parseFloat($('#id_M_opp').val());
            var ppol = Math.abs((mstd-mopp)/(2.0*mstd));
            $('#id_P_pol').val(ppol);
        }
    }

//// Automatic calculation of P_isf
    $('#id_FDD').change(function() {
        var fdd = $('#id_FDD').val();
        var fcd = $('#id_Cone option:selected').text().split("FCD")[1];
        var isf = (fdd/parseFloat(fcd))**2;
        //$('#id_P_isf').prop("readonly", false);
        $('#id_P_isf').val(isf);
    });

//// Automatic calculation of P_tp
    $('#id_Pressure').change(function() {
        updatePtp();
    });
    $('#id_Temperature').change(function() {
        updatePtp();
    });
    function updatePtp() {
        var presr = parseFloat($('#id_Pressure').val());
        var tempr = parseFloat($('#id_Temperature').val());
        var ptp = 760.0*(tempr+273.2)/(presr*295.2);
        //$('#id_P_tp').prop("readonly", false);
        $('#id_P_tp').val(ptp);
    }

//// Display Units for DR_Air and DR_Water
    var kerma = 'Air Kerma Rate in Air (cGy/';
    var dose = 'Dose Rate at Water Surface (cGy/';
    var punit = $('#id_DurationUnit option:selected').val();
    var pend = '):';
    $('label[for="id_DR_Air"]').text(kerma+punit+pend);
    $('label[for="id_DR_Water"]').text(dose+punit+pend);
    $('#id_DurationUnit').change(function() {
        punit = $('#id_DurationUnit option:selected').val();
        $('label[for="id_DR_Air"]').text(kerma+punit+pend);
        $('label[for="id_DR_Water"]').text(dose+punit+pend);
        $('#id_DR_Air').val(0.0);
        $('#id_DR_Water').val(0.0);
    });

//// Handling DR_Air and DR_Water
    $('form#calibration_form :input').change(function(event) {
        if (event.target.id=='id_CalibName') { return; }
        if (event.target.id=='id_Comment') { return; }
        if (event.target.id=='id_Status') { return; }
        if (event.target.id=='id_MeasurementDate') { return; }
        if (event.target.id=='id_MeasuredByUser') { return; }
        if (event.target.type=='submit') { return; }
        $('#id_DR_Air').val(0.0);
        $('#id_DR_Water').val(0.0);
    });

})

