function resetAction() {
    // Reset sliders
    $("#visibleH2Production").data("ionRangeSlider").update({ from: defaultValueForH2Production });
    // ... repeat for other sliders ...

    // Reset display elements for calculation results
    $("#totalElectricityRequirement").text('Default Value or Empty');
    $("#totalCO2Emissions").text('Default Value or Empty');
    // ... repeat for other display elements ...

    // Reset or clear plots
    // This depends on how you're generating plots. You might need to re-render them with default data
    // or clear them if they are generated client-side.
    // Example for Chart.js:
    // myChart.data.datasets[0].data = [defaultDataset];
    // myChart.update();
}

// Attach this function to your reset button
