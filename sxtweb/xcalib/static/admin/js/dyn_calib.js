$(document).ready(function(){
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

//// Automatic calculation of P_isf
    $('#id_FDD').change(function() {
        var fdd = $('#id_FDD').val();
        var fcd = $('#id_Cone option:selected').text().split("FCD")[1];
        var isf = (fdd/parseFloat(fcd))**2;
        $('#id_P_isf').prop("readonly", false);
        $('#id_P_isf').val(isf);
        $('#id_P_isf').prop("readonly", true);
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
        $('#id_P_tp').prop("readonly", false);
        $('#id_P_tp').val(ptp);
        $('#id_P_tp').prop("readonly", true);
    }
})
