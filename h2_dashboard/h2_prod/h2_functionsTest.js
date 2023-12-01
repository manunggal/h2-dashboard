// Function to update dashboard data (reset values, update calculation, update plot, etc.)
function updateDashboardData(isReset = false, sliderId = null, data = null) {

    // Determine if it's a reset action or regular slider update
    if (isReset) {
      // AJAX call for reset
      $.ajax({
        type: "POST",
        url: "http://localhost:8000/h2_prod/hydrogen-production/",
        data: {
          'csrfmiddlewaretoken': "{{ csrf_token }}",
          'reset': true
        },
        success:function  (response) {
          if (response.reset){
            // Update page elements to reflect the reset state
            $('#displayTotalElectricityRequirement').text('4281 TWh');
            $('#displayTotalH2Production').text('90 MegaTonnes');
            $('#displayRequiredElectrolyzerUnits').text('24437 Units');
            $('#displayTotalCO2eEmissions').text('1409 MegaTonnes');
            // reset sliders
            $("#visibleH2Production").data("ionRangeSlider").update({
              from: 90
            });
          } 
        }
      });
      return;
    }
    
    //For regular slider update
    if (sliderId && data) {
      // update the hidden input for the current sliders
      var hiddenInputId = sliderId.replace("visible", "hidden");
      $("#" + hiddenInputId).val(data.from);

      // Get the slider values
      var hiddenH2Production = $('#hiddenH2Production').val();
      var hiddenElectrolyzerEff = $('#hiddenElectrolyzerEff').val();
      var hiddenRenewablePct = $('#hiddenRenewablePct').val();
      var hiddenCO2Emission = $('#hiddenCO2Emission').val();

      // AJAX call
      $.ajax({
        type: "POST",
        url: "http://localhost:8000/h2_prod/hydrogen-production/",
        data: {
          'csrfmiddlewaretoken': "{{ csrf_token }}",
          'hiddenH2Production': hiddenH2Production,
          'hiddenElectrolyzerEff': hiddenElectrolyzerEff,
          'hiddenRenewablePct': hiddenRenewablePct,
          'hiddenCO2Emission': hiddenCO2Emission
        },
        success: function (response) {
          //update page with response data
          $('#displayTotalElectricityRequirement').text(response.total_electricity_requirement + ' TWh');
          $('#displayTotalH2Production').text(response.total_h2_production + ' MegaTonnes');
          $('#displayRequiredElectrolyzerUnits').text(response.required_electrolyzer_units + ' Units');
          $('#displayTotalCO2eEmissions').text(response.total_co2_emissions + ' MegaTonnes');
        }
      })
      }
  }