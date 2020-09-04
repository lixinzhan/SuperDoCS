(function($) {
    ////////////////////////////////////////////////////////////////
    showAlert = function() {
        alert('tst new showAlert');
    };
    
    warningLeave = function(WarningMsg) {
        if (WarningMsg!='') {
            var confirmExit = confirm(WarningMsg);
            if (confirmExit){ return true; }
            else { return false; }
        }
        return true;
    };

    handleROF = function() {
        $('#setup-table input#id_SpecifyROF').is(':checked') ? ShowROFEntry(): HideROFEntry();
        $('#setup-table input#id_SpecifyROF').click(function() {
            $(this).is(':checked') ? ShowROFEntry() : HideROFEntry();
        });
    };
    
    function ShowROFEntry() {
        $('#setup-table input#id_ROF_Exposure').parents("tr").show();
    }
    function HideROFEntry() {
        var autoROF = $('input#id_autoROF').val();
        $('#setup-table input#id_ROF_Exposure').val(autoROF);
        $('#setup-table input#id_ROF_Exposure').parents("tr").hide();
    }
    
    ////////////////////////////////////////////////////////////////
    
    handleCutout = function() {
        $('#setup-table input#id_CutoutRequired').is(':checked') ? ShowCutoutEntries() : HideCutoutEntries();
        $('#setup-table input#id_CutoutRequired').click(function() {
            $(this).is(':checked') ? ShowCutoutEntries() : HideCutoutEntries();
        });
    };
    
    function ShowCutoutEntries()
    {
        $('#setup-table select#id_CutoutShape').parents("tr").show();
        $('#setup-table input#id_CutoutLength').parents("tr").show();
        $('#setup-table input#id_CutoutWidth').parents("tr").show();
        $('#setup-table input#id_CutoutThickness').parents("tr").show();        
    }
    function HideCutoutEntries()
    {
        $('#setup-table select#id_CutoutShape').parents("tr").hide();
        $('#setup-table input#id_CutoutLength').parents("tr").hide();
        $('#setup-table input#id_CutoutWidth').parents("tr").hide();
        $('#setup-table input#id_CutoutThickness').parents("tr").hide();        
    }

    ////////////////////////////////////////////////////////////////

    var FormChanged_NonCalcPart = false
    var FormChanged_CalcPart = false
    var FormChanged_CalcDone = false
    var warning = '';
    var warning_NonCalcPartChange = "WARNING: You have made changes! "
                        + "Please SAVE before navigating from this page "
                        + "or all changes will be lost! \n\n"
                        + "CONTINUE ANYWAY?";
    var warning_CalcPartChange = 'WARNING: You have made changes that might affect treatment delivery! '
                        + 'Please Re-Calculate and Save before navigating from this page '
                        + 'or all changes will be lost! \n\n'
                        + 'CONTINUE ANYWAY?';
    var warning_CalcDone = 'WARNING: you have made changes to the calculation. '
                    + 'Please SAVE before navigating from this page '
                    + 'or all changes will be lost! \n\n'
                    + 'CONTINUE ANYWAY?';
    
    handleFormChange = function() {
        $('#id_newcalc').each(function() {
            FormChanged_CalcDone = true;
            $('html, body').animate({
                    scrollTop: $(document).height()
                 },
                 0);
                 return false;
        });
        
        // backup initial values
        $('#setup-table input').each(function() {
            $(this).data('initial_value', $(this).serialize());
        });
        
        $('#setup-table input#id_PlanName, '+
          '#setup-table input#id_PatientId, '+
          '#setup-table input#id_LastName, '+
          '#setup-table input#id_FirstName, '+
          '#setup-table select#id_Doctor, '+
          '#setup-table textarea#id_Comment').change(function() {
            if ($(this).data('init_value') != $(this).serialize()) {
               FormChanged_NonCalcPart = true;
            }
        });
        
        $('#setup-table input#id_TotalDose, '+
          '#setup-table input#id_Fractions, '+
          '#setup-table input#id_PrescriptionDepth, '+
          '#setup-table select#id_TargetTissue, '+
          '#setup-table select#id_Filter, '+
          '#setup-table select#id_Cone, '+
          '#setup-table input#id_CutoutRequired, '+
          '#setup-table select#id_CutoutShape, '+
          '#setup-table input#id_CutoutLength, '+
          '#setup-table input#id_CutoutWidth, '+
          '#setup-table input#id_CutoutThickness, '+
          '#setup-table input#id_StandOut, '+
          '#setup-table input#id_SpecifyROF, '+
          '#setup-table input#id_ROF_Exposure').change(function() {
            if ($(this).data('init_value') != $(this).serialize()) {
                FormChanged_CalcPart = true
                $('#calc_time').hide();
            }
        });
        
        $('a').click(function(){
            warning = '';
            if (FormChanged_CalcPart)         { warning = warning_CalcPartChange; }
            else if (FormChanged_NonCalcPart) { warning = warning_NonCalcPartChange; }
            else if (FormChanged_CalcDone)    { warning = warning_CalcDone; }
            var leave = warningLeave(warning);
            return leave;
        });
        $('#txbuttongroup input[name=qa_submit]').click(function() {
            warning = '';
            if (FormChanged_CalcPart)         { warning = warning_CalcPartChange; }
            else if (FormChanged_NonCalcPart) { warning = warning_NonCalcPartChange; }
            else if (FormChanged_CalcDone)    { warning = warning_CalcDone; }
            var leave = warningLeave(warning);
            return leave;
        });
        $('#txbuttongroup input[name=cancel_submit]').click(function() {
            warning = '';
            if (FormChanged_CalcPart)         { warning = warning_CalcPartChange; }
            else if (FormChanged_NonCalcPart) { warning = warning_NonCalcPartChange; }
            else if (FormChanged_CalcDone)    { warning = warning_CalcDone; }
            var leave = warningLeave(warning);
            return leave;
        });
        $('#txbuttongroup input[name=save_submit]').click(function() {
            warning = '';
            if (FormChanged_CalcPart) {
                warning = warning_CalcPartChange;
                var leave = warningLeave(warning);
                return leave;
            }
            FormChanged_CalcDone = false;
            FormChanged_CalcPart = false;
            FormChanged_NonCalcPart = false;
            warning = '';
            return true;
        });
        
    }; // handleDataChange

})(jQuery);
